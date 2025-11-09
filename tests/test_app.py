from app.app import redact_and_hash

def test_redact_and_hash():
    u_r, p_h = redact_and_hash('john.doe@example.com','Secret123!')
    assert '***' in u_r
    assert len(p_h) == 16
