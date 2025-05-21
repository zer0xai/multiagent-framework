from scripts.core.translate import t


def test_translation_english(monkeypatch):
    monkeypatch.setenv("LANGUAGE", "en")
    assert (
        t("agent_created", agent_name="Test")
        == "Agent 'Test' created and integrated successfully."
    )


def test_translation_portuguese(monkeypatch):
    monkeypatch.setenv("LANGUAGE", "pt")
    result = t("agent_created", agent_name="Teste")
    assert "criado e integrado" in result


def test_translation_fallback(monkeypatch):
    monkeypatch.setenv("LANGUAGE", "xx")
    assert (
        t("agent_created", agent_name="Test")
        == "Agent 'Test' created and integrated successfully."
    )
