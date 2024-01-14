import pandas as pd


class Schedule:
    def __init__(self, file_path: str):
        self.__path = file_path
        self.main: pd.DataFrame

        self.__cook_data()
        self.__get_first_build()

    def run(self):
        return self.__made_info()

    def get_groups_first_build(self) -> list:
        group = []
        for i in self.main['group'].squeeze(axis=1).unique().tolist():
            if i != "":
                group.append(i)
        return group

    def get_teacher_first_build(self) -> list:
        teacher = []
        for i in self.main['teacher'].squeeze(axis=1).unique().tolist():
            if i != "":
                teacher.append(i)
        return teacher

    def __cook_data(self) -> pd.DataFrame:
        df = pd.DataFrame(pd.read_json(self.__path).loc[0].iloc[0]['groups'])

        df_main = pd.DataFrame(columns=[['group', 'auditory', 'date', 'subject', 'teacher', 'time_start', 'time_end']])
        for week, group in zip(df['days'], df['group_name']):
            for day in week:
                try:
                    for i in day['lessons']:
                        data = [group, i['auditories'][0]['auditory_name'], i['date'],
                                i['subject'], i['teachers'][0]['teacher_name'],
                                i['time_start'], i['time_end']]
                        df_main.loc[len(df_main.index)] = data
                except:
                    pass

        self.main = df_main
        return df_main

    def __made_info(self) -> (list, list, list):
        group_list = []
        prepod_list = []
        room_list = []

        for i in self.main.values.tolist():
            text_g = f"({i[-3]}){i[3]}"
            desc_g = f"Время {i[-2]} - {i[-1]}: {i[-3]}, ауд. {i[1].split('-')[0]}"
            date = self.fix_date(i[2])

            text_p = f"({i[0]}){i[3]}"
            desc_p = f"Время {i[-2]} - {i[-1]}: {i[0]}, ауд. {i[1].split('-')[0]}"

            text_r = f"{i[0]} - {i[-3]}"
            desc_r = f"{i[0]} - {i[-3]} ({i[3]})"


            group_list.append([text_g, desc_g, date, [i[-2], i[-1]], 7, i[0]])
            prepod_list.append([text_p, desc_p, date, [i[-2], i[-1]], 8, i[-3]])
            room_list.append([text_r, desc_r, date, [i[-2], i[-1]], 5, i[1].split('-')[0]])

        return group_list, prepod_list, room_list

    def __get_first_build(self) -> pd.DataFrame:
        data = self.main
        data['auditory'] = data['auditory'].astype(str)
        data['auditory'] = data['auditory'].apply(lambda x: [i if i.split("-")[-1] == "1" and i.split("-")[0][:-1] != "Общ" else None for i in x]).reset_index(drop=True)
        data.dropna(inplace=True)
        self.main = data
        return data

    @staticmethod
    def fix_date(data: str) -> str:
        date = data.split('-')
        if len(date[0]) != 2:
            date[0] = "0" + str(date[0])
        if len(date[1]) != 2:
            date[0] = "0" + str(date[1])
        date = "-".join(date)
        return date


if __name__ == '__main__':
    S = Schedule("json/Raspisanie_11.json")
    g, p, r = S.run()
    # print(g)
    # group = S.get_groups_first_build()
    # teacher = S.get_teacher_first_build()
    # print(teacher)


