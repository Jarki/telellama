import logging
from typing import Optional, Any, Protocol

import ollama


logger = logging.getLogger(__name__)


class LLMResponseProvider:
    def get_response(self, prompt):
        pass


class StatelessOllamaLLMProvider:
    def __init__(self, host: Optional[str] = None) -> None:
        if host is not None:
            self._client = ollama.Client(host)
        else:
            self._client = ollama

        self._model_name = None

    def pull_model(self, model_name: str):
        """
        model_name has to be one of https://ollama.com/library
        """
        logger.info(f'Pulling model {model_name}')
        self._model_name = model_name

        return self._client.pull(model_name)
    
    def get_response(self, prompt: str) -> dict[str, Any]:
        if self._model_name is None:
            raise ValueError('Please pull the model first')

        return self._client.generate(model=self._model_name, prompt=prompt)