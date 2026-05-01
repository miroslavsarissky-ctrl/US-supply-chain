from supply_chain.pipelines.export import ALLOWED

def test_allowed_grades():
    assert "unverified" not in ALLOWED
    assert "regulatory_record" in ALLOWED
