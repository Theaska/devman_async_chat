import asyncio
import logging

from argument_parser import parser


args, _ = parser.parse_known_args()
MINECRAFT_CHATBOT_HOST = args.host  # 'minechat.dvmn.org'
MINECRAFT_CHATBOT_PORT = args.port  # 5050
LOG_FILE = args.history
# LOG_FILE = args.history
USER_TOKEN = "364ad4bc-0e18-11ee-ad76-0242ac110002"
NEW_LINE = '\n'
EXIT = 'exit'


logger = logging.getLogger(__name__)


async def login_user(
    writer: asyncio.StreamWriter,
    token: str
):
    await write_message(writer, msg=token)


async def write_message(writer: asyncio.StreamWriter, msg: str):
    logger.info(msg, extra={'msg_type': 'writer'})
    writer.write((msg+NEW_LINE+NEW_LINE).encode('UTF-8'))
    await writer.drain()


async def read_message(reader: asyncio.StreamReader):
    line = await reader.readline()
    line = line.decode()
    logger.info(msg=line, extra={'msg_type': 'reader'})
    print(line)


async def start_chat(host: str, port: str):
    chat_reader, chat_writer = await asyncio.open_connection(host, port)

    token = input('Введите токен пользователя: \n')
    await read_message(chat_reader)
    await write_message(chat_writer, token)
    await read_message(chat_reader)

    while True:
        msg = input('Введите сообщение или exit для выхода из чата: \n', )
        if msg.lower() == EXIT:
            chat_writer.close()
            await chat_writer.wait_closed()
            logger.info('Exit', extra={'msg_type': 'writer'})
            return
        await write_message(chat_writer, msg)
        await read_message(chat_reader)


if __name__ == '__main__':
    logging.basicConfig(
        filename='log.txt',
        level='INFO',
        format='%(levelname)s:%(msg_type)s:%(message)s'
    )
    asyncio.run(start_chat(MINECRAFT_CHATBOT_HOST, MINECRAFT_CHATBOT_PORT))