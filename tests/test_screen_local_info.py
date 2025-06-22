import types
from PIL import Image
import sys

from app.utils import local_info


def setup_pyautogui(size=(1024, 768)):
    dummy_pyautogui = types.SimpleNamespace(
        size=lambda: size,
        screenshot=lambda: Image.new("RGB", (1, 1))
    )
    sys.modules['pyautogui'] = dummy_pyautogui
    from importlib import reload
    from app.utils import screen as screen_module
    reload(screen_module)
    return screen_module.Screen


def test_get_size_and_screenshot():
    Screen = setup_pyautogui()
    screen = Screen()
    assert screen.get_size() == (1024, 768)
    img = screen.get_screenshot()
    assert isinstance(img, Image.Image)


def test_local_info_attributes(monkeypatch):
    monkeypatch.setattr(local_info, 'locally_installed_apps', ['Foo.app'])
    monkeypatch.setattr(local_info, 'operating_system', 'Windows')
    assert isinstance(local_info.locally_installed_apps, list)
    assert isinstance(local_info.operating_system, str)
