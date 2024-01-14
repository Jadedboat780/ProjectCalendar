from datetime import datetime

import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build

import Config
import logging_code

class Google_calendar:
    def __init__(self, program):
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        self.__calendar_id = Config.calendar_id
        self.__servise_account_file = '../json/Google_Credention.json'
        self.__credentials = service_account.Credentials.from_service_account_file(self.__servise_account_file, scopes=self.scopes)
        self.__service = googleapiclient.discovery.build('calendar', 'v3', credentials=self.__credentials)

        self.__calendar_id = Config.CalendarID

        self.__log_bot = logging_code.tele_bot()

        self.name_teacher = Config.name_teacher
        self.name_groups = Config.name_groups

        self.id_events = list()
        self.name_list = list()

    def new_events(self, text: str, description: str, day: str, time: str, color: str, group: str):
        if '-' not in time:
            time = time.split(' — ')
        else:
            time = time.split('-')

        time[0] = time[0].replace(' ', '')
        time[-1] = time[-1].replace(' ', '')
        event = {
            'summary': text,
            'description': description,
            'colorId': color,
            'start': {'dateTime': f'{day}T{time[0]}:00+03:00'},
            'end': {'dateTime': f'{day}T{time[-1]}:00+03:00'}
        }
        try:
            self.__service.events().insert(calendarId=self.__calendar_id[group], body=event).execute()  # Выполняем запрос о создании ивента
            # print(f'Был создан ивент - {group}')
        except Exception as e:
            self.__log_bot.message_bot(f'''Произошла ошибка\n
                                Ошибка была вызвана этими данными:\n\n
                                text = '{text}', \ndescription = '{description}', \nday = '{day}', 
                                \ntime = {time}, \ncolor = '{color}', \ngroup = '{group}'\n
                                Описание ошибки: {e}''')

    def delete_events(self):
        num = -1
        for event_id in self.id_events:
            try:
                num += 1
                self.__service.events().delete(calendarId=self.__calendar_id[event_id], eventId=self.id_events[num + 1]).execute()
            except:
                pass
        self.id_events.clear()

    def clear_calendar(self):
        for calen_id in self.__calendar_id:
            n = calen_id.strip()
            if n in Config.name_teacher or n in Config.name_groups:
                now = datetime.utcnow().isoformat() + 'Z'
                events_result = self.__service.events().list(calendarId=self.__calendar_id[n], timeMin=now, maxResults=100, singleEvents=True, orderBy='startTime').execute()
                events = events_result.get('items', [])
                for event in events:
                    self.id_events += (n, event.get('id'))
        self.delete_events()  # вызываем метод для удаления событий из id_events списка

    def get_events_list(self, time: str):
        """Функция находит id ивентов в календаре и записывает их в лист"""
        self.id_events.clear()
        for i in self.__calendar_id:
            n = i.strip()
            if n in self.name_teacher or n in self.name_groups:
                try:
                    now = datetime.utcnow().isoformat() + 'Z'
                    events_result = self.__service.events().list(calendarId=self.__calendar_id[n], timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
                    events = events_result.get('items', [])
                    for event in events:
                        start = str(event['start'].get('dateTime')).split('T')
                        if start[0] == time:
                            self.id_events += (n, event.get('id'))
                except Exception as e:
                    self.__log_bot.message_bot(f'''Ошибка при поиске ID событий в календаре: Данные вызвавшие ошибку: {i} \nПодробности ошибки: {e}''')
            else:
                self.__log_bot.message_bot(f'''Ошибка при поиске ID событий в календаре: преподаватель или группа не найдены
                                         Данные, не найденные в списке: \'{i}\' -- \'{n}\'''')
        self.name_list.clear()