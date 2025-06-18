"""Model wrapper for Anthropic Claude.

This module relies on the :mod:`anthropic` client to communicate with
Claude models.  The API key used for authentication should be supplied
via the constructor or the ``ANTHROPIC_API_KEY`` environment variable.
A screenshot of the user's screen is captured and attached to each
request so Claude can reason about the current UI state.
"""

import json
from typing import Any

from anthropic import Anthropic

from models.model import Model
from utils.screen import Screen


class Claude(Model):
    """Simple interface around the Anthropic Claude API.

    - ``get_instructions_for_objective`` sends the user's request and a
      screenshot to Claude and returns parsed instructions.
    - ``format_user_request_for_llm`` builds the message payload that is
      sent to the Claude API.
    - ``convert_llm_response_to_json_instructions`` extracts the JSON
      instructions from Claude's text response.
    """

    def __init__(self, model_name, base_url, api_key, context):
        super().__init__(model_name, base_url, api_key, context)
        self.client = Anthropic(api_key=api_key, base_url=base_url)

    def get_instructions_for_objective(self, original_user_request: str, step_num: int = 0) -> dict[str, Any]:
        message = self.format_user_request_for_llm(original_user_request, step_num)
        llm_response = self.send_message_to_llm(message)
        return self.convert_llm_response_to_json_instructions(llm_response)

    def send_message_to_llm(self, message):
        response = self.client.messages.create(
            model=self.model_name,
            messages=[{"role": "user", "content": message}],
            max_tokens=800,
        )
        return response

    def format_user_request_for_llm(self, original_user_request, step_num) -> str:
        base64_img: str = Screen().get_screenshot_in_base64()
        request_data: str = json.dumps({
            "original_user_request": original_user_request,
            "step_num": step_num,
        })
        message = (
            self.context
            + request_data
            + "\n\nHere is a screenshot of the user's screen encoded in base64:"\
            + base64_img
        )
        return message

    def convert_llm_response_to_json_instructions(self, llm_response) -> dict[str, Any]:
        llm_response_data = str(getattr(llm_response, "content", "")).strip()
        start_index = llm_response_data.find("{")
        end_index = llm_response_data.rfind("}")
        try:
            json_response = json.loads(llm_response_data[start_index:end_index + 1].strip())
        except Exception as e:
            print(f"Error while parsing JSON response - {e}")
            json_response = {}
        return json_response

    def cleanup(self):
        pass
