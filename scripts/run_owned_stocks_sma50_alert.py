from pathlib import Path
import site
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
for vendor_dir in (".localdeps", ".deps", ".deps2", "vendor", "vendor_py314"):
    candidate = PROJECT_ROOT / vendor_dir
    if candidate.exists():
        site.addsitedir(str(candidate))

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.strategy_lab.owned_stocks_sma50_alert import main


if __name__ == "__main__":
    main()
