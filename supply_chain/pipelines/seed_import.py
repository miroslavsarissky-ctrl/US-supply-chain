from pathlib import Path
import pandas as pd
from sqlmodel import Session
from ..db import init_db, engine
from ..models import Vendor, EvidenceItem


def run(input_path: str) -> int:
    init_db()
    p = Path(input_path)
    if p.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(p)
    else:
        df = pd.read_csv(p)
    required = {"vendor_id", "display_name"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    inserted = 0
    with Session(engine) as s:
        for row in df.to_dict("records"):
            v = Vendor(
                vendor_id=str(row["vendor_id"]),
                display_name=row["display_name"],
                legal_name=row.get("legal_name"),
                website=row.get("website"),
                hq_city=row.get("hq_city"),
                hq_state=row.get("hq_state"),
            )
            s.merge(v)
            ev = EvidenceItem(
                source_id=f"seed::{v.vendor_id}",
                vendor_id=v.vendor_id,
                source_type="Seed",
                source_title="Seed import",
                source_url="local://seed",
                claim_text="Seed vendor added",
                evidence_snippet=f"{v.display_name} from seed file",
                confidence_level="company_primary",
            )
            s.merge(ev)
            inserted += 1
        s.commit()
    return inserted
