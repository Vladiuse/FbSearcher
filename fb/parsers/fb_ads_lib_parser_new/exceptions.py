class FbBlockLibError(Exception):
    """Блокировка фейсбуком запросов в библеотеку"""


class MaxWaitCardLoadError(Exception):
    """Превышено время ожидания карточек"""


class NoLoadCardBtnError(Exception):
    """Кнопка загрузки новых карточек не найдена"""