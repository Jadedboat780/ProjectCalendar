import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import logging_code

class Excel_tablet:
    def __init__(self):
        self.url_adress = 'https://drive.google.com/drive/folders/1UH5pcJc0pxkYFWBMI_bNCxrdlApqv3nX'
        self.url_excel_file = 'https://drive.google.com/uc?export=download&id='
        self.__log_bot = logging_code.tele_bot()

    def download_excel(self):
        self.__log_bot.message_bot('Парсинг расписания планшетки начал работу')

        try:
            self.responce = requests.get(url=self.url_adress)
            self.soup = BeautifulSoup(self.responce.text, 'lxml')
            self.soup = self.soup.find_all('div', class_='Q5txwe')

            for number, i in enumerate(self.soup, start=0):
                self.dates = str(datetime.now()).split()[0]
                self.dts = self.dates.split('-')
                self.dates = f'{self.dts[-1]}.{self.dts[1]}.{self.dts[0]}'  # Преобразуем текущую дату в нужный вид
                plans = i.text[0:-5]  # Убираем с названия планшетки '.xlsx'

                if self.dates == plans:  # Если текущая дата совпадает с датой планшетки
                    response = requests.get(
                        url='https://drive.google.com/drive/folders/1UH5pcJc0pxkYFWBMI_bNCxrdlApqv3nX')
                    soup = BeautifulSoup(response.text, 'lxml')
                    id_list = [i.replace('data-id="', '') for i in
                               re.findall(r'data-id="[\w\-\+/#\(\)\*&\^:<>\?\!%\$]+', str(soup))]
                    self.data_exel(identifier=id_list[number])  # Запускаем скачивание планшетки по ее id
                    break
        except Exception as e:
            self.__log_bot.message_bot(f'''Была вызвана ошибка в разделе поиска  планшеток
                                 описание ошибки: {e}
                                 !ИЗ-ЗА ОШИБКИ ДАЛЬНЕЙШАЯ РАБОТА ПРОГРАММЫ ОСТАНОВЛЕНА ДО ПОВТОРНОГО ЕГО ВЫЗОВА!''')

    def data_exel(self, identifier: str):  # Функция скачивания планшетки
        """Функция скачивает найденную планшетку"""
        try:
            planchet = requests.get(url=f'{self.url_excel_file}{identifier}')
            with open('planchette.xlsx', 'wb') as xlsx_file:
                xlsx_file.write(planchet.content)
                self.__log_bot.message_bot('Программа успешно скачала новую планшетку планшетку')
        except Exception as e:
            self.__log_bot.message_bot(f'''Была вызвана ошибка в разделе скачивания планшетки
                                     описание ошибки: {e}
                                     !ИЗ-ЗА ОШИБКИ ДАЛЬНЕЙШАЯ РАБОТА ПРОГРАММЫ ОСТАНОВЛЕНА ДО ПОВТОРНОГО ЕГО ВЫЗОВА!''')
