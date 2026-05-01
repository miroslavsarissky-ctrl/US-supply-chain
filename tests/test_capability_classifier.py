from supply_chain.pipelines.classify import CAP_RULES

def test_has_glovebox_rule():
    assert "glovebox" in CAP_RULES
