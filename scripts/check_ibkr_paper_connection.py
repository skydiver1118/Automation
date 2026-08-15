import argparse
import threading
import time
from queue import Empty, Queue

from ibapi.client import EClient
from ibapi.wrapper import EWrapper


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 7497
DEFAULT_CLIENT_ID = 7


class IbkrConnectionCheck(EWrapper, EClient):
    def __init__(self) -> None:
        EClient.__init__(self, self)
        self.events: Queue[tuple[str, object]] = Queue()

    def nextValidId(self, orderId: int) -> None:
        self.events.put(("next_valid_id", orderId))

    def managedAccounts(self, accountsList: str) -> None:
        accounts = [account.strip() for account in accountsList.split(",") if account.strip()]
        self.events.put(("managed_accounts", accounts))

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str) -> None:
        if tag in {"NetLiquidation", "TotalCashValue", "BuyingPower"}:
            self.events.put(("account_summary", (account, tag, value, currency)))

    def accountSummaryEnd(self, reqId: int) -> None:
        self.events.put(("account_summary_end", reqId))

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson="") -> None:
        self.events.put(("error", (reqId, errorCode, errorString)))


def wait_for_event(app: IbkrConnectionCheck, wanted: set[str], timeout: float) -> tuple[str, object] | None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            event = app.events.get(timeout=0.25)
        except Empty:
            continue
        print_event(event)
        if event[0] in wanted:
            return event
    return None


def print_event(event: tuple[str, object]) -> None:
    name, payload = event
    if name == "next_valid_id":
        print(f"next_valid_order_id={payload}")
    elif name == "managed_accounts":
        accounts = payload or []
        print(f"managed_accounts={','.join(accounts) if accounts else '(none)'}")
    elif name == "account_summary":
        account, tag, value, currency = payload
        print(f"account_summary account={account} tag={tag} value={value} currency={currency}")
    elif name == "error":
        _, code, message = payload
        print(f"ib_error code={code} message={message}")


def check_connection(host: str, port: int, client_id: int, timeout: float) -> int:
    app = IbkrConnectionCheck()
    app.connect(host, port, clientId=client_id)

    if not app.isConnected():
        print(f"Unable to connect to IBKR API at {host}:{port}.")
        print("Start TWS or IB Gateway in paper mode, then enable API socket clients.")
        print("For paper TWS, use Configure > API > Settings, enable socket clients, and confirm the socket port is 7497.")
        return 2

    thread = threading.Thread(target=app.run, daemon=True)
    thread.start()

    try:
        connected = wait_for_event(app, {"next_valid_id"}, timeout)
        if connected is None:
            print(f"Connected to {host}:{port}, but IBKR did not complete the API handshake within {timeout:.1f}s.")
            return 3

        app.reqManagedAccts()
        wait_for_event(app, {"managed_accounts"}, timeout)

        app.reqAccountSummary(9001, "All", "NetLiquidation,TotalCashValue,BuyingPower")
        wait_for_event(app, {"account_summary_end"}, timeout)
        app.cancelAccountSummary(9001)

        print("IBKR paper API connection check completed.")
        return 0
    finally:
        app.disconnect()
        thread.join(timeout=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check a local Interactive Brokers paper trading API connection.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="TWS/Gateway API host.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Paper TWS defaults to 7497; paper Gateway usually uses 4002.")
    parser.add_argument("--client-id", type=int, default=DEFAULT_CLIENT_ID, help="Unique IBKR API client ID.")
    parser.add_argument("--timeout", type=float, default=10.0, help="Seconds to wait for each API response.")
    args = parser.parse_args()

    raise SystemExit(check_connection(args.host, args.port, args.client_id, args.timeout))


if __name__ == "__main__":
    main()
