from datetime import datetime

import google.oauth2.service_account
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient import errors

from JsonConfig import DataConfig


class Calendar:
    def __init__(self, file_path: str):
        service_account_file = file_path
        scopes = ["https://www.googleapis.com/auth/calendar"]

        credentials = google.oauth2.service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=scopes
        )
        self.__service = build('calendar', 'v3', credentials=credentials)
        self.config = DataConfig(file_path="json/Config.json")

    def new_events(self, title: str, description: str, day: str, time: list, color: int, calendar: str) -> None:
        """
        Создает ивент в календаре
        :param title: заголов пары
        :param description: описание пары
        :param day: день проведения пары
        :param time: время проведения пары [начало, конец]
        :param color: цвет отображения пары в календаре
        :param calendar: календарь для которого создается пара
        :return: None
        """
        event = {
            'summary': title,
            'description': description,
            'colorId': color,
            'start': {'dateTime': f'{day}T{time[0]}:00+03:00'},
            'end': {'dateTime': f'{day}T{time[1]}:00+03:00'}
        }
        try:
            self.__service.events().insert(calendarId=self.config.data_calendar_id(calendar), body=event).execute()
        except ValueError as error:
            pass
        except errors.HttpError as error:
            pass
        except Exception as error:
            pass

    def delete_events(self, id_events: list) -> None:
        """
        Удаляет ивент в календаре
        :param id_events: список данный формата {"календарь": "id ивента"}
        :return: None
        """
        num = -1
        for calendar in id_events:
            try:
                num += 1
                self.__service.events().delete(
                    calendarId=self.config.data_calendar_id(list(calendar.keys())[0]),
                    eventId=list(calendar.values())[0]
                ).execute()
            except errors.HttpError as error:
                pass

    def __search_calendar_events(self, data: list) -> list:
        """
        Осуществляет поиск ивентов в календаре
        :param data: список календарей в котором происходит поиск
        :return: список данных формата [{"календарь": "id ивента"}]
        """
        id_events = list()
        for calendar in data:
            now = datetime.utcnow().isoformat() + 'Z'
            events_result = None
            try:
                events_result = self.__service.events().list(
                    calendarId=self.config.data_calendar_id(calendar),
                    timeMin=now,
                    maxResults=100,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
            except errors.HttpError as error:
                pass
            events = events_result.get('items', [])
            for event in events:
                id_events.append({calendar: event.get('id')})
        return id_events

    def clear_calendar(self) -> None:
        """
        Функция для контроля поиска ивентов в календарях и их удаление
        :return: None
        """
        calendar_id_events = list()

        calendar_id_events.extend(self.__search_calendar_events(self.config.list_groups()))
        calendar_id_events.extend(self.__search_calendar_events(self.config.list_teachers()))
        calendar_id_events.extend(self.__search_calendar_events(self.config.list_cabinet()))

        self.delete_events(id_events=calendar_id_events)

    def create_calendar(self, title: str) -> str:
        """
        Создает календарь
        :param title: имя календаря
        :return: id созданного календаря
        """
        calendar = self.__service.calendars().insert(body={"summary": title}).execute()

        return calendar['id']

    def update_rule(self, calendar_id: str, admin_account: dict) -> tuple:
        """
        Обновляет права доступа для созданного календаря
        :param calendar_id: id календаря для которого обновляются права доступа
        :param admin_account: структура формата {"аккаунт пользователя": "права доступа"} права доступа: reader, writer, owner
        :return: кортеж со ссылками для доступа к календарю
        """
        # Добавление новых пользователей с правами редактора
        for account in admin_account:
            rule = {
                'scope': {'type': 'user', 'value': account},
                'role': admin_account[account]
            }
            self.__service.acl().insert(calendarId=calendar_id, body=rule).execute()

        # Открытие календаря для всех с правами на чтение
        rule = {
            'scope': {'type': 'default'},
            'role': 'reader'
        }
        self.__service.acl().insert(calendarId=calendar_id, body=rule).execute()

        # Получение ссылки для взаимодействия с календарем
        calendar_url = f'https://calendar.google.com/calendar?cid={calendar_id}'

        # Получение ссылки для поделиться с другими пользователями
        share_url = f'https://calendar.google.com/calendar/r?cid={calendar_id}'

        # Общедоступная ссылка на календарь в формате ical
        acal_url = f"https://calendar.google.com/calendar/ical/{calendar_id}%40group.calendar.google.com/public/basic.ics"

        url: tuple = (calendar_url, share_url, acal_url)

        return url

    def delete_calendar(self, calendar_id: str) -> None:
        """
        Удаляет дополнительный календарь
        :param calendar_id: id удаляемого календаря
        :return: None
        """
        try:
            self.__service.calendars().delete(calendarId=calendar_id).execute()
        except errors.HttpError as error:
            pass
        except Exception as error:
            pass


if __name__ == "__main__":
    google_calendar = Calendar(file_path="json/Google_Credention.json")
    google_calendar.clear_calendar()
