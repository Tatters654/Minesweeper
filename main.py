import ui
import logic
import datetime


def game_menu():
    while True:
        print(f"(S)tart game")
        print(f"(H)istory")
        print(f"(Q)uit")
        choice = input("Make your choice: ").strip().lower()
        if choice == "s": #start game
            start_game()
        elif choice == "q": #quit
            break
        elif choice == "h": #history
            pass
        else:
            print("The chosen feature is not available.")

def start_game(width, height, mines):
    #width = int(input("Input play area width: ")) # Ask for play area
    #height = int(input("Input play area height: "))
    #logic.state["mines"] = int(input("Input mine amount: ")) # Ask for mines amount
    logic.state["time_started"] = datetime.datetime.now() # Get current time
    logic.create_play_area(width, height)
    logic.place_mines( logic.state["mines"]) #Places mines from state values
    for list in logic.state["field"]:
        print(list)
    leveys = len(logic.state["field"][1])
    korkeus = len(logic.state["field"])
    print(f"leveys on {leveys} ja korkeus on {korkeus}")
    ui.main()
    pass


def print_statistics():
    pass


def print_history():
    pass

#game_menu()
logic.state["mines"] = 0
start_game(15, 10, 0)