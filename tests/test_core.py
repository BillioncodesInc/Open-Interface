import types
import os
import sys

# Ensure the application code is importable
sys.path.insert(0, os.path.abspath('app'))

# Stub external dependencies used during import
dummy_pyautogui = types.SimpleNamespace()
sys.modules.setdefault('pyautogui', dummy_pyautogui)
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
sys.modules.setdefault('openai', openai_stub)
sys.modules.setdefault('openai.types', openai_stub.types)
sys.modules.setdefault('openai.types.beta', openai_stub.types.beta)
sys.modules.setdefault('openai.types.beta.threads', openai_stub.types.beta.threads)
sys.modules.setdefault('openai.types.beta.threads.message', openai_stub.types.beta.threads.message)

google_stub = types.SimpleNamespace(
    genai=types.SimpleNamespace(types=types.SimpleNamespace(SafetySetting=object, HarmCategory=object))
)
sys.modules.setdefault('google', google_stub)
sys.modules.setdefault('google.genai', google_stub.genai)
sys.modules.setdefault('google.genai.types', google_stub.genai.types)

import core as core_module

class DummyInterpreter:
    def __init__(self, queue):
        self.calls = []

    def process_command(self, cmd):
        self.calls.append(cmd)
        return True

class DummyLLM:
    def __init__(self):
        self.instructions = {"steps": [{"function": "press", "parameters": {}}], "done": "ok"}

    def get_instructions_for_objective(self, *a, **kw):
        return self.instructions

    def cleanup(self):
        pass


def test_core_execute(monkeypatch):
    monkeypatch.setattr(core_module, 'Interpreter', lambda q: DummyInterpreter(q))
    monkeypatch.setattr(core_module, 'LLM', lambda: DummyLLM())
    core = core_module.Core()
    result = core.execute('req')
    assert result == 'ok'
    assert core.interpreter.calls == [{"function": "press", "parameters": {}}]
