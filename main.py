import os
import logging

import dotenv

import telellama


dotenv.load_dotenv()

logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.INFO)
logger = logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d [%(levelname)s] - %(name)s, %(funcName)s - %(message)s'
)

OLLAMA_HOST = 'http://ollama:11434'
MODEL_NAME = 'llama2-uncensored'
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


def main():
    llm_provider = telellama.StatelessOllamaLLMProvider(OLLAMA_HOST)
    llm_provider.pull_model(MODEL_NAME)

    llm_manager = telellama.LLMManager(llm_provider)
    telegram_bot = telellama.TelegramBot(TELEGRAM_TOKEN, llm_manager)
    llm_manager.set_on_response(telegram_bot.handle_llm_request_threadsafe)

    telegram_bot.run_bot()


if __name__ == '__main__':
    main()
    