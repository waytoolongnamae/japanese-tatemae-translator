import cli
import main


class DummyTranslator:
    def translate(self, input_text, level="business", fidelity="medium", context=None):
        return {
            "tatemae_text": "dummy",
            "intent": "neutral_polite",
            "confidence": 1.0,
            "detected_language": "en",
            "level": level,
            "fidelity": fidelity,
            "context": context
        }


def test_cli_main_quiet(monkeypatch, capsys):
    monkeypatch.setattr(cli, "JapaneseTatemaeTranslator", DummyTranslator)
    monkeypatch.setattr(cli.sys, "argv", ["cli.py", "-m", "hello", "--quiet"])
    cli.main()
    captured = capsys.readouterr()
    assert "dummy" in captured.out


def test_main_example_flow(monkeypatch):
    monkeypatch.setattr(main, "JapaneseTatemaeTranslator", DummyTranslator)
    main.main()
