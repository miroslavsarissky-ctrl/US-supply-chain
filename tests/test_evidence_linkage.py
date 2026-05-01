from supply_chain.models import Capability

def test_capability_has_source_id():
    fields = Capability.model_fields
    assert "source_id" in fields
