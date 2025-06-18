from typing import Any

try:
    from anthropic import Anthropic
except Exception:  # anthopic might not be installed in environment
    Anthropic = None

class Claude:
    def __init__(self, model_name: str, api_key: str, context: str) -> None:
        if not api_key:
            raise ValueError("Anthropic API key is required to use Claude models.")
        if Anthropic is None:
            raise ImportError("anthropic package is required to use Claude models")
        self.model_name = model_name
        self.api_key = api_key
        self.context = context
        self.client = Anthropic(api_key=api_key)

    def get_instructions_for_objective(self, *args, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    def cleanup(self) -> None:
        pass
