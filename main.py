from JsonConfig import DataConfig
from GoogleCalendar import Calendar
from read_json import Schedule


class UpdateSchedule:
    def __init__(self, file_path_config: str, path_google_credentials: str, file_path_schedule: str):
        self.__json_config = DataConfig(file_path=file_path_config)
        self.__calendar = Calendar(file_path=path_google_credentials)
        self.__schedule = Schedule(file_path=file_path_config)

    