from app.auth.entra.jwks import get_jwks

def test_jwks_fetch():
    jwks = get_jwks()
    print(jwks)

    assert "keys" in jwks
    assert isinstance(jwks["keys"], list)
    assert len(jwks["keys"]) > 0
    assert "kid" in jwks["keys"][0]
