import json
import os

class DataConfig:
    def __init__(self, file_path: str):
        if os.path.exists(file_path) and file_path.endswith(".json"):
            self.file_path = file_path
            self.__data = self.create_object()
        elif not os.path.exists(file_path):
            raise FileNotFoundError("Данный файл не найден")
        elif not file_path.endswith(".json"):
            raise FileNotFoundError("Данное расширение файла не поддерживается\nТребуемый формат: \".json\"")

    def create_object(self) -> dict:
        """
        Данная функция загружает данные с файла .json в оперативную память
        :return: данные с файла .json вида dict
        """
        with open(self.file_path, 'r', encoding="utf-8") as file:
            data: dict = json.load(file)
        return data

    def list_groups(self) -> list:
        """
        Возвращает список групп
        :return: список групп
        """
        return self.__data.get("list_of_groups")

    def list_teachers(self) -> list:
        """
        Возвращает список преподавателей
        :return: список преподавателей
        """
        return self.__data.get("list_of_teachers")

    def list_cabinet(self) -> list:
        """
        Возвращает список кабинетов
        :return: список кабинетов
        """
        return self.__data.get("list_of_cabinets")

    def data_calendar_id(self, data_key: str) -> str:
        """
        Возвращает id календаря по названию. В случае отсутствия данных вызывает исключение "ValueError"
        :param data_key: название искомого id календаря
        :return: id календаря
        """
        calendar_id: dict = self.__data.get("calendar_id")
        id = calendar_id.get(data_key, None)
        if id is not None:
            return id
        else:
            raise ValueError(f"Значение \"{data_key}\" не было найдено")

    def save_data(self, data: dict) -> None:
        with open(self.file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def __get_insert_data(self, data_structure: dict, text: str) -> None:
        data = {"group": "list_of_groups", "teacher": "list_of_teachers", "cabinet": "list_of_cabinets"}

        data_key = list(data_structure.get(text).keys())[0]
        data_value = list(data_structure.get(text).values())[0]

        list_of_data: list = self.__data.get(data[text])
        calendar_id: dict = self.__data.get("calendar_id")

        list_of_data.append(data_key)
        self.__data[data[text]] = list_of_data
        calendar_id[data_key] = data_value
        self.__data["calendar_id"] = calendar_id

        self.save_data(self.__data)

    def insert_data_id(self, list_data: list) -> None:
        """
        Обновляет данные в .json
        :param list_data: Список словарей, примерная структура: [{"data": {"key": "value id"}}] вместо data возможны ключи: group, teacher, cabinet
        :return: None
        """
        for data_structure in list_data:
            if isinstance(data_structure, dict):
                if data_structure.get("group", None):
                    self.__get_insert_data(data_structure=data_structure, text="group")
                elif data_structure.get("teacher", None):
                    self.__get_insert_data(data_structure=data_structure, text="teacher")
                elif data_structure.get("cabinet", None):
                    self.__get_insert_data(data_structure=data_structure, text="cabinet")
                else:
                    raise KeyError("Данное значение ключа не допустимо. Допустимые ключи: group, teacher, cabinet")
            else:
                raise ValueError("Данная структура не допустима")

    def __get_delete_data(self, data_structure: dict, text: str) -> None:
        data = {"group": "list_of_groups", "teacher": "list_of_teachers", "cabinet": "list_of_cabinets"}

        data_value = list(data_structure.values())[0]

        list_of_data: list = self.__data.get(data[text])
        calendar_id: dict = self.__data.get("calendar_id")

        list_of_data.remove(data_value)
        self.__data[data[text]] = list_of_data
        del calendar_id[data_value]
        self.__data["calendar_id"] = calendar_id

        self.save_data(self.__data)

    def delete_data_id(self, list_data: list) -> None:
        """
        Удаляет переданные данные в json
        :param list_data: Список словарей, примерная структура: [{"data": "value"}] вместо data возможны ключи: group, teacher, cabinet
        :return: None
        """
        for data_structure in list_data:
            if isinstance(data_structure, dict):
                if data_structure.get("group", None):
                    self.__get_delete_data(data_structure=data_structure, text="group")
                elif data_structure.get("teacher", None):
                    self.__get_delete_data(data_structure=data_structure, text="teacher")
                elif data_structure.get("cabinet", None):
                    self.__get_delete_data(data_structure=data_structure, text="cabinet")
                else:
                    raise KeyError("Данное значение ключа не допустимо. Допустимые ключи: group, teacher, cabinet")
            else:
                raise ValueError("Данная структура не допустима")
