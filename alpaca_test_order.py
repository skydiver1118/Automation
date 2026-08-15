import os

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    client = TradingClient(
        api_key=require_env("ALPACA_API_KEY"),
        secret_key=require_env("ALPACA_SECRET_KEY"),
        paper=True,
    )

    order = MarketOrderRequest(
        symbol="AAPL",
        qty=1,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
    )

    submitted = client.submit_order(order)
    print(f"id={submitted.id}")
    print(f"client_order_id={submitted.client_order_id}")
    print(f"symbol={submitted.symbol}")
    print(f"side={submitted.side}")
    print(f"qty={submitted.qty}")
    print(f"status={submitted.status}")
    print(f"type={submitted.type}")
    print(f"time_in_force={submitted.time_in_force}")
    print(f"submitted_at={submitted.submitted_at}")


if __name__ == "__main__":
    main()
