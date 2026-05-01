from uuid import uuid4
from sqlmodel import Session, select
from ..db import engine
from ..models import Vendor, EvidenceItem, Capability, NewcleoRelevanceTag

CAP_RULES = {
    "glovebox": ["glovebox", "glove box"],
    "epc": ["epc", "engineering procurement construction"],
    "heavy_fabrication": ["heavy fabrication", "pressure vessel"],
}
REL_RULES = {
    "lfr_relevance": ["lead", "fast reactor", "lfr"],
    "fuel_fabrication": ["fuel fabrication", "fuel"],
}

def _text(ev: EvidenceItem) -> str:
    return f"{ev.claim_text} {ev.evidence_snippet}".lower()

def run_capabilities() -> int:
    count = 0
    with Session(engine) as s:
        vendors = s.exec(select(Vendor)).all()
        for v in vendors:
            evs = s.exec(select(EvidenceItem).where(EvidenceItem.vendor_id == v.vendor_id)).all()
            for ev in evs:
                txt = _text(ev)
                for tag, kws in CAP_RULES.items():
                    if any(k in txt for k in kws):
                        s.add(Capability(capability_id=str(uuid4()), vendor_id=v.vendor_id, capability_tag=tag,
                                         capability_basis=ev.claim_text, confidence_level=ev.confidence_level,
                                         source_id=ev.source_id))
                        count += 1
        s.commit()
    return count

def run_relevance() -> int:
    count = 0
    with Session(engine) as s:
        vendors = s.exec(select(Vendor)).all()
        for v in vendors:
            evs = s.exec(select(EvidenceItem).where(EvidenceItem.vendor_id == v.vendor_id)).all()
            for ev in evs:
                txt = _text(ev)
                for tag, kws in REL_RULES.items():
                    if any(k in txt for k in kws):
                        s.add(NewcleoRelevanceTag(tag_id=str(uuid4()), vendor_id=v.vendor_id, tag=tag,
                                                  basis=ev.claim_text, source_id=ev.source_id))
                        count += 1
        s.commit()
    return count
