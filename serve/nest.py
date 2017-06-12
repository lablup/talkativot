"""
Super-simple telegram bot API test
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
import os
import logging
import zmq

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
timers = dict()

TALKATIVOT_DEV_MODE = int(os.environ.get('TALKATIVOT_DEV_MODE', '0'))
TALKATIVOT_TELEGRAM_TOKEN = str(os.environ.get('TALKATIVOT_TELEGRAM_TOKEN', ''))
TALKATIVOT_CONVERSATION_ADDR = os.environ.get('TALKATIVOT_PORT_5001_TCP', 'tcp://127.0.0.1:5001')

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello world!")

def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry. Cannot parse your message.")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def alarm(bot, job):
    """Function to send the alarm message"""
    chat_id = job.context.get('chat_id')
    text = job.context['text'] if 'text' in job.context else 'ping'
    bot.sendMessage(chat_id, text=text)

def test_separate_engine(bot, update):
    url = 'http://localhost:8000/conversation/' +str(update.message.chat_id)
    ctx = zmq.Context.instance()
    with ctx.socket(zmq.REQ) as msg_sock:
        msg_sock.connect(TALKATIVOT_CONVERSATION_ADDR)
        msg_request = Message(
            ('message', update.message.text),
        )
        msg_sock.send(msg_request.encode())
        if msg_sock.poll(5000) == 0:
            bot.sendMessage(chat_id=update.message.chat_id, text="No response has arrived.")
            return
        resp_data = msg_sock.recv()
        msg_response = Message.decode(resp_data)
        if msg_response['success'] == 1:
            bot.sendMessage(chat_id=update.message.chat_id, text=msg_response['message'])

def main():
    updater = Updater(token=TALKATIVOT_TELEGRAM_TOKEN)
    # job_queue = updater.job_queue
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
