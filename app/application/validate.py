def validate_input(params: list[str]):
    error_message = "Параметр должен быть числом от 1 до 5"
    if len(params) == 1:
        raise ValueError("Не указан обязательный параметр командной строки. " + error_message)
    if len(params) > 2:
        raise ValueError("Слишком много параметров командной строки. " + error_message)
    if params[1].isalpha() or params[1] not in ["1", "2", "3", "4", "5"]:
        raise ValueError("Неверный параметр в командной строки. " + error_message)
