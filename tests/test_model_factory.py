import os
import sys
import types

# Insert the application directory into path so imports work
sys.path.insert(0, os.path.abspath('app'))

# Stub out heavy external dependencies before importing the factory module. This
# avoids import errors when packages like ``openai`` or ``google`` are missing.
openai_stub = types.SimpleNamespace(
    OpenAI=object,
    ChatCompletion=object,
    types=types.SimpleNamespace(
        beta=types.SimpleNamespace(
            threads=types.SimpleNamespace(
                message=types.SimpleNamespace(Message=object)
            )
        )
    )
)
sys.modules.setdefault("openai", openai_stub)
sys.modules.setdefault("openai.types", openai_stub.types)
sys.modules.setdefault("openai.types.beta", openai_stub.types.beta)
sys.modules.setdefault("openai.types.beta.threads", openai_stub.types.beta.threads)
sys.modules.setdefault(
    "openai.types.beta.threads.message", openai_stub.types.beta.threads.message
)

google_stub = types.SimpleNamespace(
    genai=types.SimpleNamespace(
        types=types.SimpleNamespace(SafetySetting=object, HarmCategory=object)
    )
)
sys.modules.setdefault("google", google_stub)
sys.modules.setdefault("google.genai", google_stub.genai)
sys.modules.setdefault("google.genai.types", google_stub.genai.types)

from models import factory

def test_model_factory_creates_correct_models(monkeypatch):
    monkeypatch.setattr(factory, "GPT4o", lambda *args, **kwargs: "gpt4o")
    monkeypatch.setattr(factory, "GPT4v", lambda *args, **kwargs: "gpt4v")
    monkeypatch.setattr(factory, "Gemini", lambda *args, **kwargs: "gemini")

    assert factory.ModelFactory.create_model("gpt-4o") == "gpt4o"
    assert factory.ModelFactory.create_model("gpt-4-vision-preview") == "gpt4v"
    assert factory.ModelFactory.create_model("gemini-pro") == "gemini"
