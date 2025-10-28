import argparse
from pipeline import run_pipeline, normalize_region_filter

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--regions", type=str, default="", help='Comma-delimited region keys; e.g. "GA,Grand Rapids, MI"')
    ap.add_argument("--sources", type=str, default="config/sources.yaml", help="Path to sources.yaml")
    args = ap.parse_args()
    run_pipeline(normalize_region_filter(args.regions), args.sources)
