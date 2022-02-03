from rich.console import Console
from rich.table import Table

def main_menu():
    console = Console()
    table = Table(caption="script by https://github.com/shadowrun33", caption_style="italic yellow", caption_justify="right")
    ascii = """
 ██████  ██     
██       ██     
██   ███ ██     
██    ██ ██     
 ██████  ██ 
 """
    table.add_column("Options", header_style = "bold red", style = "green")
    table.add_column()
    table.add_row("[bold red][1][/bold red]Get account info.", "-- General account info + SID.")
    table.add_row("[bold red][2][/bold red]Get communities info.", "-- List of all the communities account is in + account info in these communities.")
    table.add_row("[bold red][3][/bold red]Get chats info.", "-- List of chats with chatIds account is in.")
    table.add_row("[bold red][4][/bold red]Get chat log.", "-- Chat log of specified chat via chatId, even if chat is blocked.")
    table.add_row("[bold red][5][/bold red]Get wall comments.", "-- List of all, even delited by user, wall comments of an account in specified community via comId.")
    table.add_row("[bold red][6][/bold red]Get wallet info.", "-- Wallet info + general transaction history, not sorted by date.")
    table.add_row("[bold red][7][/bold red]About.", "-- Learn more about the script.")
    table.add_row("[bold red][0][/bold red]Exit.")
    console.print(ascii, end="     ", style="bold red", highlight=False)
    console.print("[bold red]GET INFO[/bold red]")
    console.print(table)
    option = console.input("[bold red][GI][/bold red] Choose option. >> ")
    if option == "0": 
        exit()
    elif option == "7":
        about = """
This tool is needed if you're interested in 
getting something deleted from your account
or you've recieved access to someone's
account and you want to gather information
as fast as possible or if you've lost
access using email password login, but
still have SID. This script stores all the
info it gathered in txt files, so it is more
convinient to run it on computer. You don't
need any other scripts to get chatId/comId,
it will be written in txt files when chosen
to get communities info and chats info.

Enjoy!
        """
        console.print(about)
        console.input("[bold red][GI][/bold red]Press any key to continue...")
    return [option, False]

def login_menu():
    console = Console()
    table = Table()
    table.add_column("Login options.", header_style = "bold red", style = "green")
    table.add_column("", style = "italic white")
    table.add_row("[bold red][1][/bold red]Login using SID.", "-- Preferable if you have SID.")
    table.add_row("[bold red][2][/bold red]Login using email and password.", "-- Regular login.")
    table.add_row("[bold red][0][/bold red]Back.", "")
    console.print(table)
    option = console.input("[bold red][GI][/bold red]Choose option. >> ")
    return option