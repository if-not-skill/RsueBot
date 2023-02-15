import sys
import logging

from bot.telegram_bot import start_bot

log = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s.%(msecs)03.0f] [%(name)17s] [pid:%(process)-5d] [tid:%(thread)0x] '
               '[%(filename)25s:%(lineno)-3d] %(levelname)-8s %(message)s ',
        datefmt='%Y-%m-%d %H:%M:%S',
        level='DEBUG',
        stream=sys.stdout
    )
    logging.getLogger('urllib3').setLevel('CRITICAL')

    log.info('Started')
    start_bot()
