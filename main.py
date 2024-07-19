import os
import logging

import dotenv

import telellama


dotenv.load_dotenv()

logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.INFO)
logger = logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d [%(levelname)s] - %(name)s, %(funcName)s - %(message)s'
)

if __name__ == '__main__':
    telellama.run_bot(os.getenv('TELEGRAM_TOKEN'))