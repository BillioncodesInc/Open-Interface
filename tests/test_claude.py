import os
import sys
from types import ModuleType
from unittest.mock import patch

# Provide a stub for pyautogui so importing Screen doesn't fail
sys.modules.setdefault('pyautogui', ModuleType('pyautogui'))
pil = ModuleType('PIL')
image_mod = ModuleType('PIL.Image')
image_mod.Image = type('Image', (), {})
pil.Image = image_mod
sys.modules.setdefault('PIL', pil)
sys.modules.setdefault('PIL.Image', image_mod)

# Ensure app package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.claude import Claude


def test_get_instructions_for_objective_parses_response():
    mock_response = {"content": [{"text": '{"steps": [], "done": "ok"}' }]}

    with patch('anthropic.resources.messages.messages.Messages.create', return_value=mock_response) as mock_create, \
         patch('app.models.claude.Screen.get_screenshot_in_base64', return_value='imgdata'):
        claude = Claude(model_name='claude-3', api_key='test', context='')
        result = claude.get_instructions_for_objective('do something', 0)

        assert result == {"steps": [], "done": "ok"}
        mock_create.assert_called_once()
