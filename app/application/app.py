import sqlite3
from datetime import datetime

from loguru import logger

from .model import UserModel
from .settings import PATH_TO_DATABASE, PATH_TO_DESCRIPTION, COUNT_RECORDS, BULK_SIZE, RU_FORMAT_DATE, FORMAT_DATE
from .sql import GENDERS, INSERT_USER_QUERY, SELECT_USER_QUERY, SELECT_ALL_MALE_USER_QUERY, USER_TABLE_CREATE_QUERY
from .utils import time_decorator, fake




@time_decorator(f"Генерация {COUNT_RECORDS} случайных пользователей заняло", logger)
def gen_users_records():
    """Генерация 1 000 000 записей в базе данных."""

    for _ in range(0, COUNT_RECORDS, BULK_SIZE):
        yield [UserModel.create_random_user() for _ in range(BULK_SIZE)]


@time_decorator("Генерация 100 записей с фамилией на букву F заняло", logger)
def gen_users_hundreds_records():
    """Генерация 100 записей Users с фамилией на букву F."""

    users = []
    for _ in range(100):
        user = UserModel.create_random_user()
        while user.full_name[0] != 'F':
            name = fake.name_male() if user.gender == GENDERS[0] else fake.name_female()
            user.full_name = name
        users.append(user)
    return users


class Application:
    def __init__(self, mode: int):
        self.mode = mode
        self._conn = sqlite3.connect(PATH_TO_DATABASE)
        self._cur = self._conn.cursor()
        self._create_user_table()

    def save_users(self, users: list[UserModel]) -> None:
        self._cur.executemany(INSERT_USER_QUERY, [user.to_list() for user in users])
        self._conn.commit()

    @staticmethod
    def input_gender():
        while True:
            gender = input(f"Введите пол: {GENDERS}: ")
            if gender.capitalize() in GENDERS:
                return gender.capitalize()
            logger.warning(f"Неверно указан пол. Попробуйте еще раз.ожидаемые значения: {GENDERS}")

    @staticmethod
    def input_birth_date() -> datetime:
        while True:
            birth_date = input(f"Введите дату рождения в формате {RU_FORMAT_DATE}: ")
            try:
                return datetime.strptime(birth_date, FORMAT_DATE)
            except ValueError:
                logger.warning("Введен некорректный формат.")

    @staticmethod
    def input_full_name() -> str:
        while True:
            full_name = input("Введите фамилию, имя, отчество (при наличии), через пробел: ")
            if full_name.count(" "):
                return full_name
            logger.warning("Неверно указаны фамилия, имя, отчество. Попробуйте еще раз.")

    def run(self):
        return getattr(self, f"_run_mode_{self.mode}", self._run_not_implemented)()

    def _run_mode_1(self):
        """Добавление пользователя в базу данных, через консоль."""
        full_name = self.input_full_name()
        birth_date = self.input_birth_date()
        gender = self.input_gender()
        UserModel(full_name, birth_date, gender).save_to_db(self._conn)
        logger.info(f"Пользователь {full_name} добавлен в базу данных.")

    @time_decorator(f"Общее время на выборку уникальных записей их вывод занял", logger)
    def _run_mode_2(self):
        """Вывод списка всех уникальных пользователей из базы данных."""
        [print(*item) for item in self._cur.execute(SELECT_USER_QUERY).fetchall()]

    @time_decorator(f"Общее время на генерацию {COUNT_RECORDS + 100} записей и внесение в базу данных заняло", logger)
    def _run_mode_3(self):
        """Генерация случайных 1 000 000 пользователей.

        Дополнительно добавление в базу данных 100 записей на `F`."""

        for users in gen_users_records():
            self.save_users(users)
        self.save_users(gen_users_hundreds_records())  # 100 записей на F

    @time_decorator(f"Общее время на запрос и вывод данных из базы данных занял", logger)
    def _run_mode_4(self):
        [print(*item) for item in self._cur.execute(SELECT_ALL_MALE_USER_QUERY).fetchall()]

    @staticmethod
    def _run_mode_5():
        with open(PATH_TO_DESCRIPTION, "r", encoding="utf-8") as file:
            for line in file:
                logger.warning(line.replace("\n", ""))

    def _run_not_implemented(self):
        raise NotImplementedError("Заданный режим не реализован.")

    def _create_user_table(self):
        self._cur.execute(USER_TABLE_CREATE_QUERY)

    def close(self):
        self._cur.close()
        self._conn.close()
        logger.info("Соединение с базой данных закрыто.")
