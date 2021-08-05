import telebot
import datetime
import time

### HELP TEXT ------------------------------------------------------------------------|
'''
User Available Commands:
    1. /poll
    2. /stats
    3. /start
    4. /help
    5. /groups
   
Developer Commands: #NOTE: ONLY @Parvat_R and @Rohithaditya are allowed for these comands:
    1. /showIds
    2. /botlogs
'''
### MAIN VARS ------------------------------------------------------------------------|
'''
THESE ARE THE IMPORTANT VARS FOR POLL BOT
'''
BOT_TOKEN = '8s858s85s:4g44g4646g464g4g448' # YOUR BOT TOKEN HERE GET FROM @BotFather
API_HASH = '85df55s5s5s55s55a4' # YOUR API HASH GET FROM my.telegram.org
API_ID = '1234567' # YOUR API ID GET FROM my.telegram.org
CHAT_ID = '-1001'# YOUR PRIVATE GROUP TO VIEW LOGS OR ERROR
USERNAME = 'Rohithaditya' # YOUR USERNAME THIS IS MANDTORY

### ABOVE MAIN VARS -------------------------------------------------------------------|
bot = telebot.TeleBot(token=BOT_TOKEN)

@bot.message_handler(commands=['showIds'])
def showIds(message):
    try:
        if message.from_user.username in ['Parvat_R', 'Rohithaditya', USERNAME]:
            file = open('joined_groups.txt', 'r ')
            bot.send_document(message.chat.id, file)
            file.close()

    except Exception as error:
        bot.send_message(CHAT_ID, str(error))

@bot.message_handler(commands=['stats', 'groups'])
def stats(message):
    try:
        if message.from_user.username in['Parvat_R','Rohithaditya', USERNAME]:
            print('Sending Stats To Owner')
            with open('joined_groups.txt', 'r') as file:
                group_ids = []
                for line in file.readlines():
                    for group_id in line.split(' '):
                        group_ids.append(group_id)
                        no_of_polls = len(group_ids)
                        no_of_groups = len(list(set(group_ids)))
                group_ids.clear()
                bot.reply_to(message, f'Number of polls Maded: {no_of_polls}\nNo of groups bot has been added: {no_of_groups}')
                file.close()
        else:
                        bot.reply_to(message, f'Sorry {message.from_user.username}! You Are Not Allowed To Use This Command,')
    except Exception as error:
                            bot.send_message(CHAT_ID, f'Hi Devs!!\nHandle This Error plox\n{error}')
                            try:
                                group_ids.clear()
                            except:
                                pass
                            bot.reply_to(message, f'An error occurred!\nError: {error}')
                            bot.send_message(CHAT_ID, f'An error occurred!\nError: {error}')
                            bot.send_document(CHAT_ID, '{message}')

@bot.message_handler(commands=['botlogs'])
def ViewTheLogsFile(message):
    try:
        if message.from_user.username in ['Parvat_R', 'Rohithaditya', USERNAME]:
            print('Owner Asked For The Logs!')
            file = open('POLL_LOGS.txt', 'r')
            bot.send_document(message.chat.id, file, timeout=60, disable_notification=True)
            file.close()
            print('Logs Sent To Owner')
        else:
            bot.reply_to(message, f'Sorry {message.from_user.username}! You Are Not Allowed For This Command,')
    except Exception as error:
        bot.reply_to(message, f'Error: {error}')

def poller(message):
    MSG = message
    try:
        #### AN IMPORTANT PROCESS TO SAVE ALL THE USES IN THE POLL_LOGS.txt FILE
        try:
            file1 = open('joined_groups.txt', 'a')
            file = open('POLL_LOGS.txt', 'a')
        except FileNotFoundError as fnfe:
            file = open('POLL_LOGS.txt', 'x')
            file.close()
            file = open('POLL_LOGS.txt', 'a')
        text_to_add_in_log_file = f'''<pollbot command = log>
Username: {message.from_user.username}
User Id : {message.from_user.id}
Command : {message.text}
OWNER : {USERNAME}
Chat Id : {message.chat.id}
ChatType: {message.chat.type}
GroupUserName: {message.chat.username}
Date    : {datetime.datetime.now()}

<split info_end = True>Command Over</split>

'''
        file1.write(f' {message.chat.id}')
        file1.close()
        file.write(text_to_add_in_log_file)
        file.close()
        ### PROCESS DONE!
        #The complete command is cut on '|'
        text_arr = message.text.split('|')

        #The splitted text are inserted in the commands list
        #Always the first command or commands[0] will be '/poll
        commands = []

        #Adding splitted text in commands:
        for cmd in text_arr:
            #ws_re_text = white space removed command text
            ws_re_text = cmd.strip()
            commands.append(ws_re_text)

        #Now the creations of commands for poll:
        question     = commands[1]
        options      = []
        multi_answer = False
        open_period  = None
        explanation  = None
        disable_noti = False
        delete_msg   = False

        #Adding the options:
        opt = commands[2].split(',')
        for op in opt:
            nop = op.replace('<.>', ',')
            options.append(nop.strip())

        #Now checking the **kwargs in the command line
        if len(commands) > 3:
            for cmd in commands[3:]:
                main_cmd = cmd.strip().split('=')
                
                if main_cmd[0].strip() in ['ma', 'multi_answer', 'm_a', 'mul_ans']:
                    multi_answer = main_cmd[1].strip()
                    
                if main_cmd[0].strip() in ['op', 'open_period', 'o_p', 'ope_per']:
                    open_period = main_cmd[1].strip()

                if main_cmd[0].strip() in ['ex', 'explanation', 'expl', 'e_x']:
                    explanation = main_cmd[1].strip()

                if main_cmd[0].strip() in ['dn', 'd_n', 'disable_notification', 'dis_not']:
                    disable_noti = main_cmd[1].strip()
                
                if main_cmd[0].strip() in ['dm', 'd_m', 'delete_message', 'del_msg']:
                    delete_msg = True
        
        if delete_msg:
            bot.delete_message(message.chat.id, message.id)
        #The main function
        return bot.send_poll(
            message.chat.id,
            question,
            options,
            allows_multiple_answers= multi_answer,
            explanation            = explanation ,
            open_period            = open_period ,
            disable_notifications  = disable_noti)
    
    except IndexError:
        return bot.reply_to(message, f'''Lol!!! You Have Entered Wrong Cmds
The format of the command should be:

`/poll | your question | option1, option2, more options | **kwargs`

But What You Sent Me was🤣🤣😂😂😁

{message.text}

Which is invalid.
For more help use: /help
or contact us at: @venilabots1
''')
    except Exception as error:
        bot.send_message(CHAT_ID,f'''Error From Poll Bot!

Error  :: {error}

--------------------------------

Command:: {message.text}

--------------------------------

UserDetails: {message.from_user}

--------------------------------

Date   :: {message.date}

--------------------------------

The Complete Detail:
{message}


''')
        
        return bot.reply_to(message, f'''An Unexpected Error Occured!
Error::  {error}
The error was informed to @venilabots''')
        
        

@bot.message_handler(commands=['poll'])
def pollNow(message):
    poller(message)

@bot.message_handler(commands=['help'])
def helper(message):
    return bot.reply_to(message, f'''My Name Defines Who Am I. 
    What Can I Do?
    1. Create polls
    2. Unlimited Polls
    3. Vast options

 Main Commands:
    /help
    /alive
    /poll

Functions:
/help:
    See the Help Text

/alive:
    Check if the bot is running or not

/poll:
    Create polls.

How To Create Polls:

use:
/poll | Your Question | Option1, Option2, Option3, more_option | **kwargs
You can add As may options as you want. (minimum-1)

what is **kwargs?
**kwargs are the optional commands, that you can pass when necessary!
those are:
    multi_answer = True/False
        This enables or disables The multiple answer mode. By default It is False.
        example:
            /poll | This is my question | Ans1, Ans2 | multi_answer = True

    op = seconds
        This tells how many seconds will the poll will last.
        It might be 'op' or 'open_period'
        example:
            /poll | This is my question | Ans1, Ans2 | op = 60
            Now the poll will last for 60 seconds.

    dn = True/False
        This tells that the poll should be notified in the notifications of the
        group members. By Default it is True. It might be 'dn' or 'disable_notification'.
        example:
            /poll | This is my question | Ans1, Ans2 | dn = False

Did you know, you can use multiple optional commands or dont use it:
Example:
    1.
        /poll | Hi there | Hello, Good bye

    2.
        /poll | This will close in 10s | Nice, Bad | op = 10
        
    3.
        /poll | Hello | Hi, Bye, Hi dev, Bye human | ma = True | open_period = 50

Note:
    -Use ',' to split the options.
    -Every part is split by '|'.
    -To use ',' in option use: '<.>'

For more informations visit:
Official Site:
https://sprin-g-reen.github.io/
Telegram:
@venilabots
@venilabots1

Devs:
@Parvat_R
@Rohithaditya

Created with:
python,
pyTelegramBotAPI
''')


@bot.message_handler(commands=['alive'])
def alive(message):
    bot.reply_to(message, f'Hey {message.from_user.username}, Ready To Serve You')

'''err_count = 0 #Check for errors
while True:
    try:
        bot.polling()
    except FileNotFoundError as e:
        print(e)
        err_count +=1
        print(f'Error Number: {err_count}')
        if err_count == 10:
            break
'''
@bot.message_handler(commands=['start'])
def alive(message):
    bot.reply_to(message, f'Heya {message.from_user.username}, I am there to help you in polls. But this cmd is bit old try /help. SEE @VENILABOTS FOR MORE BOTS LIKE THIS')

err_count = 0 #Check for errors
while True:
    try:
        bot.polling()
    except FileNotFoundError as e:
        print(e)
        err_count +=1
        print(f'Error Number: {err_count}')
        if err_count == 10:
            break
"""
PLEASE KEEP CREDITS
"""
