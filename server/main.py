import asyncio, websockets, json, os, colorama
from colorama import Fore

ws_port = 8001

async def handler(ws):
    while True:
        try:
            message2 = await ws.recv()
        except websockets.ConnectionClosedOK:
            break
        message = message2.split()
        cmd = message[0].lower()
        print(f"{Fore.LIGHTBLUE_EX}[LOG] {Fore.RESET}Got the following packet -> {Fore.LIGHTRED_EX}{ws.remote_address[0]}")
        print(f"{Fore.LIGHTBLUE_EX}[PAC] {Fore.RESET}{message2}")
        if cmd == "login":
            if len(message) == 3:
                with open('users.txt', 'r') as f:
                    lines = f.readlines()
                    ok = False
                    for line in lines:
                        line = line.replace('\n', '').split(';')
                        if (line[0].lower() == message[1].lower() and line[1] == message[2]):
                            await ws.send('AUTHORIZED')
                            ok = True
                    if not ok:
                        await ws.send("NOT AUTHORIZED")
        if cmd == "data":
            if len(message) == 3:
                with open('users.txt', 'r') as f:
                    lines = f.readlines()
                    ok = False
                    for line in lines:
                        line = line.replace('\n', '').split(';')
                        if (line[0].lower() == message[1].lower() and line[1] == message[2]):
                            data = f"""RANK {line[2]}
TIMELEFT 27"""
                            await ws.send(data)
        if cmd == "mcsearch":
            datasend=""
            if len(message) == 4:
                with open('users.txt', 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.replace('\n', '').split(';')
                        if (line[0].lower() == message[1].lower() and line[1] == message[2]):
                            ok = False
                            for file in os.listdir('dbs'):
                                if file.split('.')[-1] == "json":
                                    with open('dbs/'+file, 'r') as f:
                                        for line in f.readlines():
                                            line = line.replace('\n', '').replace('},', '}')
                                            if (line == "[" or line == "]"):
                                                pass
                                            else:
                                                tmp = json.loads(line.replace("'", '"'))
                                                if tmp['name'].lower() == message[3].lower():
                                                    with open('srvdict.txt', 'r') as f:
                                                        lines = f.readlines()
                                                        for line2 in lines:
                                                            line2 = line2.split(":")
                                                            if line2[0] == tmp['password']:
                                                                line = str(line).replace(tmp['password'], line2[1])
                                                    datasend+=file.replace('.json', '')+" "+ line +"&&&"
                                                    ok = True
                            if not ok:
                                await ws.send("NOTHING")
                            await ws.send(datasend)
        if cmd == "addpass":
            with open('users.txt', 'r') as f:
                    lines = f.readlines()
                    ok = False
                    for line in lines:
                        line = line.replace('\n', '').split(';')
                        if (line[0].lower() == message[1].lower() and line[1] == message[2]):
                            with open('srvdict.txt', 'r') as f:
                                lines = f.readlines()
                                a = False
                                for line in lines:
                                    if message[3]+":"+message[4] in line:
                                        a = True
                                if not a:
                                    with open('srvdict.txt', 'a') as f:
                                        f.write(message[3]+":"+message[4]+"\n")

async def main():
    async with websockets.serve(handler, "", ws_port):
        print(Fore.GREEN+"WS sucessfully started on port: {ws_port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
