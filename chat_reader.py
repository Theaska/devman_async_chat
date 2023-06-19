import asyncio
import aiofiles
import datetime

from argument_parser import parser


args, _ = parser.parse_known_args()

MINECRAFT_CHATBOT_HOST = args.host  # 'minechat.dvmn.org'
MINECRAFT_CHATBOT_PORT = args.port  # 5000
LOG_FILE = args.history
USER_TOKEN = "364ad4bc-0e18-11ee-ad76-0242ac110002"


async def read_chat(host: str, port: str):
    reader, _ = await asyncio.open_connection(host=host, port=port)
    async with aiofiles.open(LOG_FILE, mode='a+') as file:
        while True:
            try:
                data = await reader.read(100)
                if not data:
                    break
                log_data = f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")} {data.decode()}'
                await file.write(log_data)
                print(data.decode())
            except Exception:
                continue


if __name__ == '__main__':
    asyncio.run(read_chat(MINECRAFT_CHATBOT_HOST, MINECRAFT_CHATBOT_PORT))