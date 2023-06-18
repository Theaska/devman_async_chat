import configargparse

parser = configargparse.ArgParser()
parser.add_argument('--host', type=str, required=True, help='Host of chat bot')
parser.add_argument('--port', type=str, required=True, help='Port of chat bot')
parser.add_argument('--history', type=str, required=True, help='File to store chat logs')