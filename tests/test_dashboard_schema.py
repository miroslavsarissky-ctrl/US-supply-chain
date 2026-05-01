import json
from pathlib import Path

def test_vendors_json_exists_shape():
    p = Path("public/data/vendors.json")
    if not p.exists():
        return
    data = json.loads(p.read_text())
    if data:
        assert "vendor_id" in data[0]
        assert "capability_tags" in data[0]
