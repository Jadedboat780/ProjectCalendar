import pymysql

class SQL_Connection_DB:
    def __init__(self, host: str, user: str, port: int, password: str, db_name: str, table_name: str = None):
        """db_name - это имя самой базы данных, table_name - это имя таблицы к которой подключаемся для выборки данных"""

        # Сохраняем полученные данные, и запрещаем к ним доступ из вне этого класса
        self.__host = host
        self.__user = user
        self.__port = port
        self.__password = password
        self.__db_name = db_name
        self.__table_name = table_name

    # Подключаемся к БД
    def connection(self) -> str:
        """Установите соединение с базой данных, для работы с ней))),
        если подключение удалось верну: 'Connection successufy',
        если же подключиться к базе данных не удастся то вызову исключение: 'Error connection server: (Возникшая ошибка)'"""
        try:
            self.__connection = pymysql.connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                password=self.__password,
                database=self.__db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            return 'Connection successufy'
        except Exception as e:
            raise Exception(f'Error connection server: {e}')

    # Выборка данных из БД
    def select_db_data(self, group: str, date: str, time: str, table_name: str = 'Visit_control') -> dict:
        """
        :param esp: номер кабинета в виде ('414')
        :param table_name: имя таблицы к которой требуется подключиться (является не обязательным аргументом если передали строку при инициализации класа)
        :return: возвращает список данных где кажный элемент является словарем
        Передайте в качестве аргумента номер аудитории и я вам верну все найденные результаты в виде списка, где кажное значение это словарь, если такие данные не
        будут найдены будет возвращено None, в этом методе вы можете переназначить переменную table_name на другие данные
        """

        if table_name == None:  # Проверяем есть ли изменения в название таблицы БД
            table_name = self.__table_name
        try:
            with self.__connection.cursor() as cursor:
                sql = f'SELECT * FROM `{table_name}` WHERE `Group`=%s AND `Couple_date`=%s AND `Couple_time`=%s'
                cursor.execute(sql, (group, date, time))
                return cursor.fetchone()
        except Exception as ex:
            return f'Error: {ex}'

    # Функция закрываем соединение с БД
    def close_connection(self, on_off: bool = False) -> str:
        """
        :param on_off: хранит bool для определения показывать сообщение о завершенном соединение с БД по умолчанию стоит False (не показывать)
        :return:
        Закрывает соединенис с базой данных
        """
        self.__connection.close()
        if on_off: return 'Соединение с БД закрыто'

    # Добавляет нового пользователя
    def insert_db_person(self, Cabinet, Couple, Teacher, Couple_date, Couple_time, Group, table_name='Visit_control') -> str:
        """
        :param name: имя пользователя
        :param passworrd: пароль пользователя
        :param id_card: номер карты пользователя (является не обязательной, данные возьмутся из основной БД)
        :param table_name: имя таблицы куда заносить нового пользователя (является обязательной)
        :return: возвращает строку с результатом работы функции

        Данная функция проверяет отсувствует ли данный пользователь в базе данных если так то добавляем нового, если данный пользователь
        есть в базе данных то выводим соответствующее сообщение
        """

        try:
                with self.__connection.cursor() as cursor:
                    sql = f'INSERT INTO `{table_name}` (`Cabinet`, `Couple`, `Group`, `Teacher`, `Couple_date`, `Couple_time`) VALUES (%s, %s, %s, %s, %s, %s)'
                    cursor.execute(sql, (Cabinet, Couple, Group, Teacher, Couple_date, Couple_time))
                    self.__connection.commit()
                return f'Пользователь был успешно добавлен'
        except Exception as ex:
                return f'Добавить пользователя не удалось, {ex}'

    # Изменение данных в БД
    def update_person_date(self, cabinet: str, couple: str, teacher: str, id: str, table_name='Visit_control') -> str:
        """
        :param table_name: имя таблицы в которой изменять данные
        :param name: Имя пользователя используется для поиска пользователя в БД
        :param password: пароль используется для поиска пользователя в БД
        :param new_name: изменяем старое имя на новое
        :return: Возврашает результат выполнения функции

        Данная функция позволяет обновить данные в базе данных используя переменные new_name, new_password и new_id_card
        """
        try:
            with self.__connection.cursor() as cursor:
                sql = f'UPDATE `{table_name}` SET `Cabinet`=%s, `Couple`=%s, `Teacher`=%s WHERE `ID`=%s'
                cursor.execute(sql, (cabinet, couple, teacher, id))
                self.__connection.commit()
                return 'Обновление данных прошло успешно'
        except Exception as e:
            return f'Error: {e}'
