"""Config sanity."""
from app.core.config import Persona, get_settings


def test_persona_enum():
    assert {p.value for p in Persona} == {"citizen", "founder", "practitioner"}


def test_settings_defaults():
    s = get_settings()
    assert s.openai_model_default
    assert s.openai_embedding_dim == 1536
    assert s.refusal_floor > 0


def test_origins_list_parses():
    s = get_settings()
    out = s.origins_list
    assert isinstance(out, list)
    assert all(isinstance(o, str) for o in out)
