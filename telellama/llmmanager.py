import time
import queue
import threading
import logging
from typing import Callable, Optional
from dataclasses import dataclass

from . import utils


logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    text: str

@dataclass(kw_only=True)
class LLMRequestBase:
    request_text: str
    response: Optional[LLMResponse] = None

class LLMBusyError(Exception):
    def __init__(self, wait_time: int, *args: object) -> None:
        super().__init__(*args)
        self.wait_time = wait_time

class LLMManager:
    def __init__(self, on_response: Callable) -> None:
        self._q = queue.Queue()
        self._is_busy = threading.Event()
        self._rq_time = -1
        self._work_thread = threading.Thread(target=self._run_llm_loop)
        self._work_thread.isDaemon = True
        self._work_thread.start()

        self._user_callback = on_response

    def _run_llm_loop(self):
        while True:
            request = self._q.get()

            self._call_llm(request)
            
    def _call_llm(self, request: LLMRequestBase):
        self._is_busy.set()

        logger.debug(f'Sent request to llm {repr(request)}')

        self._rq_time = utils.time_now_ms()
        time.sleep(3)
        request.response = LLMResponse('Test response')
        self._user_callback(request)

        self._is_busy.clear()

    def get_response(self, request: LLMRequestBase) -> dict:
        if self._is_busy.is_set():
            raise LLMBusyError(utils.time_now_ms() - self._rq_time)
        
        self._q.put(request)