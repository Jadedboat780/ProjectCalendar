import httplib2
import apiclient.discovery
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient import errors
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials


class SpreadSheet:
    def __init__(self, file_path_drive: str, file_path_spreadsheet):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            filename=file_path_spreadsheet,
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
        http_auth = credentials.authorize(httplib2.Http())
        self.__service = apiclient.discovery.build("sheets", "v4", http=http_auth)

        credentials1 = service_account.Credentials.from_service_account_file(
            filename=file_path_drive,
            scopes=["https://www.googleapis.com/auth/drive"])
        self.__services = build("drive", "v3", credentials=credentials1)

        self.spreadsheet_id = "1s0EvrWwJVtV_r7poJaaxfs63CSBjx2VmKt0609mZ8Ek"

    def insert_data(self, calendar_name: str, ical_url: str, https_url: str) -> None:
        """
        Добавляет новую запись в excel таблицу
        :param calendar_name: имя календаря
        :param ical_url: общедоступная ссылка для добавления календаря в формате iCal
        :param https_url: общедоступная ссылка для добавления календаря
        :return: None
        """
        body = {'values': [[calendar_name, ical_url, https_url]]}
        try:
            self.__service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range='Календарь!A10:C1000',
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()

            # Получение последней добавленной ячейки
            last_row = len(body['values']) + 9  # С учетом начала диапазона 'A10'
            print(last_row)
            cell_range = f'Календарь!A{last_row}'

            # Окрашивание ячейки в зеленый цвет
            requests = [
                {
                    'updateCells': {
                        'range': {
                            'sheetId': 0,
                            'startRowIndex': last_row - 1,
                            'endRowIndex': last_row,
                            'startColumnIndex': 0,
                            'endColumnIndex': 1
                        },
                        'rows': [
                            {
                                'values': [
                                    {
                                        'userEnteredFormat': {
                                            'backgroundColor': {
                                                'red': 0.0,
                                                'green': 1.0,
                                                'blue': 0.0
                                            }
                                        }
                                    }
                                ]
                            }
                        ],
                        'fields': 'userEnteredFormat.backgroundColor'
                    }
                }
            ]

            self.__service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={'requests': requests}
            ).execute()

        except errors.HttpError as error:
            pass
        except Exception as error:
            pass

    def clear_color_formated(self):
        request = [
            {
                'updateCells': {
                    'range': {
                        'sheetId': 0,
                        'startRowIndex': 7,
                        'endRowIndex': 1000,
                        'startColumnIndex': 0,
                        'endColumnIndex': 3
                    },
                    'rows': [
                        {
                            'values': [
                                {
                                    'userEnteredFormat': {
                                        'backgroundColor': {
                                            'red': 0.0,
                                            'green': 0.0,
                                            'blue': 0.0
                                        }
                                    }
                                }
                            ]
                        }
                    ],
                    'fields': 'userEnteredFormat.backgroundColor'
                }
            }
        ]

        # Отправка запроса на обновление заднего фона ячейки
        self.__service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={'requests': [request]}
        ).execute()


if __name__ == "__main__":
    spreadsheet = SpreadSheet(file_path_drive="json/CredentialsDrive.json", file_path_spreadsheet="json/CredentialSpreadSheet.json")
    # spreadsheet.insert_data("103", "sdfsf", 'sdafsfas')
    spreadsheet.clear_color_formated()