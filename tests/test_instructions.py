"""Persona and entrypoint smoke checks (no LiveKit session, no API keys)."""

from instructions import GREETING_INSTRUCTIONS, SUCCESS_BUD_INSTRUCTIONS


def test_instructions_are_french_vous() -> None:
    text = SUCCESS_BUD_INSTRUCTIONS.lower()
    assert "vous vouvoyez" in text or "vouvoiement" in text
    assert "français" in text


def test_instructions_embed_cv_anchors() -> None:
    text = SUCCESS_BUD_INSTRUCTIONS
    assert "Fifty-five" in text
    assert "juillet 2023" in text
    assert "Cnam" in text
    assert "Adobe Analytics Developer" in text
    assert "Ironhack" in text
    assert "TOEIC 810" in text


def test_instructions_one_question_and_scorecard() -> None:
    text = SUCCESS_BUD_INSTRUCTIONS
    assert "UNE seule question" in text
    assert "Correctness" in text
    assert "Depth" in text
    assert "Structure" in text
    assert "Role fit" in text
    assert "Evidence" in text
    assert "0 à 5" in text


def test_instructions_allowlist_and_humility() -> None:
    text = SUCCESS_BUD_INSTRUCTIONS
    assert "GA4" in text
    assert "Piano" in text
    assert "IAB TCF" in text
    assert "Simo Ahava" in text
    assert "je ne sais pas" in text
    assert "70" in text


def test_instructions_forbid_out_of_scope() -> None:
    text = SUCCESS_BUD_INSTRUCTIONS.lower()
    assert "ne contactez aucun employeur" in text
    assert "api" in text
    assert "trading" in text


def test_greeting_is_single_question() -> None:
    assert "UNE seule" in GREETING_INSTRUCTIONS
    assert "français" in GREETING_INSTRUCTIONS.lower()


def test_agent_module_exports_persona() -> None:
    import agent as agent_mod

    assert agent_mod.AGENT_NAME == "success-bud-oral"
    assert agent_mod.GEMINI_LIVE_MODEL.startswith("gemini-2.5-flash-native-audio")
    assert "GOOGLE_APPLICATION_CREDENTIALS" not in agent_mod.SUCCESS_BUD_INSTRUCTIONS
    agent = agent_mod.SuccessBudOral()
    assert "Fifty-five" in agent.instructions
