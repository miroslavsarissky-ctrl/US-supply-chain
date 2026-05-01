from datetime import datetime, date
from sqlmodel import SQLModel, Field
from typing import Optional

class Vendor(SQLModel, table=True):
    vendor_id: str = Field(primary_key=True)
    display_name: str
    legal_name: Optional[str] = None
    website: Optional[str] = None
    hq_city: Optional[str] = None
    hq_state: Optional[str] = None
    hq_country: Optional[str] = "US"
    sec_cik: Optional[str] = None
    uei: Optional[str] = None
    cage_code: Optional[str] = None
    sam_status: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EvidenceItem(SQLModel, table=True):
    source_id: str = Field(primary_key=True)
    vendor_id: str
    source_type: str
    source_title: str
    source_url: str
    source_date: Optional[date] = None
    claim_text: str
    evidence_snippet: str
    confidence_level: str

class Capability(SQLModel, table=True):
    capability_id: str = Field(primary_key=True)
    vendor_id: str
    capability_tag: str
    capability_basis: str
    confidence_level: str
    source_id: str
    review_status: str = "auto"

class NewcleoRelevanceTag(SQLModel, table=True):
    tag_id: str = Field(primary_key=True)
    vendor_id: str
    tag: str
    basis: str
    source_id: str
    review_status: str = "auto"

class PeerRelationship(SQLModel, table=True):
    relationship_id: str = Field(primary_key=True)
    vendor_id: str
    peer_company: str
    relationship_type: str
    source_id: str

class FederalAward(SQLModel, table=True):
    award_id: str = Field(primary_key=True)
    vendor_id: str
    recipient_name: str
    award_amount: float = 0
    awarding_agency: Optional[str] = None
    source_id: str
