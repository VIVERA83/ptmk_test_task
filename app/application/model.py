import sqlite3
from datetime import datetime

from .sql import INSERT_USER_QUERY, GENDERS
from .utils import fake


class UserModel:
    def __init__(self, full_name: str, birth_date: datetime, gender: str) -> None:
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender
        self.age = self._calculate_age()

    def to_list(self) -> list:
        return [self.full_name, self.birth_date, self.gender, self.age]

    def _calculate_age(self) -> int:
        today = datetime.today()
        return (today.year - self.birth_date.year) - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def save_to_db(self, conn: sqlite3.Connection) -> None:
        with conn as cursor:
            cursor.execute(
                INSERT_USER_QUERY,
                (self.full_name, self.birth_date, self.gender, self.age))
            conn.commit()

    @classmethod
    def create_random_user(cls):
        gender = fake.random_element(GENDERS)
        birth_date = fake.date_time_between(start_date="-30y", end_date="now")
        name = fake.name_male() if gender == GENDERS[0] else fake.name_female()
        return cls(name, birth_date, gender)

    def __repr__(self) -> str:
        return f"<User {self.full_name} {self.gender} {self.age}>"