import asyncio
import logging
from dataclasses import dataclass

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, Application, filters, CommandHandler

from . import llmmanagers as llm


logger = logging.getLogger(__name__)

@dataclass(kw_only=True)
class LLMRequestTG(llm.LLMRequestBase):
    update: Update
    event_loop: asyncio.BaseEventLoop

class TelegramBot:
    def __init__(self, token: str, llm_manager: llm.LLMManager) -> None:
        self._bot_token = token
        self._llm_mgr = llm_manager

    def handle_llm_request_threadsafe(self, request: LLMRequestTG) -> None:
        logger.debug('Send llm response to user')
        response_text = request.response.text
        update = request.update
        asyncio.run_coroutine_threadsafe(update.message.reply_text(response_text), request.event_loop)

    async def _on_reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message.reply_to_message and update.message.reply_to_message.from_user.id != context.bot.id:
            return

        logger.debug('Reply to message')
        request = LLMRequestTG(request_text=update.message.text, update=update, event_loop=asyncio.get_event_loop())

        try:
            self._llm_mgr.get_response(request)
        except llm.LLMBusyError as e:
            await update.message.reply_text(f'Waiting for llm response ({e.wait_time}ms)')
            return

        await update.message.reply_text('Sent a request to llm. Now wait')

    async def _on_ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.debug('Respond to on_ping')
        await update.message.reply_text('Pong')

    def run_bot(self) -> Application:
        logger.info(f'Creating telegram bot with token {self._bot_token[:3]}...')
        app = ApplicationBuilder().token(self._bot_token).build()

        app.add_handler(MessageHandler(filters=filters.REPLY, callback=self._on_reply))
        app.add_handler(CommandHandler('ping', self._on_ping))

        logger.info('Telegram bot creating. Launching polling')
        app.run_polling()