import aminofix
from rich.console import Console
from rich.progress import track
from . import menu_configs

console = Console()

client = aminofix.Client()

def login():
    choice_is_made = False
    while choice_is_made == False:
        choice = menu_configs.login_menu()
        if choice == "1":
            sid = console.input("[bold red][GI][/bold red]SID >> ")
            try:
                client.login_sid(sid)
                choice_is_made = True
                return False
            except:
                console.print_exception(show_locals = False)
        elif choice == "2":
            email = str(console.input("[bold red][GI][/bold red]Email >> "))
            password = str(console.input("[bold red][GI][/bold red]Password >> "))
            try:
                client.login(email, password)
                choice_is_made = True
                return False
            except:
                console.print_exception(show_locals = False)
        elif choice == "0":
            choice_is_made = True
            return True
        else:
            console.print("[bold red][GI][/bold red]Please enter a number of option.")
            choice_is_made = False

def get_user_info():
    json = client.get_account_info().json
    sid = client.sid
    current_nickname = client.get_user_info(client.userId).nickname
    output = f'Uid: {json["uid"]}\nTwitter ID: {json["twitterID"]}\nApple ID: {json["appleID"]}\nFacebook ID: {json["facebookID"]}\nGoogle ID: {json["googleID"]}\nPhone number: {json["phoneNumber"]}\nFirst Nickname: {json["nickname"]}\nCurrent Nickname: {current_nickname}\nAmino ID: {json["aminoId"]}\nEmail: {json["email"]}\nIcon link: {json["icon"]}\nSid: {sid}\n\n'
    return [output, sid]

def get_user_communities():
    comInfo = []
    userInfo = []
    coms = []
    com = client.sub_clients()
    for step, comId, name in zip(track(range(len(com.comId)), description = "[bold red][GI][/bold red]Getting communities info..."), com.comId, com.name):
        comInfo.append((f'ComId: {comId} -- Title: {name}'))
        coms.append(comId)
        sub_client = aminofix.SubClient(comId, profile=client.profile)
        user_info = sub_client.get_user_info(client.userId)
        username = user_info.nickname
        icon = user_info.icon
        media_list = user_info.mediaList
        images = []
        if str(media_list) == "None":
            images.append("No links.")
        else:
            for i in range(len(media_list)):
                image_link = media_list[i][1]
                images.append(image_link)
        reputation = user_info.reputation
        level = user_info.level
        followers = user_info.followersCount
        following = user_info.followingCount
        comments = user_info.commentsCount
        posts = user_info.postsCount
        join_time = user_info.createdTime
        modified_time = user_info.modifiedTime
        content = user_info.content
        userInfo.append(f'  Username: {username}\n  Icon Link: {icon}\n  Media List: {images}\n  Reputation: {reputation}\n  Level: {level}\n  Followers: {followers}\n  Following: {following}\n  Posts: {posts}\n  Comments: {comments}\n  Joined on {join_time}\n  Last modified {modified_time}\n  Content:\n  {content}\n\n\n')
    console.print("[bold red][GI][/bold red][green]Done![/green]")
    return [comInfo, coms, userInfo]

def get_user_chats():
    coms = get_user_communities()[1]
    comsChats = []
    privateChats = []
    with console.status(f'[bold green]Getting chats of {client.get_user_info(client.userId).nickname}...'):
        for i in coms:
            chatIds = []
            com_chat = []
            p_com_chat = []
            sub_client = aminofix.SubClient(comId = i, profile = client.profile)
            chat = sub_client.get_chat_threads()
            for chatName, chatId, host, userId, chatType in zip(chat.title, chat.chatId, chat.author.nickname, chat.author.userId, chat.type):
                if chatType in [0, 1]:
                    if chatIds.count(chatId) >= 1:
                        pass
                    else:
                        if str(chatName) == "None":
                            p_com_chat.append(f'  ChatId: {chatId} -- UserId: {userId} -- Username: {host}')
                        else:
                            p_com_chat.append(f'  ChatId: {chatId} -- UserId: {userId} -- Title: {chatName} -- Username: {host}')     
                else:
                    com_chat.append((f'  ChatId: {chatId} -- Title: {chatName}'))
            com_chat.sort()
            comsChats.append(com_chat)
            p_com_chat.sort()
            privateChats.append(p_com_chat)
            console.log(f'Got chats in {client.get_community_info(i).name}.')
    chatInfo = {com: comsChats[i] for i, com in zip(range(len(coms)), coms)}
    privateChatInfo = {com: privateChats[i] for i, com in zip(range(len(coms)), coms)}
    console.print("[bold red][GI][/bold red][green]Done![/green]")
    return [chatInfo, privateChatInfo]

def get_chat_log(comId, chatId, n):
    authors = []
    contents = []
    ids = []
    userIds = []
    timestamp = []
    output = []
    sub_client = aminofix.SubClient(comId, profile = client.profile)
    if sub_client.get_chat_thread(chatId).type == 0:
        output_header = f'Messages in private chat with {sub_client.get_chat_thread(chatId).author.nickname}.\n'
    else:
        output_header = f'Messages in {sub_client.get_chat_thread(chatId).title}.\n'
    message_list = sub_client.get_chat_messages(chatId, n)
    for messageId, username, userId, content, time in zip(message_list.messageId, message_list.author.nickname, message_list.author.userId, message_list.content, message_list.createdTime):
        if str(content) == 'None':
            pass
        else:
            authors.append(username)
            contents.append(content)
            ids.append(messageId)
            userIds.append(userId)
            timestamp.append(time)
    messages = {ids[i]: [authors[i], contents[i], userIds[i], timestamp[i]] for i in range(len(ids))}
    ids.reverse()
    for i in ids:
        output.append(f'  {messages[i][2]} -- [{messages[i][3]}]{messages[i][0]}: {messages[i][1]}\n')
    return [output, output_header]

def get_wallet_info(l, n):
    output = []
    coins = client.get_wallet_info().totalCoins
    history = client.get_wallet_history(l, n)
    with console.status(f'[bold green]Getting wallet info...'):
        for i, ip, t_id, t_coins in zip(range(len(history.originCoins)), history.sourceIp, history.transanctionId, history.originCoins):
            try:
                path_raw = history.extData[i]["objectDeeplinkUrl"].split("/")
                comId = path_raw[2].removeprefix("x")
                blogId = path_raw[4]
                com_title = client.get_community_info(comId).name
                title = history.extData[i]["description"]
                output.append(f'  User {history.extData[i]["subtitle"]} in {com_title}: {t_coins} ac.\n  TransactionId: {t_id} -- Ip: {ip}\n  BlogId: {blogId} -- Title: {title}.\n\n')
            except:
                title = history.extData[i]["description"]
                output.append(f'  Transaction: {t_coins} ac.\n  TransactionId: {t_id} -- Ip: {ip}\n  Title: {title}.\n\n')
    return [coins, output]

def get_comments(comId, l, n):
    sub_client = aminofix.SubClient(comId, profile = client.profile)
    comments = sub_client.get_wall_comments(client.userId, "newest", l, n)
    output_header = f'Wall comments in {client.get_community_info(comId).name}:\n'
    output = []
    for json in comments.json:
        output.append(json)
    return [output_header, output]

def account_output():
    account_info = get_user_info()[0]
    file = open("account_info.txt", "w", encoding="utf8") 
    file.write(account_info) 
    file.close()
    print(account_info)

def communities_info_output():
    file = open("communities_list.txt", "w", encoding="utf8") 
    user_communities = get_user_communities()
    coms_info, profile_info = user_communities[0], user_communities[2]
    for i, j in zip(coms_info, profile_info):
        file.write(f'{i}\n')
        file.write(f'{j}\n')
        print(i)
    file.close()

def chats_output(): 
    user_chats = get_user_chats()
    chats, p_chats = user_chats[0], user_chats[1]

    file = open("public_chats_list.txt", "w", encoding="utf8")
    for comId in list(chats.keys()):
        file.write(f'\nChats in {client.get_community_info(comId).name}, {comId}:\n')
        if chats[comId] == []:
            file.write("  No chats found.\n")
        else:
            for line in chats[comId]:
                file.write(f'  {line}\n')
    file.close()

    file = open("private_chats_list.txt", "w", encoding="utf8")
    for comId in list(p_chats.keys()):
        file.write(f'\nPrivate chats in {client.get_community_info(comId).name}, {comId}:\n')
        if p_chats[comId] == {}:
            file.write("  No chats found.\n")
        else:
            for line in p_chats[comId]:
                file.write(f'  {line}\n')
    file.close()

def chat_log_output():
    comId = str(console.input("[bold red][GI][/bold red]Community Id >> "))
    chatId = str(console.input("[bold red][GI][/bold red]Chat Id >> "))
    n = int(console.input("\nHow many messages you want to gather?\n\nPlease notice that you may get less messages than you've had specified\ndue to the fact that this option is ignoring non-text messages.\nMaximum amount of messages is 100.\n\n[bold red][GI][/bold red] >> "))
    chat_log = get_chat_log(comId, chatId, n)
    file = open("chat_log.txt", "w", encoding="utf8")
    file.write(chat_log[1])
    for line in chat_log[0]:
        file.write(line)
    file.close()

def wallet_output():
    yes = ['y', 'yes', 'yes.']
    no = ['n', 'no', 'no.']
    q = ['q', 'quit', 'quit.']
    while True:
        choice = console.input("\nDo you want to get info of more than 100 transactions? [Y/N/Q]\n\n[bold red][GI][/bold red] >> ")

        if choice.lower() in yes:
            n = int(console.input("\nThis may take a while.\nPlease specify how many transactions you want to gather info of.\nUse only such numbers as 200, 300, 400, etc.\n\n[bold red][GI][/bold red] >> "))

            coins = get_wallet_info(0, 0)[0]
            wallet_list = []

            for i in range(0, n, 100):
                wallet = get_wallet_info(i, 100)[1]
                wallet_list.append(wallet)

            file = open("wallet_info_large.txt", "w", encoding="utf8")
            file.write(f'{client.get_user_info(client.userId).nickname} has {coins} ac.\n\n')

            cnt = 0
            for i in wallet_list:
                i.sort()
                for line in i:
                    cnt+=1
                    file.write(line)
            file.close()
            break

        elif choice.lower() in no:
            n = int(console.input("\nPlease specify how many transactions you want to gather info of.\nRemember, 100 is a maximum for this option.\n\n[bold red][GI][/bold red] >> "))

            coins, wallet = get_wallet_info(0, 0)[0], get_wallet_info(0, n)[1]

            file = open("wallet_info.txt", "w", encoding="utf8")
            file.write(f'{client.get_user_info(client.userId).nickname} has {coins} ac.\n\n')

            cnt = 0
            for line in wallet:
                cnt+=1
                file.write(line)
            file.close()
            break

        elif choice.lower() in q:
            break

        else:
            console.print("[bold red][GI][/bold red]Please enter Y or N, if you wish to go back, enter Q.")

def comments_output():
    comId = str(console.input("[bold red][GI][/bold red]Community Id >> "))
    i = int(console.input("[bold red][GI][/bold red]How many comments to gather >> "))
    comments = get_comments(comId, 0, i)
    file = open("comments_info.txt", "w", encoding="utf8")
    file.write(comments[0])
    for line in comments[1]:
        links = []
        if str(line["mediaList"]) == "None":
            links.append('None')
        else:
            for i in line["mediaList"]:
                links.append(i[1])
        file.write(f'[{line["modifiedTime"]}]{line["author"]["nickname"]}: {line["content"]}\nMedia List: {str(links)}\n\n')
        if line["subcommentsCount"] == 0:
            file.write("  No subcomments.\n\n")
        else:
            line["subcommentsPreview"].reverse()
            for i in line["subcommentsPreview"]:
                sublinks = []
                if str(i["mediaList"]) == "None":
                    sublinks.append('None')
                else:
                    for j in i["mediaList"]:
                        links.append(j[1])
                file.write(f'- - - -[{i["modifiedTime"]}]{i["author"]["nickname"]}: {i["content"]}\n  Media List: {str(sublinks)}\n\n')
        file.write("\n\n\n\n")
    file.close()
    