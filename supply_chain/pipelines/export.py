from pathlib import Path
import pandas as pd
from sqlmodel import Session, select
from ..db import engine
from ..models import Vendor, EvidenceItem, Capability, NewcleoRelevanceTag

ALLOWED = {"regulatory_record", "government_program", "sec_filing", "company_primary"}

def dashboard_json(out: str) -> None:
    outp = Path(out); outp.mkdir(parents=True, exist_ok=True)
    with Session(engine) as s:
        vendors = s.exec(select(Vendor)).all()
        evidence = [e for e in s.exec(select(EvidenceItem)).all() if e.confidence_level in ALLOWED]
        caps = s.exec(select(Capability)).all()
        tags = s.exec(select(NewcleoRelevanceTag)).all()
    vendors_payload = []
    for v in vendors:
        vc = [c.capability_tag for c in caps if c.vendor_id == v.vendor_id]
        vt = [t.tag for t in tags if t.vendor_id == v.vendor_id]
        vendors_payload.append({"vendor_id": v.vendor_id, "display_name": v.display_name, "capability_tags": vc, "newcleo_tags": vt})
    pd.DataFrame(vendors_payload).to_json(outp / "vendors.json", orient="records", indent=2)
    pd.DataFrame([e.model_dump(mode="json") for e in evidence]).to_json(outp / "evidence.json", orient="records", indent=2)
    pd.DataFrame([]).to_json(outp / "relationships.json", orient="records", indent=2)
    pd.DataFrame([]).to_json(outp / "programs.json", orient="records", indent=2)

def excel_export(out: str) -> None:
    with Session(engine) as s:
        vendors = [x.model_dump(mode="json") for x in s.exec(select(Vendor)).all()]
        evidence = [x.model_dump(mode="json") for x in s.exec(select(EvidenceItem)).all()]
        caps = [x.model_dump(mode="json") for x in s.exec(select(Capability)).all()]
        tags = [x.model_dump(mode="json") for x in s.exec(select(NewcleoRelevanceTag)).all()]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(out) as w:
        pd.DataFrame(vendors).to_excel(w, sheet_name="Vendors", index=False)
        pd.DataFrame(caps).to_excel(w, sheet_name="Capabilities", index=False)
        pd.DataFrame(tags).to_excel(w, sheet_name="newcleo Relevance", index=False)
        pd.DataFrame(evidence).to_excel(w, sheet_name="Sources", index=False)
