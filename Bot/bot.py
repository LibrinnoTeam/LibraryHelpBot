import telegram
from telegram import InlineKeyboardMarkup as IKM
from telegram import ReplyKeyboardMarkup as RKM
from telegram import ReplyKeyboardRemove as RKR
from telegram import InlineKeyboardButton as IKB
from telegram.ext import MessageHandler as MHandler
from telegram.ext import Updater, CommandHandler, Filters, CallbackQueryHandler
from Bot.filter import *
from Bot import utils, func_data
from Bot.bot_modules.constructor import construct
import logging
import configs


# Class represents a Bot in Telegram
class LibraryBot:
    # Intialization of Bot
    # params:
    # token -- Token from BotFather
    # cntrl -- Bot's data base
    def __init__(self, token, cntrl):
        self.cntrl = cntrl
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        # self.logger = logging.getLogger(__name__)
        self.keyboard_dict = func_data.keyboard_dict
        self.types = func_data.lists["user_types"]
        self.pages = {}
        self.inline_key = {}
        self.location = {}

        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.add_handlers()

        # self.dispatcher.add_error_handler(self.error)

        self.updater.start_polling()
        self.updater.idle()

    def add_handlers(self):

        # User handlers
        self.dispatcher.add_handler(MHandler(WordFilter('Library🏤'), self.library))
        self.dispatcher.add_handler(MHandler(WordFilter('Search🔎'), self.cancel))
        self.dispatcher.add_handler(MHandler(WordFilter('My Books📚') & UserFilter(2), self.user_orders))
        self.dispatcher.add_handler(MHandler(WordFilter('Help👤') & UserFilter(2), self.cancel))

        f1 = (WordFilter('Books📖') | WordFilter('Journal Articles📰') | WordFilter('Audio/Video materials📼'))
        self.dispatcher.add_handler(MHandler(f1 & LocationFilter(self.location, 'library'), self.load_material))

        self.dispatcher.add_handler(MHandler(WordFilter('Registration📝') & UserFilter(0), self.registration))
        self.dispatcher.add_handler(MHandler(LocationFilter(self.location, 'reg') & Filters.text, self.reg_steps))
        self.dispatcher.add_handler(CommandHandler('get_admin', self.reg_admin, filters=UserFilter(2), pass_args=True))

        self.dispatcher.add_handler(MHandler(WordFilter('Cancel⤵️'), self.cancel))

        # Admin handlers
        self.dispatcher.add_handler(CommandHandler('get_key', utils.get_key, filters=UserFilter(3)))
        self.dispatcher.add_handler(MHandler(WordFilter("User management 👥") & UserFilter(3), self.user_manage))

        self.dispatcher.add_handler(MHandler(WordFilter("Confirm application📝") & UserFilter(3), self.confirm))
        self.dispatcher.add_handler(MHandler(WordFilter("Check overdue📋") & UserFilter(3), self.cancel))
        self.dispatcher.add_handler(MHandler(WordFilter("Show users👥") & UserFilter(3), self.show_users))
        self.dispatcher.add_handler(
            MHandler(LocationFilter(self.location, "user_modify") & UserFilter(3), self.modify_user))
        self.dispatcher.add_handler(MHandler(LocationFilter(self.location, "notice") & UserFilter(3), self.notice_user))

        self.dispatcher.add_handler(
            MHandler(WordFilter("Material management 📚") & UserFilter(3), self.mat_manage))
        self.dispatcher.add_handler(CallbackQueryHandler(self.call_back))

        self.dispatcher.add_handler(MHandler(WordFilter("Add material🗄") & UserFilter(3), self.add_doc))
        self.dispatcher.add_handler(
            MHandler(f1 & UserFilter(3) & LocationFilter(self.location, 'add_doc'), self.start_adding))
        self.dispatcher.add_handler(
            MHandler(LocationFilter(self.location, 'add_doc') & Filters.text, self.adding_steps))

    # Main menu
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def start(self, bot, update):
        user_type = self.cntrl.user_type(update.message.chat_id)
        keyboard = self.keyboard_dict[self.types[user_type]]

        bot.send_message(chat_id=update.message.chat_id, text="I'm bot, Hello",
                         reply_markup=RKM(keyboard, True))

    def call_back(self, bot, update):
        chat = update.callback_query.message.chat_id
        if chat in self.inline_key:
            key = self.inline_key[chat]
            if key == 'conf_flip':
                self.conf_flip(bot, update)
            elif key == 'user_flip':
                self.user_flip(bot, update)
            elif key == 'load_material':
                self.library_flip(bot, update)
            elif key == 'order_history':
                self.order_flip(bot, update)

    def check_overdue(self, bot, update):
        pass

    # Main menu of library
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def library(self, bot, update):
        self.location[update.message.chat_id] = ['library']
        bot.send_message(chat_id=update.message.chat_id, text="Choose type of material",
                         reply_markup=RKM(self.keyboard_dict["lib_main"], True))

    # Selected material
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def load_material(self, bot, update):
        chat = update.message.chat_id
        doc_type = func_data.analog[update.message.text]
        self.inline_key[chat] = 'load_material'
        n = 2
        docs = self.cntrl.get_all_doctype(doc_type)
        self.pages[chat] = [0, doc_type]

        if len(docs) == 0:
            bot.send_message(chat_id=chat, text="There are no " + doc_type + " in the library")
            return

        docs = [docs[i * n:(i + 1) * n] for i in range(len(docs) // n + 1) if i * n < len(docs)]
        text_message = ("\n" + "-" * 50 + "\n").join(
            ["{}) {} - {}".format(i + 1, doc['title'], doc["authors"]) for i, doc in enumerate(docs[0])])
        keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(docs[0]))]]
        keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
        update.message.reply_text(text=text_message + "\nCurrent page: {}/{}".format(str(1), len(docs)),
                                  reply_markup=IKM(keyboard))

    def library_flip(self, bot, update):
        query = update.callback_query
        chat = query.message.chat_id
        doc_type = self.pages[chat][1]
        n = 2
        docs = self.cntrl.get_all_doctype(doc_type)
        docs = [docs[i * n:(i + 1) * n] for i in range(len(docs) // n + 1) if i * n < len(docs)]
        max_page = len(docs) - 1
        if (query.data in ["prev", "next", 'cancel']) and (max_page or query.data == 'cancel'):
            if query.data == "next":
                if self.pages[chat][0] == max_page:
                    self.pages[chat][0] = 0
                else:
                    self.pages[chat][0] += 1
            if query.data == "prev":
                if self.pages[chat][0] == 0:
                    self.pages[chat][0] = max_page
                else:
                    self.pages[chat][0] -= 1

            text_message = ("\n" + "-" * 50 + "\n").join(
                ["{}) {} - {}".format(i + 1, doc['title'], doc["authors"]) for i, doc in
                 enumerate(docs[self.pages[chat][0]])])
            keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(docs[self.pages[chat][0]]))]]
            keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
            bot.edit_message_text(
                text=text_message + "\nCurrent page: {}/{}".format(self.pages[chat][0] + 1, len(docs)), chat_id=chat,
                message_id=query.message.message_id, reply_markup=IKM(keyboard))
        elif utils.is_int(query.data):
            k = int(query.data)
            doc = docs[self.pages[chat][0]][k]
            text = """Title: {title};\nAuthors: {authors}\n"""
            if doc_type == "book":
                text += """Description: {description}\nFree copy: {free_count}"""
            elif doc_type == "article":
                text += """Journal: {journal}\nIssue: {issue}\nDate: {date}\nFree copy: {free_count}"""
            elif doc_type == "media":
                text += """Free copy: {free_count}"""
            if self.cntrl.user_type(chat) == 2 and doc['free_count'] > 0:
                keyboard = [[IKB("Order the document", callback_data='order ' + query.data),
                             IKB("Cancel", callback_data='cancel')]]
            elif self.cntrl.user_type(chat) == 3:
                keyboard = [[IKB("Edit", callback_data='edit ' + query.data),
                             IKB("Delete", callback_data='del ' + query.data),
                             IKB("Cancel", callback_data='cancel')]]

            else:
                keyboard = [[IKB("Cancel", callback_data='cancel')]]

            bot.edit_message_text(text=text.format(**doc), chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
        elif query.data.split(" ")[0] == 'order':
            k = int(query.data.split(" ")[1])
            doc = docs[self.pages[chat][0]][k]
            status, report = self.cntrl.check_out_doc(chat, doc['id'], type_bd=doc_type)
            message = "Your order was successful.\nYou may take the document during library working hours." if status else "You already have this document"
            bot.edit_message_text(text=message, chat_id=chat, message_id=query.message.message_id)
        elif query.data.split(" ")[0] == 'modifier':
        k = int(query.data.split(" ")[1])
        self.material[chat] = docs[self.pages[chat][0]][k]
        self.inline_key[chat] = 'modifier'
        text = """"
                               Choose modified parameters: \n
                                \\authors \n  \\title \n  \\count \n  \\price \n  \\keywords \n   
                           """
        if doc_type == "book":
            text += " \\best_seller \n \\overview \n "
        elif doc_type == "article":
            text += """\\journal \n\\issue \n \\editor \n \\date \n"""
        elif doc_type == "media":
            pass
        self.modObj[chat] = ""
        keyboard = self.keyboard_dict['modMat']
        bot.send_message(chat_id=chat, text=text, reply_markup=RKM(keyboard, True))


def modifier(self, bot, update):
    text = update.message.text
    chatId = update.message.chat_id
    if text[:1] == '\\':
        self.modObj[chatId] = text[1:]
        bot.send_message(chatid=update.message.chat_id, text="Modifier " + text[1:])
    else:
        self.material[self.modObj[chatId]] = update.message.text
        bot.send_message(chatid=update.message.chat_id, text="Updated.")


def Apply(self, bot, update):
    self.cntrl.modify_document(self.modObj[update.message.chat_id])
    self.cancel(bot, update)

    def user_orders(self, bot, update):
        chat = update.message.chat_id
        self.inline_key[chat] = 'order_history'
        n = 2
        docs = self.cntrl.get_user_orders(chat)
        self.pages[chat] = 0

        if len(docs) == 0:
            bot.send_message(chat_id=chat, text="You have no orders")
            return
        docs = [docs[i * n:(i + 1) * n] for i in range(len(docs) // n + 1) if i * n < len(docs)]
        text_message = ("\n" + "-" * 50 + "\n").join(
            ["{}) {}, till {}".format(i + 1, doc['doc_dict']['title'], doc["time_out"]) for i, doc in
             enumerate(docs[0])])
        keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(docs[0]))]]
        keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
        update.message.reply_text(
            text=text_message + "\nCurrent page: {}/{}".format(self.pages[chat] + 1, len(docs)),
            reply_markup=IKM(keyboard))

    def order_flip(self, bot, update):
        query = update.callback_query
        chat = query.message.chat_id
        n = 2
        docs = self.cntrl.get_user_orders(chat)
        docs = [docs[i * n:(i + 1) * n] for i in range(len(docs) // n + 1) if i * n < len(docs)]
        max_page = len(docs) - 1
        if (query.data in ["prev", "next", 'cancel']) and (max_page or query.data == 'cancel'):
            if query.data == "next":
                if self.pages[chat] == max_page:
                    self.pages[chat] = 0
                else:
                    self.pages[chat] += 1
            if query.data == "prev":
                if self.pages[chat] == 0:
                    self.pages[chat] = max_page
                else:
                    self.pages[chat] -= 1
            text_message = ("\n" + "-" * 50 + "\n").join(
                ["{}) {}, till {}".format(i + 1, doc['doc_dict']['title'], doc["time_out"]) for i, doc in
                 enumerate(docs[self.pages[chat]])])
            keyboard = [[IKB(str(i + 1), callback_data=str(i)) for i in range(len(docs[self.pages[chat]]))]]
            keyboard += [[IKB("⬅", callback_data='prev'), IKB("➡️", callback_data='next')]]
            bot.edit_message_text(text=text_message + "\nCurrent page: {}/{}".format(self.pages[chat] + 1, len(docs)), chat_id=chat,
                                  message_id=query.message.message_id, reply_markup=IKM(keyboard))
        elif utils.is_int(query.data):
            k = int(query.data)
            doc = docs[self.pages[chat]][k]
            doc, time, time_out = doc.values()
            text = """
            Title: {}\nAuthors: {}\nAvailable till: {}
            """.format(doc['title'], doc['authors'], time_out)
            keyboard = [[IKB("Cancel", callback_data='cancel')]]

            bot.edit_message_text(text=text, chat_id=chat, message_id=query.message.message_id,
                                  reply_markup=IKM(keyboard))
            # elif query.data.split(" ")[0] == 'order':
            #     k = int(query.data.split(" ")[1])
            #     doc = docs[self.pages[chat][0]][k]
            #     status, report = self.cntrl.check_out_doc(chat, doc['id'], type_bd=doc_type, returning_time=2)
            #     message = "Your order was successful.\nCollect the book from the library not later than 4 hours" if status else "You already have this document"
            #     bot.edit_message_text(text=message, chat_id=chat, message_id=query.message.message_id)


    # Cancel the operation
    # params:
    #  bot -- This object represents a Bot's commands
    #  update -- This object represents an incoming update
    def cancel(self, bot, update):
        chat = update.message.chat_id
        self.inline_key.pop(chat, 0)
        self.location[chat] = ['main']
        user_type = self.cntrl.user_type(chat)
        keyboard = self.keyboard_dict[self.types[user_type]]

        bot.send_message(chat_id=chat, text="Main menu", reply_markup=RKM(keyboard, True))

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, error)


# Start Bot
# params:
#  Controller -- Bot's data base
def start_bot(controller):
    construct(LibraryBot)
    LibraryBot(configs.token, controller)
