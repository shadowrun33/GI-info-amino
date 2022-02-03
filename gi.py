import os
from main_functions import *
from menu import *
cls = lambda: os.system('cls' if os.name=='nt' else 'clear')
global return_to_menu
global option
return_to_menu = True
while True:
    if return_to_menu == True:
        menu = main_menu()
        option = menu[0]
        return_to_menu = menu[1]
        cls()
    elif option == "1":
        return_to_menu = login()
        cls()
        if return_to_menu == False:
            account_output()
            option = None
            cls()
    elif option == "2":
        return_to_menu = login()
        cls()
        if return_to_menu == False:
            communities_info_output()
            option = None
            cls()
    elif option == "3":
        return_to_menu = login()
        cls()
        if return_to_menu == False:
            chats_output()
            option = None
            cls()
    elif option == "4":
        return_to_menu = login()
        cls()
        if return_to_menu == False:
            chat_log_output()
            option = None
            cls()
    elif option == "5":
        return_to_menu = login()
        cls()
        if return_to_menu == False:
            comments_output()
            option = None
            cls()
    elif option == "6":
        return_to_menu = login()
        cls()
        if return_to_menu == False:
            wallet_output()
            option = None
            cls()
    else:
        cls()
        return_to_menu = True