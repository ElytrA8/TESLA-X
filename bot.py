from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
import sys, asyncio, os, logging, time, subprocess
import pexpect as pe

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
SESSION = os.environ.get('SESSION')
sfuser = os.environ.get('sfuser') or None
sfpass = os.environ.get('sfpass') or None

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

phoneError = '\nERROR: The Phone No. entered is INVALID' \
             '\n Tip: Use Country Code along with number.' \
             '\n or check your phone number and try again !'
try:
    os.mkdir('downloads')
except:
    print(f'{os.getcwd()}/downloads already exists!')

bot = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

bot_verison = 0.2

uptime = time.time()

help_list = []

async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time

@bot.on(events.NewMessage(outgoing=True, pattern="^.(start|on)$"))
async def on(event):
    from platform import python_version
    from telethon import __version__, version
    bot_time = await get_readable_time(time.time() - uptime)
    await event.delete()
    msg = (
    '\tuservanced\n'
    '`uservanced is up and ready`!\n'
    f'`🤖 bot_verison`       {bot_verison} 🤖\n'
    f'`⏱️ bot_uptime`         {bot_time} ⏱️\n'
    f'`🐍 python_version`     {python_version()} 🐍\n'
    f'`💬 telethon_version`   {version.__version__} 💬\n'
    f'`🛠️ loaded_modules`      {len(help_list)}  🛠️)\n')
    await bot.send_file(event.chat_id, 'https://telegra.ph/file/92a69b23614ed0122bb47.mp4', caption=msg)
help_list.append(
'`on/start`:\n checks the bot stats\n usage: `.on`\n\n'
)

@bot.on(events.NewMessage(outgoing=True, pattern=r"^.die$"))
async def die(event):
    await event.edit("`ok. i'm gonna commit deletus now`")
    sys.exit(1)

@bot.on(events.NewMessage(outgoing=True, pattern='^.download(?: |$)(.*)'))
async def download(event):
    url = event.pattern_match.group(1)
    if url == None:
        await event.edit('`enter a URL!!!`')
        return
    home_folder = os.getcwd()
    os.chdir('downloads')
    await event.edit('`download started!`')
    file = f'aria2c {url}'
    process = await asyncio.create_subprocess_shell(file, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    await event.edit(f'{stdout.decode()}')
    os.chdir(home_folder)
help_list.append('`.download:`\n download files from direct links.\n usage: .download <url>\n\n')

@bot.on(events.NewMessage(outgoing=True, pattern='^\.gsi(?: |$|\n)(.*)'))
async def gsi(event):
    url = event.pattern_match.group(1).split(" ", 1)[0]
    rom_name = str(event.pattern_match.group(1).split(" ", 1)[1])
    path = os.getcwd()
    if not url:
        await event.edit('bruh. enter needed paramters')
        return
    queue = []
    queue.append(url)
    if queue[0] != None:
        await event.edit(f'`added {rom_name} to queue`')
    try:
        os.mkdir('working')
    except:
        print("file already exists. skipping..")
    os.chdir('working')
    if os.path.exists(f'{path}/working/output.txt'):
        await event.edit('`old output spotted!\n deleting...`')
        os.remove('output.txt')
    gsi_making = f'sudo chmod -R 0777 ErfanGSIs;cd ErfanGSIs;sudo bash setup.py;sudo ./url2GSI.sh {queue.pop(0)} {rom_name}'
    output = await asyncio.create_subprocess_shell(
    gsi_making, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await output.communicate()
    out = str(stdout.decode()) + str(stderr.decode())
    if len(out) > 4096:
        with open('output.txt', 'w+') as a:
            a.write(out)
            await bot.send_file(
            'output.txt',
            event.chat_id,
            reply_to=event.id,
            caption='output was too big so it was sent as a file'
            )
            os.remove('output.txt')
    else:
        await event.respond(str(out))
    await event.edit('\n gsi zipping started')
    os.chmod(f'{path}ErfanGSIs/output', 0o777)
    os.chdir(f'{path}ErfanGSIs/output')
    zip_images = f'sudo zip {rom_name}-GSI-AB.zip *-AB-*.img; sudo zip {rom_name}-GSI-Aonly.zip *-Aonly-*.img;rm -rf *.img'
    await asyncio.create_subprocess_shell(
    zip_images, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    await event.edit('zip uploading started')
    upload = f'./transfer wet *-AB-*.zip | grep Download >> AB_download.txt;./transfer wet *-Aonly-*.zip | grep Download >> Aonly_download.txt;touch info.txt;cp *AB*.txt info.txt'
    await asyncio.create_subprocess_shell(
    upload, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    with open('AB_download.txt') as ab:
        os.environ['down_ab'] = ab.read()
    with open('Aonly_download.txt') as aon:
        os.environ['aonly'] = aon.read()
    with open('info.txt') as inf:
        os.environ['info'] = inf.read()
    message = (
        f"`{rom_name} - GSI`\n"
        "information about this gsi\n"
        f"`{info}`\n\n"
        f"Downloads!\n"
        f"AB: [Download AB](down_ab)\n"
        f"Aonly: [Download Aonly](Aonly)\n"
        f"thanks to:\n"
        f"Erfan Abdi and cytolytic\n\n"
        )
    bot.send_message(
    event.chat_id, message)
    os.chdir(path)
    # clean up
    clean = f'rm -rf *.txt; rm -rf *.zip;rm -rf working'
    await asyncio.create_subprocess_shell(
    clean, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
help_list.append("`ErfanGSIs`:\n build ErfanGSIs easily and build it anywhere!\n usage: .gsi <rom_url> <rom_name>\n\n")


from random import randint
@bot.on(events.NewMessage(outgoing=True, pattern='^.ping$'))
async def ping(event):
    from datetime import datetime
    start = datetime.now()
    await event.edit('PONG!')
    end = datetime.now()
    speed = (end - start).microseconds / 1000
    await event.edit(f'PONG!\n `{speed}ms`')
help_list.append('`Ping!\n Pong!`')

@bot.on(events.NewMessage(outgoing=True, pattern='^.retard$'))
async def retard(event):
    from random import randint
    replied = await event.get_reply_message()
    sender = replied.sender
    await event.edit(f'{sender.username} is {randint(1, 100)}% retarded!')

@bot.on(events.NewMessage(outgoing=True, pattern=r"^.die$"))
async def die(event):
    await event.edit("`ok. i'm gonna commit deletus now`")
    sys.exit(1)

@bot.on(events.NewMessage(outgoing=True, pattern="^.speedtest$"))
async def speed(event):
    import speedtest
    owo = speedtest.Speedtest()
    await event.edit('speed test strated...')
    try:
        await event.edit('getting the best server...')
        owo.get_best_server()
        await event.edit('testing the download')
        owo.download()
        await event.edit('testing the upload')
        owo.upload()
        owo.results.share()
        proc = test.results.dict()
    except Exception as e:
        await event.edit(e)
    await event.edit(
    f"`{speed_convert(proc['download'])}\n"
    f"{speed_convert(proc['upload'])}`\n"
    f"{proc['ping']}`\n"
    )
def speed_convert(size):
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "Mb/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

@bot.on(events.NewMessage(outgoing=True, pattern='^.spam (.*)'))
async def spam(event):
    counter = int(event.pattern_match.group(1).split(" ", 1)[0])
    spam_message = str(event.pattern_match.group(1).split(" ", 1)[1])
    if spam_message == None:
        await event.edit("give me a message to spam!!")
        return
    elif counter == None:
        await event.edit("give a number to spam!!")
        return
    else:
        await event.delete()
        for i in range(counter):
            await event.respond(f"{spam_message}")

help_list.append(
'`spam`:\n this module can be used to spam your friends.\n usage: .spam <number to spam> <the message you want to spam>\n\n'
)

@bot.on(events.NewMessage(outgoing=True, pattern='^\.sh(?: |$|\n)(.*)'))
async def shell(sh):
    comm = sh.pattern_match.group(1)
    user = 'uservanced'
    if not comm:
        await sh.edit(f"you didnt specify what command to excute! \n")
        return
    exec = await asyncio.create_subprocess_shell(
    comm, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await exec.communicate()
    output = str(stdout.decode()) + str(stderr.decode())
    if len(output) > 4000:
        try:
            with open("doingurmom.txt", 'w') as out:
                out.write(output)
                await bot.send_file(
                'doingurmom.txt', sh.chat_id, reply_to=sh.id,
                caption="output was too big so it was sent as a file"
                )
                remove('doingurmom.txt')
                return
        except:
            await sh.edit("and error has occured")
            return
    print(f'~{user}:$ {comm}\n {output}')
    await sh.edit(f"`~{user}:$ {comm}\n {output}`")

help_list.append(
'`sh:`\n shell bash command runner.\n usage: .sh <command>\n\n'
)


@bot.on(events.NewMessage(outgoing=True, pattern='^\.sf(?: |$|\n)(.*)'))
async def sf(event):
    file_dir = event.pattern_match.group(1)
    if  sfuser == None or sfpass == None:
        await event.edit("please enter ur sfuser/ pass")
        return
    elif sfdir == None:
        await event.edit('`no dir found!!`')
        return
    else:
        try:
            await event.edit('uploading failed')
            os.system("sh sf.sh")
            await event.edit('uploading completed!')
        except Exception as cock:
            await event.edit(f'uploading failed!\n logs:\n {cock}')
            return
help_list.append(
'`sf/sourceforge:`\n uploads the files u choose to sourceforge. \n usage: .sf <filename>\n\n '
)

@bot.on(events.NewMessage(outgoing=True, pattern='^\.transfer(?: |$|\n)(.*)'))
async def transfer(event):
    url = event.pattern_match.group(1)
    if not url:
        await event.edit('`bruh what am i supposed to upload?`')
        return
    upload = f'./transfer wet {url}'
    await event.edit(f'`uploading started for {url}`')
    process = await asyncio.create_subprocess_shell(
    upload, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    await event.edit(f'{stdout.decode()}')
help_list.append("`transfer`:\n upload files to we.tl \n usage: .transfer <url>\n\n")

@bot.on(events.NewMessage(outgoing=True, pattern='^.help(?: |$)(.*)'))
async def help(event):
    message = 'welcome to uservanced modules Helper!\n\n'
    for key in help_list:
         message += '¬'
         message += f'{key}'
         message += "\n"
    photo_help = 'https://telegra.ph/file/0429706d4cac9b035e07f.mp4'
    await event.delete()
    await bot.send_file(event.chat_id, photo_help, caption=message)
try:
    bot.start()
except PhoneNumberInvalidError:
    print(phoneError)
    sys.exit(1)
print("uservanced is now running!!")
bot.run_until_disconnected()
