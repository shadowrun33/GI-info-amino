import os
from configs import menu_configs
from configs import main_functions
global return_to_menu
global option
return_to_menu = True
cls = lambda: os.system('cls' if os.name=='nt' else 'clear')
while True:
    if return_to_menu == True:
        menu = menu_configs.main_menu()
        option = menu[0]
        return_to_menu = menu[1]
        cls()
    elif option == "1":
        return_to_menu = main_functions.login()
        cls()
        if return_to_menu == False:
            main_functions.account_output()
            option = None
            cls()
    elif option == "2":
        return_to_menu = main_functions.login()
        cls()
        if return_to_menu == False:
            main_functions.communities_info_output()
            option = None
            cls()
    elif option == "3":
        return_to_menu = main_functions.login()
        cls()
        if return_to_menu == False:
            main_functions.chats_output()
            option = None
            cls()
    elif option == "4":
        return_to_menu = main_functions.login()
        cls()
        if return_to_menu == False:
            main_functions.chat_log_output()
            option = None
            cls()
    elif option == "5":
        return_to_menu = main_functions.login()
        cls()
        if return_to_menu == False:
            main_functions.comments_output()
            option = None
            cls()
    elif option == "6":
        return_to_menu = main_functions.login()
        cls()
        if return_to_menu == False:
            main_functions.wallet_output()
            option = None
            cls()
    else:
        cls()
        return_to_menu = True
