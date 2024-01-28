import os
import json
from datetime import datetime

# Colourise command line output
class background:
    Black= '\033[48;5;0m'
    Red= '\033[48;5;1m'
    Green= '\033[48;5;2m'
    Yellow= '\033[48;5;3m'
    Blue= '\033[48;5;4m'
    Magenta= '\033[48;5;5m'
    Cyan= '\033[48;5;6m'
    White= '\033[48;5;7m'

class foreground:
    white='\033[39m'
    black='\033[30m'
    yellow='\033[93m'
    pink='\033[95m'
    red='\033[91m'
    green='\033[92m'
    cyan='\033[96m'
    purple='\033[94m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'

reset_color="\033[0m"




filename = "sleep.json"

if not os.path.exists(filename):
    with open(filename, "w") as f:
        json.dump([], f)




def time_to_seconds(time_str):
    time_object = datetime.strptime(time_str, "%H:%M")
    return time_object.hour * 3600 + time_object.minute * 60

def calculate_time_difference(logoff, bed):
    time1_seconds = time_to_seconds(logoff)
    time2_seconds = time_to_seconds(bed)
    return abs(time2_seconds - time1_seconds)

def convert_seconds_to_hours_minutes(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return hours, minutes, seconds




def print_schema(entry, i):
    logoff = entry["logoff"]
    bed = entry["bed"]
    logon = entry["logon"]

    time_difference_seconds = calculate_time_difference(logoff, bed)
    hours, minutes, _ = convert_seconds_to_hours_minutes(time_difference_seconds)

    print(f"{foreground.purple}{i}: | {foreground.green}{logoff}  | {foreground.pink}{bed} ({hours}h:{minutes}m) | {foreground.cyan}{logon}{reset_color}")







def show_menu():
  print(foreground.yellow + "\nSELECT A NUMBER OPTION BELOW AND THEN PRESS ENTER:")
  
  print(foreground.cyan + "VIEW[1] " + foreground.pink + "SEARCH[2] " + foreground.purple + "ADD[3] " + foreground.green + "EDIT[4] " + foreground.red + "DELETE[5] " + foreground.white + "EXIT[0]")





def view_data():
  with open(filename, "r") as f:
    temp = json.load(f)
  
  print(f"{background.White}{foreground.black}id | Logoff |      Bed       | Logon{reset_color}")

  i = 0
  for entry in temp:
    print_schema(entry, i)
    i +=1





def search_data():
    search_word = input("Enter search word:\n\n" + foreground.green).lower()
    with open(filename, "r") as f:
        temp = json.load(f)

    found_results = False  # A flag to check if any results were found

    for i, entry in enumerate(temp):
        logoff = entry["logoff"]
        bed = entry["bed"]
        logon = entry["logon"]

        if search_word in logoff or search_word in bed or search_word in logon:
            print(f"\n{background.Red}{foreground.purple}id {i}:{reset_color}\n\n{foreground.green}{logoff}\n\n{foreground.pink}{bed}\n\n{foreground.cyan}{logon}\n")
            found_results = True

    if not found_results:
        print(foreground.red + "No results found.")




  
def delete_data():
  #view_data()
  new_data = []
  with open(filename, "r") as f:
    temp = json.load(f)
    data_length = len(temp) -1

  delete_option = input(f"{foreground.green}HINT:{foreground.pink} If you don't know the id, try SEARCH before using this DELETE option.\n {foreground.cyan} \nSelect the ID number to delete from 0-{data_length} (or press the ENTER key to ABORT)\n")
  
  if not delete_option:
    return
  
  i = 0
  confirm = input(f"{background.Red}Press Y to DELETE or N to Abort {reset_color}\n")
  
  if confirm == "Y":
    for entry in temp:
      if i == int(delete_option):
        pass
        i +=1
      else:
        new_data.append(entry)
        i +=1
    with open(filename, "w") as f:
      json.dump(new_data, f, indent=4)
    print(f"{foreground.green}Deleted successfully")
  else:
      print(f"{foreground.yellow}No problem. Try another option:")





def edit_data():
  #view_data()
  new_data = []
  with open(filename, "r") as f:
    temp = json.load(f)
    data_length = len(temp) -1

  edit_option = input(foreground.green + "HINT: " + foreground.pink + "If you don't know the id, try SEARCH before using this EDIT option.\n" + foreground.cyan + f"\nSelect the ID number to edit from 0-{data_length} (or press the Enter key followed by N to abort)\n")
  i = 0
  confirm = input(foreground.red + "Do you wish to proceed? (Y/N) ")
  if confirm == "Y":
    for entry in temp:
      if i == int(edit_option):
        print_schema(entry, i)
        logoff = input(f"New logoff (current: {entry['logoff']}): ").strip().lower() or entry['logoff']
        logoff = logoff.lower()
        bed = input(f"New bed (current: {entry['bed']}): ").strip().lower() or entry['bed']
        bed = bed.lower()
        logon = input(f"New logon (current: {entry['logon']}): ").strip().lower() or entry['logon']
        logon = logon.lower()
        new_data.append({"logoff": logoff, "bed": bed, "logon": logon})
        i +=1
      else:
        new_data.append(entry)
        i +=1
    with open(filename, "w") as f:
      json.dump(new_data, f, indent=4)
  else:
    print(foreground.yellow + "No problem. Try another option:")





def add_data():
  item_data = {}
  with open(filename, "r") as f:
    temp = json.load(f)
  item_data["logoff"] = input("Logoff: ")
  item_data["bed"] = input("Bed: ")
  item_data["logon"] = input("Logon: ")
  
  temp.append(item_data)
  with open(filename, "w") as f:
    json.dump(temp, f, indent=4)





while True:
  show_menu()
  choice = input("\n")
  if choice == "1":
    view_data()
  elif choice == "2":
    search_data()
  elif choice == "3":
    add_data()
  elif choice == "4":
    edit_data()
  elif choice == "5":
    delete_data()
  elif choice == "0":
    break
  else:
    print(foreground.red + "Incorrect option, please try again.")
