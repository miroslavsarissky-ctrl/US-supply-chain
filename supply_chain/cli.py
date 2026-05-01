import argparse
from .pipelines import seed_import, classify, export
from .db import init_db


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    p_seed = sub.add_parser("seed-import")
    p_seed.add_argument("--input", required=True)

    p_enrich = sub.add_parser("enrich")
    p_enrich.add_argument("target", choices=["identity", "sec", "nrc", "doe", "usaspending", "sam", "osha"])
    p_enrich.add_argument("--all", action="store_true")

    p_class = sub.add_parser("classify")
    p_class.add_argument("target", choices=["capabilities", "newcleo-relevance"])
    p_class.add_argument("--all", action="store_true")

    p_exp = sub.add_parser("export")
    p_exp.add_argument("target", choices=["dashboard-json", "excel"])
    p_exp.add_argument("--out", required=True)

    args = parser.parse_args()
    init_db()
    if args.cmd == "seed-import":
        seed_import.run(args.input)
    elif args.cmd == "classify":
        if args.target == "capabilities":
            classify.run_capabilities()
        else:
            classify.run_relevance()
    elif args.cmd == "export":
        if args.target == "dashboard-json":
            export.dashboard_json(args.out)
        else:
            export.excel_export(args.out)
    elif args.cmd == "enrich":
        # placeholder deterministic no-op in MVP
        return

if __name__ == "__main__":
    main()
