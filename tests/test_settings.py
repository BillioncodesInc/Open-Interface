import base64
import json
from pathlib import Path
from app.utils.settings import Settings

def test_save_and_load_settings(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    settings = Settings()
    data = {"api_key": "secret", "model": "gpt-4o"}
    settings.save_settings_to_file(data)
    loaded = Settings()
    result = loaded.get_dict()
    assert result["api_key"] == "secret"
    assert result["model"] == "gpt-4o"

    settings_file = tmp_path/".open-interface"/"settings.json"
    with open(settings_file) as f:
        raw = json.load(f)
    assert raw["api_key"] == base64.b64encode(b"secret").decode()
