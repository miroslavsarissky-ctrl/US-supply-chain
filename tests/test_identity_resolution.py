def normalize_domain(url: str) -> str:
    return url.replace("https://", "").replace("http://", "").split("/")[0].lower()

def test_domain_normalization():
    assert normalize_domain("https://Example.COM/a") == "example.com"
