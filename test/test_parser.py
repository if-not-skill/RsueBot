import sys
import asyncio
import logging

from parser import Parser


log = logging.getLogger(__name__)


class Config:
    def __init__(self):
        self.url = "https://rsue.ru/raspisanie/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }


async def main(args):
    config = Config()

    parser = Parser(
        url=config.url,
        headers=config.headers)
    await parser.start_parsing()


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
    asyncio.run(main(sys.argv[1:]))