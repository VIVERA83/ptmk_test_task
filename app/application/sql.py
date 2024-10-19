GENDERS = ['Male', 'Female']

USER_TABLE_CREATE_QUERY = (
    "CREATE TABLE IF NOT EXISTS users ("
    "id INTEGER PRIMARY KEY,"
    "full_name TEXT,"
    "birth_date DATE,"
    "gender CHAR(6),"
    "age INTEGER"
    ")")

INSERT_USER_QUERY = ("INSERT INTO users (full_name, birth_date, gender, age) "
                     "VALUES (?, ?, ?, ?)")

SELECT_USER_QUERY = ("SELECT DISTINCT full_name, date(birth_date), gender, age "
                     "FROM users "
                     "ORDER BY full_name")

SELECT_ALL_MALE_USER_QUERY = (f"SELECT full_name, date(birth_date), gender, age "
                              f"FROM users "
                              f"WHERE gender = '{GENDERS[0]}' "
                              f"AND users.full_name LIKE 'F%'")
