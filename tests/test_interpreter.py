import sys
import types
from multiprocessing import Queue
from PIL import Image

# Create a dummy pyautogui module before importing Interpreter
calls = []
dummy_pyautogui = types.SimpleNamespace(
    press=lambda *args, **kwargs: calls.append(("press", args, kwargs)),
    write=lambda *args, **kwargs: calls.append(("write", args, kwargs)),
    hotkey=lambda *args, **kwargs: calls.append(("hotkey", args, kwargs)),
    size=lambda: (800, 600),
    screenshot=lambda: Image.new("RGB", (1, 1))
)
sys.modules['pyautogui'] = dummy_pyautogui

from app.interpreter import Interpreter


def test_execute_function_press(monkeypatch):
    queue = Queue()
    interpreter = Interpreter(queue)
    interpreter.execute_function('press', {'key': 'enter'})
    assert calls[1][0] == 'press'
    assert calls[1][1][0] == 'enter'


def test_process_command_puts_status(monkeypatch):
    queue = Queue()
    interpreter = Interpreter(queue)
    monkeypatch.setattr(interpreter, 'execute_function', lambda *a, **kw: None)
    command = {'function': 'press', 'parameters': {'key': 'a'}, 'human_readable_justification': 'Test'}
    assert interpreter.process_command(command)
    assert queue.get() == 'Test'
