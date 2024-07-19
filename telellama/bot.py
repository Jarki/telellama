import asyncio
import logging
import functools as ft
from dataclasses import dataclass

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, Application

from . import llmmanager as llm


logger = logging.getLogger(__name__)

@dataclass(kw_only=True)
class LLMRequestTG(llm.LLMRequestBase):
    update: Update
    event_loop: asyncio.BaseEventLoop

def on_llm_response(request: LLMRequestTG) -> None:
    response_text = request.response.text
    update = request.update
    asyncio.run_coroutine_threadsafe(update.message.reply_text(response_text), request.event_loop)

llm_mgr = llm.LLMManager(on_llm_response)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    request = LLMRequestTG(request_text=update.message.text, update=update, event_loop=asyncio.get_event_loop())

    try:
        llm_mgr.get_response(request)
    except llm.LLMBusyError as e:
        await update.message.reply_text(f'Waiting for llm response ({e.wait_time}ms)')
        return

    await update.message.reply_text('Sent a request to llm. Now wait')

def run_bot(token: str) -> Application:
    app = ApplicationBuilder().token(token).build()

    app.add_handler(MessageHandler(filters=None, callback=hello))

    app.run_polling()