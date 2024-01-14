import telebot
import Config

class tele_bot:
    def __init__(self):
        self.bot = telebot.TeleBot(Config.Token_bot)
        self.__id_telegram = Config.TG_Bot_ID

    def message_bot(self, text: str) -> None:
        for i in self.__id_telegram:
            self.bot.send_message(i, text)