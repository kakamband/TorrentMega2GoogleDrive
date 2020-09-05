import shutil, psutil
import signal
import pickle

from os import execl, path, remove
from sys import executable
import time

from telegram.ext import CommandHandler, run_async
from bot import dispatcher, updater, botStartTime
from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, delete


@run_async
def stats(update, context):
    currentTime = get_readable_time((time.time() - botStartTime))
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>Bot Uptime:</b> {currentTime}\n' \
            f'<b>Total disk space:</b> {total}\n' \
            f'<b>Terpakai:</b> {used}\n' \
            f'<b>Kosong:</b> {free}\n' \
            f'<b>CPU:</b> {cpuUsage}%\n' \
            f'<b>RAM:</b> {memory}%\n' \
            f'<b>Disk:</b> {disk}%'
    sendMessage(stats, context.bot, update)


@run_async
def start(update, context):
    LOGGER.info('UID: {} - UN: {} - MSG: {}'.format(update.message.chat.id,update.message.chat.username,update.message.text))
    if update.message.chat.type == "private" :
        sendMessage(f"Hey <b>{update.message.chat.first_name}</b>. Welcome to <b>ScupidC0des Bot. Contact: @scupidc0des</b>", context.bot, update)
    else :
        sendMessage("READY TO PARTY :)", context.bot, update)
    if not CustomFilters.authorized_user(update):
        sendMessage("Awwww..izin dulu dongg....", context.bot, update)


@run_async
def restart(update, context):
    restart_message = sendMessage("Restarting, Please wait!", context.bot, update)
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")


@run_async
def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


@run_async
def log(update, context):
    sendLogFile(context.bot, update)


@run_async
def bot_help(update, context):
    help_string_adm = f'''
/{BotCommands.StartCommand} <b>: Cek bot masih idup kaga</b>
/{BotCommands.MirrorCommand} <b>[url OR magnet_link]: Download terus diuploads</b>
/{BotCommands.TarMirrorCommand} <b>[url OR magnet_link]: Download & upload ke format .tar</b>
/{BotCommands.UnzipMirrorCommand} <b>[url OR magnet_link] : Unzip & Upload</b>
/{BotCommands.WatchCommand} <b>[link]: Yotube/other streaming service video</b>
/{BotCommands.TarWatchCommand} <b>[link]: Download video (Youtube, dll) & upload ke format .tar</b>
/{BotCommands.CloneCommand} <b>[link]: Salin Google Drive Folder</b>
/{BotCommands.CancelMirror} <b>: Balas ke command download</b>
/{BotCommands.CancelAllCommand} <b>: Batalkan semua proses</b>
/{BotCommands.StatusCommand} <b>: Lihat status downloads</b>
/{BotCommands.ListCommand} <b>[name]: Cari file di Google Drive Folder</b>
/{BotCommands.deleteCommand} <b>[link]: Hapus file di drive[HANYA PEMILIK YANG BISA]</b>
/{BotCommands.StatsCommand} <b>: Cek status server</b>
/{BotCommands.PingCommand} <b>: Check ping!</b>
/{BotCommands.RestartCommand} <b>: Restart bot[HANYA PEMILIK YANG BISA]</b>
/{BotCommands.AuthorizeCommand} <b>: Izinkan user[HANYA PEMILIK YANG BISA]</b>
/{BotCommands.UnAuthorizeCommand} <b>: Hapus izin[HANYA PEMILIK YANG BISA]</b>
/{BotCommands.AuthorizedUsersCommand} <b>: Cek user[HANYA PEMILIK YANG BISA]</b>
/{BotCommands.AddSudoCommand} <b>: Tambah padmin[HANYA PEMILIK YANG BISA]</b>
/{BotCommands.RmSudoCommand} <b>: Hapus admin[HANYA PEMILIK YANG BISA]</b>
/{BotCommands.LogCommand} <b>: Get log file[HANYA PEMILIK YANG BISAo]</b>

'''

    help_string = f'''
/{BotCommands.StartCommand} <b>: Cek bot masih idup kaga</b>
/{BotCommands.MirrorCommand} <b>[url OR magnet_link]: Download terus diuploads</b>
/{BotCommands.TarMirrorCommand} <b>[url OR magnet_link]: Download & upload ke format .tar</b>
/{BotCommands.UnzipMirrorCommand} <b>[url OR magnet_link] : Unzip & Upload</b>
/{BotCommands.WatchCommand} <b>[link]: Yotube video</b>
/{BotCommands.TarWatchCommand} <b>[link]: Download video (Youtube, dll) & upload ke format .tar</b>
/{BotCommands.CloneCommand} <b>[link]: Salin Google Drive Folder</b>
/{BotCommands.CancelMirror} <b>: Balas ke command download</b>
/{BotCommands.CancelAllCommand} <b>: Batalkan semua proses</b>
/{BotCommands.StatusCommand} <b>: Lihat status downloads</b>
/{BotCommands.ListCommand} <b>[name]: Cari file di Google Drive Folder</b>
/{BotCommands.StatsCommand} <b>: Show Stats of the machine</b>
/{BotCommands.PingCommand} <b>: Check ping!</b>

'''

    if CustomFilters.sudo_user(update) or CustomFilters.owner_filter(update):
        sendMessage(help_string_adm, context.bot, update)
    else:
        sendMessage(help_string, context.bot, update)


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("Restarted Successfully!")
        remove('restart.pickle')

    start_handler = CommandHandler(BotCommands.StartCommand, start)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling()
    LOGGER.info("Yeah am running!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)


main()
