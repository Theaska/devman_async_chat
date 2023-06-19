import asyncio
import aiofiles
import datetime

from argument_parser import parser


args, _ = parser.parse_known_args()
MINECRAFT_CHATBOT_HOST = args.host  # 'minechat.dvmn.org'
MINECRAFT_CHATBOT_PORT = args.port  # 5050
LOG_FILE = args.history
# LOG_FILE = args.history
USER_TOKEN = "364ad4bc-0e18-11ee-ad76-0242ac110002"
NEW_LINE = '\n'
EXIT = 'exit'


async def login_user(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    token: str
):
    await write_message(reader, writer, msg=token)


async def write_message(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, msg: str):
    line = await reader.readline()
    print(line)

    writer.write((msg+NEW_LINE+NEW_LINE).encode('UTF-8'))
    await writer.drain()

    line = await reader.readline()
    print(line)


async def start_chat(host: str, port: str):
    chat_reader, chat_writer = await asyncio.open_connection(host, port)

    token = input('Введите токен пользователя: \n')
    await write_message(chat_reader, chat_writer, token)
    while True:
        msg = input('Введите сообщение или exit для выхода из чата: \n', )
        await write_message(chat_reader, chat_writer, msg)
        if msg.lower() == EXIT:
            chat_writer.close()
            await chat_writer.wait_closed()
            return


if __name__ == '__main__':
    asyncio.run(start_chat(MINECRAFT_CHATBOT_HOST, MINECRAFT_CHATBOT_PORT))