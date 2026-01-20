import pytest
from app.utils.persona_generator import persona_generator

def test_generate_persona_us():
    """Test generating a persona for US (standard supported country)."""
    persona = persona_generator.generate("US")
    assert "name" in persona
    assert "phone" in persona
    # Check that phone number is in international format (starts with +1)
    # The new logic generates E.164-ish international format, e.g. +1 201 555 0123
    # Faker fallback might be different, but we expect phonenumbers to work for US.
    assert persona["phone"].startswith("+1")

def test_generate_persona_zw():
    """Test generating a persona for Zimbabwe (fallback country in Faker)."""
    persona = persona_generator.generate("ZW")
    assert "name" in persona
    assert "phone" in persona
    # Should start with +263
    assert persona["phone"].startswith("+263")

def test_generate_persona_va():
    """Test generating a persona for Vatican (fallback country in Faker)."""
    persona = persona_generator.generate("VA")
    assert "name" in persona
    assert "phone" in persona
    # Should start with +39 (Italy prefix used by Vatican)
    assert persona["phone"].startswith("+39")

def test_phone_randomization():
    """Test that generated phone numbers are random."""
    p1 = persona_generator.generate("ZW")
    p2 = persona_generator.generate("ZW")

    # Names might be the same (Faker en_US fallback), but verify phone numbers are different
    # (chance of collision is low but possible, but we retry if collision happens in real world tests, here we assume it works)
    assert p1["phone"] != p2["phone"]

def test_fallback_behavior():
    """Test fallback behavior for Antarctica (AQ) where phonenumbers example might be missing."""
    # AQ (Antarctica) often doesn't have a single country code or example number in phonenumbers lib
    persona = persona_generator.generate("AQ")
    assert "phone" in persona
    # We just expect a string, format depends on fallback (likely Faker en_US)
    assert isinstance(persona["phone"], str)
    assert len(persona["phone"]) > 0
