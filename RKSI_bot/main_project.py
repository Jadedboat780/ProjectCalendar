import datetime

import schedule

import Calendar
import Parsings
import download_excel
import logging_code

class The_basis:
    def __init__(self):
        # Инициализируем функции для работы основной программы
        self.excel = download_excel.Excel_tablet()
        self.planshet = Parsings.Parsing(1)
        self.calendar = Calendar.Google_calendar(program=1)  # 1 для работы основной программы
        self.date_time = datetime.datetime.now()
        self.__log_bot = logging_code.tele_bot()

    def update_table(self):
        new_time = str(datetime.datetime.now())

        if str(self.date_time) <= new_time < str((self.date_time + datetime.timedelta(minutes=50))):
            self.__log_bot.message_bot('Программа запустила обновление планшетки вовремя')
            self.date_time += datetime.timedelta(minutes=50)
            self.excel.download_excel()  # Скачивание обновленой версии excel таблицы
            self.check = self.planshet.planchette_check()
            if self.check:
                self.planshet.planchette()
            else:
                self.__log_bot.message_bot('Планшетка не соответствует требованиям')
        else:
            self.__log_bot.message_bot('Программа запустила обновление планшетки не вовремя, игнорируется данный запуск')

    def update_schedule_rksi(self):
        self.__log_bot.message_bot('Программа была запущена')
        self.calendar.clear_calendar()  # Очищаем календарь
        self.planshet.par_group()
        self.planshet.par_teacher()

message = logging_code.tele_bot()

def monday():
    excele = The_basis()
    for time in ['04:30', '07:15', '08:10', '09:05', '10:30', '12:20', '13:15', '15:00', '16:20', '17:11']:
        schedule.every().day.at(time).do(excele.update_table)
    del excele

def tuesday():
    excele = The_basis()
    for time in ['04:30', '07:15', '08:10', '09:05', '10:30', '12:20', '14:00', '15:50', '17:17', '18:34']:
        schedule.every().day.at(time).do(excele.update_table)
    del excele

def update_rksi():
    schedule_rksi = The_basis()
    schedule_rksi.update_schedule_rksi()
    del schedule_rksi

def main():
    """Функция запускает другие функции в определенное время и день недели"""
    schedule.every().monday.at('04:25').do(monday)
    schedule.every().tuesday.at('04:25').do(tuesday)
    schedule.every().wednesday.at('04:25').do(tuesday)
    schedule.every().thursday.at('00:00').do(update_rksi)
    schedule.every().thursday.at('04:25').do(tuesday)
    schedule.every().friday.at('04:25').do(tuesday)
    schedule.every().saturday.at('04:25').do(tuesday)
    schedule.every().saturday.at('22:40').do(update_rksi)
    schedule.every().sunday.at('06:00').do(update_rksi)
    schedule.every().sunday.at('12:00').do(update_rksi)
    schedule.every().sunday.at('15:00').do(update_rksi)
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    main()

