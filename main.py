from datetime import datetime
from db import db_log, getCategories, getLogs, getSumLogs, SQL_Request 
from settings import DB_Settings

def inputCategory(DB_Settings: dict):
    categories = getCategories(DB_Settings)

    print("Categories:")
    for row in categories:
        print(f"{row[0]}. {row[1]}")

    return int(input("> "))

def newTask(DB_Settings: dict):
    categoryid = inputCategory(DB_Settings)
    
    print("Task description:")
    logdescription = input("> ")
    
    timeMenu = {
        "1": ("Get current time", datetime.now, dict()),
        "2": ("Manual time input", input, ("YYYY-MM-DD hh:mm:ss\n",))
    }
    
    logstarttime = printMenu(timeMenu, "Start Time:")

    logendtime = printMenu(timeMenu, "End Time:")

    db_log(DB_Settings, categoryid, logdescription, logstarttime, logendtime)

def printLogs(DB_Settings: dict):
    sqlConditions = []

    dateMenu = {
        "1": ("Get current date", datetime.now, dict()),
        "2": ("Manual date input", input, ("YYYY-MM-DD\n",)),
        "0": ("All", lambda *_: None, dict())
    }
    day = printMenu(dateMenu, "Select Day:")
    if day:
        sqlConditions.append(f"DATE(logs.logstarttime) = DATE('{day}')")

    categoryMenu = {
        "1": ("Manual category select", inputCategory, (DB_Settings,)),
        "0": ("All", lambda *_: None, dict())
    }
    categoryid = printMenu(categoryMenu, "Select Category:")
    if categoryid:
        sqlConditions.append(f"logs.categoryid = {categoryid}")
    
    sumMenu = {
        "1": ("Show all lines", lambda *_: False, dict()),
        "2": ("Show sum", lambda *_: True, dict())
    }
    showSum = printMenu(sumMenu, "Show sum?")

    if showSum:
        for row in getSumLogs(DB_Settings, sqlConditions):
            print(
                '{:.10}'.format(str(row[0])).ljust(10),
                row[1]
            )
    else:
        for row in getLogs(DB_Settings, sqlConditions):
            print(
                '{:.5}'.format(str(row[0])).ljust(5),
                '{:.20}'.format(str(row[1])).ljust(20),
                '{:.10}'.format(str(row[2])).ljust(10),
                '{:.10}'.format(str(row[3])).ljust(10),
                '{:.19}'.format(str(row[4])).ljust(19),
                '{:.19}'.format(str(row[5])).ljust(19)
            )

def printMenu(menu: dict, description: str = ""):
    while True:
        print()
        print(description)
        for key in menu:
            print(f"{key}) {menu[key][0]}")
        
        select = input("> ")
        value = menu.get(select)
        if not value:
            print("invalid key!")
            break

        print(value[0])
        return value[1](*value[2])  #Menu funtion execute 

if __name__ == "__main__":
    mainMenu = {
        "n": ("New Task", newTask, (DB_Settings,)),
        "g": ("Get Logs", printLogs, (DB_Settings,)),
        "e": ("exit", exit, dict())
    }

    while True:
        printMenu(mainMenu, "Menu:")
