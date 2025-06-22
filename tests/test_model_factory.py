import os
import sys
sys.path.insert(0, os.path.abspath('app'))
from models import factory

def test_model_factory_creates_correct_models(monkeypatch):
    monkeypatch.setattr(factory, "GPT4o", lambda *args, **kwargs: "gpt4o")
    monkeypatch.setattr(factory, "GPT4v", lambda *args, **kwargs: "gpt4v")
    monkeypatch.setattr(factory, "Gemini", lambda *args, **kwargs: "gemini")

    assert factory.ModelFactory.create_model("gpt-4o") == "gpt4o"
    assert factory.ModelFactory.create_model("gpt-4-vision-preview") == "gpt4v"
    assert factory.ModelFactory.create_model("gemini-pro") == "gemini"
