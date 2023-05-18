from core import Core
import os

core = Core()
text="""
Select option:
1 - Add new daemon manually
2 - Add new from file
3 - Remove daemon 
4 - Exit
"""

def getDaemonsFromFile():
    file = input("Enter path to file: ")
    with open(file,"r") as f:
        for line in f.readlines():
            daemon_data = line.replace("\n",'').split()
            core.addDaemon(daemon_data[0],daemon_data[1],daemon_data[2])
    print(f"Daemons from {file} added successfully")
def getDaemonsFromCLI():
    daemon_params = []
    daemon_params.append(input("Enter daemon name: "))
    daemon_params.append(input("Enter path to service file: "))
    daemon_params.append(input("Enter category: "))
    core.addDaemon(daemon_params[0],daemon_params[1],daemon_params[2])
    print("Daemon was added successfully")

def removeDaemon():
    name = input("Enter daemon name: ")
    try:
        os.remove(f"saved/{name}.pkl")
    except:
        print("Error")
    print(f'{name} was removed successfully')

print("Welcome to SystemD Remote Shell Manager")
while True:
    print(text)
    choose = int(input("Enter: "))
    if choose == 1:
        getDaemonsFromCLI()
    elif choose == 2:
        getDaemonsFromFile()
    elif choose == 3:
        removeDaemon()
    elif choose == 4:
        break
