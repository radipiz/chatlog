import socket
from datetime import datetime
from config import CHANNEL

sock = socket.socket()
sock.connect(('irc.chat.twitch.tv', 6667))
sock.send(f"NICK justinfan0\n".encode('utf-8'))
for chan in CHANNEL:
    sock.send(f"JOIN {chan}\n".encode('utf-8'))

lastAlert = 0


def parse_chat(resp):
    resp = resp.rstrip().split('\r\n')
    for line in resp:
        if "PRIVMSG" in line:
            user = line.split(':')[1].split('!')[0]
            channel = get_channel(line)
            msg = line.split(':', maxsplit=2)[2]
            datestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            line = f'{datestr} {channel} {user}: {msg}'
        print(line)


def get_channel(line: str) -> str:
    indicator = 'PRIVMSG'
    left_cut = line[line.index('PRIVMSG') + len(indicator) + 1:]
    return left_cut[:left_cut.index(':') - 1]


while True:
    response = sock.recv(2048).decode('utf-8')

    if response.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))

    elif len(response) > 0:
        parse_chat(response)
