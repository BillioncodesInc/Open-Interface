import types
import os
import sys
import builtins
from pathlib import Path

# Ensure the application code is importable
sys.path.insert(0, os.path.abspath('app'))

# Stub openai dependency
openai_stub = types.SimpleNamespace(
    OpenAIError=type('OpenAIError', (), {}),
    ChatCompletion=object,
    OpenAI=object,
    types=types.SimpleNamespace(
        beta=types.SimpleNamespace(
            threads=types.SimpleNamespace(message=types.SimpleNamespace(Message=object))
        )
    ),
)
sys.modules['openai'] = openai_stub
sys.modules['openai.types'] = openai_stub.types
sys.modules['openai.types.beta'] = openai_stub.types.beta
sys.modules['openai.types.beta.threads'] = openai_stub.types.beta.threads
sys.modules['openai.types.beta.threads.message'] = openai_stub.types.beta.threads.message

google_stub = types.SimpleNamespace(genai=types.SimpleNamespace(types=types.SimpleNamespace(SafetySetting=object, HarmCategory=object)))
sys.modules['google'] = google_stub
sys.modules['google.genai'] = google_stub.genai
sys.modules['google.genai.types'] = google_stub.genai.types

# Stub pyautogui for Screen usage
dummy_pyautogui = types.SimpleNamespace(size=lambda: (1, 1), screenshot=lambda: None)
sys.modules['pyautogui'] = dummy_pyautogui
import importlib
import utils.screen as screen_module
importlib.reload(screen_module)

from app import llm as llm_module


class DummyModel:
    def __init__(self, *args, **kwargs):
        pass

    def cleanup(self):
        pass


def test_llm_init_loads_model_and_context(monkeypatch, tmp_path):
    context_file = tmp_path / 'context.txt'
    context_file.write_text('CTX')
    # Mock settings
    monkeypatch.setattr(llm_module.Settings, 'get_dict', lambda self: {
        'model': 'custom',
        'base_url': 'https://base/',
        'api_key': 'key'
    })
    monkeypatch.setattr(llm_module.ModelFactory, 'create_model', lambda *a, **k: DummyModel())
    # Redirect context file open
    real_open = builtins.open

    def fake_open(path, *args, **kwargs):
        if str(path).endswith('context.txt'):
            return real_open(context_file, *args, **kwargs)
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, 'open', fake_open)
    llm = llm_module.LLM()
    assert llm.model_name == 'custom'
    assert isinstance(llm.model, DummyModel)
    text = llm.read_context_txt_file()
    assert 'CTX' in text
