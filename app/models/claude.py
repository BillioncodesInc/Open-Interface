import json
from typing import Any
from anthropic import Anthropic
from .model import Model
from ..utils.screen import Screen


class Claude(Model):
    def __init__(self, model_name, api_key, context):
        super().__init__(model_name, base_url="https://api.anthropic.com/v1/", api_key=api_key, context=context)
        # Anthropic client doesn't take base_url in this simple wrapper but our
        # Model base class expects one. We'll ignore base_url argument by
        # overriding client with Anthropic.
        self.client = Anthropic(api_key=api_key)

    def get_instructions_for_objective(self, original_user_request: str, step_num: int = 0) -> dict[str, Any]:
        data = self.format_user_request_for_llm(original_user_request, step_num)
        llm_response = self.client.messages.create(**data)
        return self.convert_llm_response_to_json_instructions(llm_response)

    def format_user_request_for_llm(self, original_user_request: str, step_num: int) -> dict[str, Any]:
        base64_img = Screen().get_screenshot_in_base64()
        request_data = json.dumps({
            "original_user_request": original_user_request,
            "step_num": step_num
        })
        messages = [
            {
                "role": "user",
                "content": self.context + request_data
            },
            {
                "role": "user",
                "content": {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64_img
                    }
                }
            }
        ]
        return {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": 800
        }

    def convert_llm_response_to_json_instructions(self, llm_response: Any) -> dict[str, Any]:
        llm_response_data = llm_response["content"][0]["text"].strip()
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
