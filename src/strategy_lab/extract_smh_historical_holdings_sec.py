from __future__ import annotations

import html
import json
import re
import time
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Any
from urllib.parse import quote
from xml.etree import ElementTree as ET

import pandas as pd
import requests


SEC_USER_AGENT = "Codex SMH holdings research contact@example.com"
CIK = "1137360"
SMH_SERIES_ID = "S000034411"
HOLDRS_CIK = "728612"

DATA_DIR = Path("data/smh_components")
CACHE_DIR = DATA_DIR / "sec_cache"
REPORT_DIR = Path("reports")


NAME_TO_TICKER = {
    "advanced micro devices": "AMD",
    "altera": "ALTR",
    "analog devices": "ADI",
    "applied materials": "AMAT",
    "arm holdings": "ARMH",
    "asml": "ASML",
    "astera labs": "ALAB",
    "atmel": "ATML",
    "avago technologies": "AVGO",
    "broadcom corp": "BRCM",
    "broadcom inc": "AVGO",
    "broadcom ltd": "AVGO",
    "broadcom": "AVGO",
    "cadence design systems": "CDNS",
    "cavium": "CAVM",
    "cree": "CREE",
    "credo technology": "CRDO",
    "entegra": "ENTG",
    "entegris": "ENTG",
    "integrated device technology": "IDTI",
    "intel": "INTC",
    "kla-tencor": "KLAC",
    "kla corp": "KLAC",
    "lam research": "LRCX",
    "linear technology": "LLTC",
    "marvell technology": "MRVL",
    "maxim integrated": "MXIM",
    "microchip technology": "MCHP",
    "microsemi": "MSCC",
    "micron technology": "MU",
    "monolithic power": "MPWR",
    "mks instruments": "MKSI",
    "nvidia": "NVDA",
    "nxp semiconductor": "NXPI",
    "nxp semiconductors": "NXPI",
    "on semiconductor": "ON",
    "qualcomm": "QCOM",
    "qorvo": "QRVO",
    "sandisk": "SNDK",
    "skyworks solutions": "SWKS",
    "stmicroelectronics": "STM",
    "synopsys": "SNPS",
    "taiwan semiconductor": "TSM",
    "teradyne": "TER",
    "texas instruments": "TXN",
    "universal display": "OLED",
    "xilinx": "XLNX",
}

@dataclass(frozen=True)
class Filing:
    form: str
    filing_date: str
    period_end: str
    accession: str
    document: str
    source_url: str


HOLDRS_POSAM_FILINGS = [
    Filing(
        form="POS AM",
        filing_date="2009-03-11",
        period_end="2009-03-11",
        accession="0000947871-09-000168",
        document="ss56639_posam-semi.htm",
        source_url=(
            "https://www.sec.gov/Archives/edgar/data/"
            f"{HOLDRS_CIK}/000094787109000168/ss56639_posam-semi.htm"
        ),
    ),
    Filing(
        form="POS AM",
        filing_date="2010-04-15",
        period_end="2010-04-15",
        accession="0000947871-10-000490",
        document="ss87938_posam-semi.htm",
        source_url=(
            "https://www.sec.gov/Archives/edgar/data/"
            f"{HOLDRS_CIK}/000094787110000490/ss87938_posam-semi.htm"
        ),
    ),
    Filing(
        form="POS AM",
        filing_date="2011-03-15",
        period_end="2011-03-15",
        accession="0000947871-11-000271",
        document="ss113520_posam-semi.htm",
        source_url=(
            "https://www.sec.gov/Archives/edgar/data/"
            f"{HOLDRS_CIK}/000094787111000271/ss113520_posam-semi.htm"
        ),
    ),
]


def request_text(url: str, cache_name: str | None = None) -> str:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if cache_name:
        cache_path = CACHE_DIR / cache_name
        if cache_path.exists():
            return cache_path.read_text(encoding="utf-8", errors="ignore")
    response = requests.get(url, headers={"User-Agent": SEC_USER_AGENT}, timeout=90)
    response.raise_for_status()
    text = response.text
    if cache_name:
        cache_path.write_text(text, encoding="utf-8")
    time.sleep(0.11)
    return text


def sec_search(query: str, forms: str, size: int = 100) -> list[dict[str, Any]]:
    url = (
        "https://efts.sec.gov/LATEST/search-index"
        f"?dateRange=all&category=custom&q={quote(query)}&forms={quote(forms)}"
        f"&from=0&size={size}"
    )
    data = json.loads(request_text(url, f"search_{safe_name(query)}_{safe_name(forms)}.json"))
    return data.get("hits", {}).get("hits", [])


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:120]


def archive_url(accession: str, document: str) -> str:
    accession_no_dash = accession.replace("-", "")
    document = document.split("/", 1)[-1]
    return f"https://www.sec.gov/Archives/edgar/data/{CIK}/{accession_no_dash}/{document}"


def discover_nport_filings() -> list[Filing]:
    filings: list[Filing] = []
    for hit in sec_search(SMH_SERIES_ID, "NPORT-P", 100):
        source = hit["_source"]
        accession = source["adsh"]
        filings.append(
            Filing(
                form=source.get("form", "NPORT-P"),
                filing_date=source.get("file_date", ""),
                period_end=source.get("period_ending", ""),
                accession=accession,
                document="primary_doc.xml",
                source_url=archive_url(accession, "primary_doc.xml"),
            )
        )
    return sorted(unique_filings(filings), key=lambda filing: filing.period_end)


def load_submission_rows() -> list[dict[str, Any]]:
    base = "https://data.sec.gov/submissions/"
    main = json.loads(request_text(base + "CIK0001137360.json", "CIK0001137360.json"))
    rows: list[dict[str, Any]] = []

    def add(payload: dict[str, Any]) -> None:
        recent = payload["filings"]["recent"] if "filings" in payload else payload
        row_count = len(recent["form"])
        keys = [key for key, value in recent.items() if isinstance(value, list) and len(value) == row_count]
        for index in range(row_count):
            rows.append({key: recent[key][index] for key in keys})

    add(main)
    for file_info in main.get("filings", {}).get("files", []):
        add(json.loads(request_text(base + file_info["name"], file_info["name"])))
    return rows


def discover_nq_filings() -> list[Filing]:
    filings: list[Filing] = []
    for row in sorted(load_submission_rows(), key=lambda item: item["filingDate"]):
        if row.get("form") != "N-Q":
            continue
        accession = row["accessionNumber"]
        document = row["primaryDocument"]
        url = archive_url(accession, document)
        text = request_text(url, f"{accession}_{document}")
        lowered = text.lower()
        if "semiconductor etf" not in lowered and "vaneck vectors semiconductor" not in lowered:
            continue
        filings.append(
            Filing(
                form="N-Q",
                filing_date=row.get("filingDate", ""),
                period_end=row.get("reportDate", ""),
                accession=accession,
                document=document,
                source_url=url,
            )
        )
    return sorted(unique_filings(filings), key=lambda filing: filing.period_end)


def discover_shareholder_report_filings() -> list[Filing]:
    filings: list[Filing] = []
    for hit in sec_search('"Semiconductor ETF" "SMH"', "N-CSR,N-CSRS", 100):
        source = hit["_source"]
        if CIK.zfill(10) not in source.get("ciks", []):
            continue
        accession = source["adsh"]
        document = hit["_id"].split(":", 1)[1]
        filings.append(
            Filing(
                form=source.get("form", ""),
                filing_date=source.get("file_date", ""),
                period_end=source.get("period_ending", ""),
                accession=accession,
                document=document,
                source_url=archive_url(accession, document),
            )
        )
    return sorted(unique_filings(filings), key=lambda filing: filing.period_end)


def unique_filings(filings: list[Filing]) -> list[Filing]:
    seen: set[tuple[str, str]] = set()
    unique: list[Filing] = []
    for filing in filings:
        key = (filing.accession, filing.document)
        if key in seen:
            continue
        seen.add(key)
        unique.append(filing)
    return unique


def parse_nport(filing: Filing) -> list[dict[str, Any]]:
    xml_text = request_text(filing.source_url, f"{filing.accession}_primary_doc.xml")
    root = ET.fromstring(xml_text)
    ns = {"n": "http://www.sec.gov/edgar/nport"}
    series = text_of(root.find(".//n:genInfo/n:seriesName", ns))
    series_id = text_of(root.find(".//n:genInfo/n:seriesId", ns))
    report_date = text_of(root.find(".//n:genInfo/n:repPdDate", ns)) or filing.period_end
    if series_id != SMH_SERIES_ID:
        return []

    records: list[dict[str, Any]] = []
    for holding in root.findall(".//n:invstOrSecs/n:invstOrSec", ns):
        asset_cat = text_of(holding.find("n:assetCat", ns))
        name = clean_security_name(text_of(holding.find("n:name", ns)))
        if not name or asset_cat != "EC":
            continue
        records.append(
            {
                "period_end": report_date,
                "filing_date": filing.filing_date,
                "form": filing.form,
                "source_type": "SEC N-PORT",
                "series": series,
                "accession": filing.accession,
                "source_url": filing.source_url,
                "security_name": name,
                "ticker_guess": ticker_guess(name),
                "cusip": text_of(holding.find("n:cusip", ns)),
                "shares": parse_number(text_of(holding.find("n:balance", ns))),
                "market_value_usd": parse_number(text_of(holding.find("n:valUSD", ns))),
                "pct_value": parse_number(text_of(holding.find("n:pctVal", ns))),
            }
        )
    return records


def parse_report_html(filing: Filing) -> list[dict[str, Any]]:
    text = request_text(filing.source_url, f"{filing.accession}_{filing.document}")
    start = find_schedule_start(text)
    if start < 0:
        return []

    section = text[start : start + 260_000]
    records: list[dict[str, Any]] = []
    for table in pd.read_html(StringIO(section)):
        flat = flat_text(table)
        upper = flat.upper()
        if "SUMMARY OF INVESTMENTS" in upper or "LEVEL 1" in upper and records:
            break
        for _, row in table.iterrows():
            record = parse_holding_row(list(row))
            if record is None:
                continue
            records.append(
                {
                    "period_end": filing.period_end or period_from_section(section),
                    "filing_date": filing.filing_date,
                    "form": filing.form,
                    "source_type": "SEC shareholder/N-Q report",
                    "series": "VanEck/Market Vectors Semiconductor ETF",
                    "accession": filing.accession,
                    "source_url": filing.source_url,
                    **record,
                }
            )
    return records


def parse_holdrs_posam(filing: Filing) -> list[dict[str, Any]]:
    text = request_text(filing.source_url, f"{filing.accession}_{filing.document}")
    records: list[dict[str, Any]] = []
    for table in pd.read_html(StringIO(text)):
        flat = flat_text(table)
        flat_compact = re.sub(r"[^a-z0-9]+", "", flat.lower())
        if (
            "nameofcompany" not in flat_compact
            or "shareamounts" not in flat_compact
            or "advancedmicrodevices" not in flat_compact
        ):
            continue
        for _, row in table.iloc[1:].iterrows():
            values = [clean_cell(value) for value in row]
            if len(values) < 5:
                continue
            name = clean_security_name(values[0])
            ticker = values[2].strip().upper()
            share_amount = parse_number(values[4])
            if not name or not ticker or ticker == "NAN":
                continue
            records.append(
                {
                    "period_end": filing.period_end,
                    "filing_date": filing.filing_date,
                    "form": filing.form,
                    "source_type": "SEC legacy HOLDRS POS AM",
                    "series": "Semiconductor HOLDRS Trust",
                    "accession": filing.accession,
                    "source_url": filing.source_url,
                    "security_name": name,
                    "ticker_guess": ticker,
                    "cusip": "",
                    "shares": share_amount,
                    "market_value_usd": None,
                    "pct_value": None,
                }
            )
        if records:
            break
    return records


def find_schedule_start(text: str) -> int:
    holding_markers = [
        "advanced micro devices",
        "asml",
        "intel corp",
        "nvidia",
        "taiwan semiconductor",
    ]
    for schedule in re.finditer(r"schedule\s+of\s+investments", text, flags=re.IGNORECASE):
        immediate_before = text[max(0, schedule.start() - 700) : schedule.start()]
        after = text[schedule.end() : schedule.end() + 70_000].lower()
        before_words = re.sub(r"\s+", " ", strip_tags(immediate_before)).lower()
        before_compact = re.sub(r"[^a-z0-9]+", "", before_words)
        if not before_compact.endswith("semiconductoretf"):
            continue
        if not any(marker in after for marker in holding_markers):
            continue
        return max(0, schedule.start() - 1000)
    return -1


def parse_holding_row(row: list[Any]) -> dict[str, Any] | None:
    values = [clean_cell(value) for value in row]
    if len(values) < 4:
        return None

    share_index = -1
    shares = None
    for index, value in enumerate(values[:4]):
        parsed = parse_number(value)
        if parsed is not None:
            share_index = index
            shares = parsed
            break
    if shares is None:
        return None

    name = security_name_from_row(values, share_index)
    if not name or not looks_like_holding(name):
        return None

    value_numbers = [parse_number(value) for value in values[share_index + 1 :]]
    value_numbers = [value for value in value_numbers if value is not None]
    market_value = value_numbers[-1] if value_numbers else None
    if market_value is not None and market_value == shares:
        market_value = None

    name = clean_security_name(name)
    return {
        "security_name": name,
        "ticker_guess": ticker_guess(name),
        "cusip": "",
        "shares": shares,
        "market_value_usd": market_value,
        "pct_value": None,
    }


def security_name_from_row(values: list[str], share_index: int) -> str:
    candidates = []
    for index, value in enumerate(values[share_index + 1 : share_index + 7], start=share_index + 1):
        if not value:
            continue
        letter_count = len(re.findall(r"[A-Za-z]", value))
        candidates.append((letter_count, -index, value))
    candidates.sort(reverse=True)
    return candidates[0][2] if candidates else ""


def looks_like_holding(value: str) -> bool:
    lowered = re.sub(r"\s+", " ", value.lower())
    skip_words = [
        "common stocks",
        "preferred stocks",
        "total ",
        "cost:",
        "money market",
        "government cash",
        "overnight government",
        "collateral",
        "net assets",
        "liabilities",
        "number of shares",
        "value",
        "schedule of investments",
        "summary of investments",
    ]
    if any(word in lowered for word in skip_words):
        return False
    if re.search(r":\s*\(?\d", value):
        return False
    return bool(re.search(r"[A-Za-z]{3,}", value))


def period_from_section(section: str) -> str:
    text = re.sub(r"\s+", " ", strip_tags(section[:6000]))
    match = re.search(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\s+\d{1,2},\s+\d{4}",
        text,
    )
    if not match:
        return ""
    return pd.Timestamp(match.group(0)).date().isoformat()


def clean_cell(value: Any) -> str:
    if pd.isna(value):
        return ""
    return html.unescape(str(value)).replace("\xa0", " ").strip()


def clean_security_name(value: str) -> str:
    value = html.unescape(value).replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\s*\((ADR|USD)\)", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s*[#*†‡¦]+$", "", value).strip()
    return value


def parse_number(value: str) -> float | None:
    if not value:
        return None
    value = html.unescape(str(value)).replace("\xa0", " ").strip()
    if value in {"—", "-", "nan", "NaN"}:
        return None
    negative = "(" in value and ")" in value
    numbers = re.findall(r"\d+(?:\.\d+)?", value.replace(",", ""))
    if not numbers:
        return None
    number = float(numbers[0])
    return -number if negative else number


def text_of(element: ET.Element[str] | None) -> str:
    return "" if element is None or element.text is None else element.text.strip()


def flat_text(frame: pd.DataFrame) -> str:
    return " ".join(clean_cell(value) for value in frame.values.ravel())


def strip_tags(value: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", value))


def ticker_guess(name: str) -> str:
    normalized = re.sub(r"[^a-z0-9 ]", " ", name.lower())
    normalized = re.sub(r"\b(inc|corp|corporation|co|company|ltd|limited|nv|n v|plc|group)\b", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    for fragment, ticker in NAME_TO_TICKER.items():
        if fragment in normalized or fragment in name.lower():
            return ticker
    return ""


def build_snapshot_summary(holdings: pd.DataFrame) -> pd.DataFrame:
    summary = (
        holdings.groupby(["period_end", "source_type", "form", "accession", "source_url"], dropna=False)
        .agg(
            stock_count=("security_name", "nunique"),
            mapped_ticker_count=("ticker_guess", lambda values: int((values.astype(str) != "").sum())),
            tickers=("ticker_guess", lambda values: ", ".join(sorted(v for v in set(values.astype(str)) if v))),
            names=("security_name", lambda values: "; ".join(sorted(set(values.astype(str))))),
        )
        .reset_index()
        .sort_values("period_end")
    )
    return summary


def write_summary(summary: pd.DataFrame, holdings: pd.DataFrame) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    first = summary["period_end"].min()
    last = summary["period_end"].max()
    lines = [
        "# SMH Historical Holdings From Public SEC Filings",
        "",
        f"- Source fund: VanEck ETF Trust, CIK `{CIK.zfill(10)}`, SMH series `{SMH_SERIES_ID}` / class `C000105869`.",
        f"- Snapshots extracted: {len(summary)} from {first} to {last}.",
        f"- Equity holding rows extracted: {len(holdings)}.",
        "- Source types: legacy Semiconductor HOLDRS POS AM filings, pre-2019 N-Q/shareholder reports, and 2019+ N-PORT XML filings.",
        "- Caveat: ticker symbols are best-effort mappings from security names; the SEC rows are name/CUSIP/share/value records, not survivorship-free price data by themselves.",
        "",
        "## Snapshot Coverage",
        "",
        markdown_table(
            summary[
                ["period_end", "source_type", "form", "stock_count", "mapped_ticker_count", "tickers"]
            ].tail(20)
        ),
    ]
    (REPORT_DIR / "smh_historical_holdings_sec_summary.md").write_text("\n".join(lines), encoding="utf-8")


def markdown_table(frame: pd.DataFrame) -> str:
    columns = list(frame.columns)
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    nport_filings = discover_nport_filings()
    report_filings = discover_nq_filings() + discover_shareholder_report_filings()
    report_filings = sorted(unique_filings(report_filings), key=lambda filing: filing.period_end)
    report_filings = [filing for filing in report_filings if filing.period_end < "2019-09-30"]

    records: list[dict[str, Any]] = []
    for filing in HOLDRS_POSAM_FILINGS:
        parsed = parse_holdrs_posam(filing)
        print(f"{filing.period_end} {filing.form} {filing.accession}: {len(parsed)} legacy HOLDRS stocks")
        records.extend(parsed)
    for filing in report_filings:
        parsed = parse_report_html(filing)
        print(f"{filing.period_end} {filing.form} {filing.accession}: {len(parsed)} holdings")
        records.extend(parsed)
    for filing in nport_filings:
        parsed = parse_nport(filing)
        print(f"{filing.period_end} {filing.form} {filing.accession}: {len(parsed)} holdings")
        records.extend(parsed)

    holdings = pd.DataFrame(records)
    if holdings.empty:
        raise RuntimeError("No SMH holdings extracted")
    holdings = holdings.drop_duplicates(["period_end", "accession", "security_name"])
    holdings = holdings.sort_values(["period_end", "market_value_usd", "security_name"], ascending=[True, False, True])

    summary = build_snapshot_summary(holdings)
    holdings.to_csv(DATA_DIR / "smh_historical_holdings_sec.csv", index=False)
    summary.to_csv(DATA_DIR / "smh_historical_snapshots_sec.csv", index=False)
    with pd.ExcelWriter(DATA_DIR / "smh_historical_holdings_sec.xlsx") as writer:
        summary.to_excel(writer, sheet_name="Snapshots", index=False)
        holdings.to_excel(writer, sheet_name="Holdings", index=False)

    write_summary(summary, holdings)
    print(f"Saved {DATA_DIR / 'smh_historical_holdings_sec.csv'}")
    print(f"Saved {DATA_DIR / 'smh_historical_holdings_sec.xlsx'}")
    print(f"Saved {REPORT_DIR / 'smh_historical_holdings_sec_summary.md'}")


if __name__ == "__main__":
    main()
