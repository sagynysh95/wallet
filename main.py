import re
from datetime import datetime
import json
from typing import Dict, Union, Optional, Iterator


# import pydoc


class Wallet:
    """
    Класс для работы с кошельком.

    Атрибуты
    ---------
    operation_index: int
        ведет нумерацию записей в базе

    Методы
    ------
    load_data():
        Загружает данные с базы
    change_overall_money(operation_type, money, wallet_data):
        Изменяет итоговую сумму в зависимости доход это или расход
    show_money():
        Выводить информацию о доходах, расходах и итоговой сумме
    add_record(operation_type, money, description):
        Добавляет запись в базу
    edit_record(id, money = None, description = None):
        Изменяет запись по id
    search_items(id = None, add_date = None, change_date = None, category = '', money = None):
        Ищет в базе записи по поданным значениям
    """
    def __init__(self, operation_index: int = 1) -> None:
        self.operation_index = operation_index

    def load_data(self) -> Dict[str, list]:
        """
        Загружает данные с базы и возвращает их

        :return: загруженные данные с базы
        """
        with open('wallet_data.json', 'r') as file:
            data: Dict[str, list] = json.load(file)
            return data

    def change_overall_money(self, operation_type: str, money: int, wallet_data: Dict[str, list]) -> Dict[str, list]:
        """
        Изменяет итоговую сумму в зависимости доход это или расход

        :param operation_type: типа операции, доход или расход
        :param money: сумма денег которые нужно добавить или отнять от итоговой суммы
        :param wallet_data: данные с базы
        :return: измененные данные с базы
        """
        if operation_type.lower() == "доход":
            wallet_data["wallet_data"][0]["доход"] += money
            wallet_data["wallet_data"][0]["итог"] += money
        elif operation_type.lower() == "расход":
            wallet_data["wallet_data"][0]["расход"] += money
            wallet_data["wallet_data"][0]["итог"] -= money
        return wallet_data

    def show_money(self) -> str:
        """
        Выводить информацию о доходах, расходах и итоговой сумме

        :return: Данные о доходах, расходах и итоговой сумме
        """
        wallet_data: Dict[str, list] = self.load_data()
        income: int = wallet_data["wallet_data"][0]["доход"]
        expense: int = wallet_data["wallet_data"][0]["расход"]
        overall: int = wallet_data["wallet_data"][0]["итог"]
        result = 'Доход: {}\nРасходы: {}\nИтого: {}'.format(income, expense, overall)
        return result

    def add_record(self, operation_type: str, money: int, description: str = "") -> str:
        """
        Добавляет запись в базу

        :param operation_type: типа операции, доход или расход
        :param money: сумма денег
        :param description: описание операции
        :return: Строку с сообщением об успешно добавлений записи
        """
        wallet_data: Dict[str, list] = self.load_data()
        data: Dict[str, any] = {"номер": self.operation_index,
                                "дата добавления": f"{datetime.now().date()}",
                                "дата изменения": "",
                                "категория": operation_type,
                                "сумма": money,
                                "описание": description}

        wallet_data["wallet_data"].append(data)
        wallet_data: Dict[str, list] = self.change_overall_money(operation_type, money, wallet_data)

        with open('wallet_data.json', 'w') as file:
            json.dump(wallet_data, file, ensure_ascii=False, indent=4)
            self.operation_index += 1
        result = (f'{operation_type.capitalize()} был успешно добавлен\nИтоговая сумма на счету: '
                  f'{self.load_data()["wallet_data"][0]["итог"]}')
        return result

    def edit_record(self, id: int, money: int = None, description: str = None) -> str:
        """
        Изменяет запись по id

        :param id: id записи для редактировать
        :param money: сумма денег на переписание
        :param description: описание на переписание
        :return: Строку об успешно выполнении и данные измененной записи
        """
        wallet_data: Dict[str, list] = self.load_data()
        for record in wallet_data["wallet_data"]:
             if record.get("номер") == id:
                 record["сумма"]: int = money if money else record["сумма"]
                 record["описание"]: int = description if description else record["описание"]
                 record["дата изменения"]: str = f"{datetime.now().date()}"
                 operation_type: str = record["категория"]
                 if money:
                     wallet_data = self.change_overall_money(operation_type, money, wallet_data)
                 with open('wallet_data.json', 'w') as file:
                     json.dump(wallet_data, file, ensure_ascii=False, indent=4)
                 return (f'Запись c id {id} успешно изменен\n'
                         f'{json.dumps(record, indent=4, ensure_ascii=False)}')
        else:
            return 'Записи с таким id не существует. Попробуйте еще раз'


    def search_items(self, id: int = None, add_date: str = None, change_date: str = None,
                           category: str = '', money: int = None) -> Iterator[Union[str, dict]]:
        """
        Ищет в базе записи по одному из критериев отправленный в функцию

        :param id: id записи
        :param add_date: дата добавления записи
        :param change_date: дата изменения записи
        :param category: категория записи
        :param money: сумма записи
        :return: Генератор с найденными данными в базе
        """
        wallet_data: Dict[str, list] = self.load_data()
        anything_printed: bool = False
        for elem in wallet_data["wallet_data"][1:]:
            if (elem["номер"] == id or
                elem["дата добавления"] == add_date or
                elem["дата изменения"] == change_date or
                elem["категория"] == category.lower() or
                elem["сумма"] == money):
                anything_printed: bool = True
                yield json.dumps(elem, indent=4, ensure_ascii=False)
        if not anything_printed :
            yield 'Записи по введеннным данным отсутствуют в базе'


class Realization:
    """
        Класс для реализации работы с кошельком.

        Атрибуты:
            wallet: Wallet
                экземпляр класс Wallet

        Методы:
            check_negative_value(money):
                Проверяет чтобы итоговая сумма не была ниже нуля
            add():
                Работая с экземпляром класса Wallet добавляет запись в базу
            edit():
                Работая с экземпляром класса Wallet изменяет запись в базе
            search():
                Работая с экземпляром класса Wallet ищет запись в базе по параметрам
            main():
                Используя экземпляр класса Wallet запускает работу кошелька
        """
    wallet: Wallet = Wallet()


    def check_negative_value(self, money: int) -> bool:
        """
        Проверяет чтобы при операции с расходами итоговая сумма не была ниже нуля

        :param money: Сумма подающаяся на вход
        :return: bool значение в зависимости итог ушел в минус или нет
        """
        overall: int = self.wallet.load_data()["wallet_data"][0]["итог"]
        if overall - money < 0:
            print('Итоговая сумма в кошелке не может быть ниже нуля.\n'
                  f'У Вас в кошелке {overall} денег. Попробуйте другие значения\n')
            return False
        return True

    def add(self) -> Optional[str]:
        """
        Работая с экземпляром класса Wallet добавляет запись в базу

        :return: Строку об успешно добавлением записи
        """
        operation_type: str = input('Введите типа операции (доход/расход):\n> ').lower()
        if operation_type in ('доход', 'расход'):
            try:
                amnt_money: int = int(input('Введите сумму:\n> '))
                if operation_type == 'расход' and not self.check_negative_value(amnt_money):
                    return self.add()
                description: str = input('Введите описание:\n> ')
                return self.wallet.add_record(operation_type, amnt_money, description)
            except ValueError:
                print('Неверно введенные данные. Попробуйте еще раз')
                self.add()
        else:
            print('Неверно введенные данные. Попробуйте еще раз')
            self.add()

    def edit(self) -> str:
        """
        Работая с экземпляром класса Wallet изменяет запись в базе

        :return: Строку об успешно выполнении и данные измененной записи
        """
        amnt_operations: int = len(self.wallet.load_data()["wallet_data"]) - 1
        if amnt_operations == 0:
            return 'К сожалению, в вашем кошелке еще нет операции. Сначала добавьте, пожалуйста'
        else:
            print(f'В вашем кошелке {amnt_operations} записи')
            id: int = int(input(f'Введите id операции от 1 до {amnt_operations}:\n> '))
            print('Вы можете изменить сумму и/или описание')
            data: str = input('Введите через пробел эти данные:\n> ')
            try:
                data_lst: list = data.split(" ", 1)
                result = self.wallet.edit_record(id, int(data_lst[0]), data_lst[1])
                return result
            except IndexError:
                return self.wallet.edit_record(id, money=int(data))
            except ValueError:
                return self.wallet.edit_record(id, description=data)

    def search(self) -> Iterator[Union[str, dict]]:
        """
        Работая с экземпляром класса Wallet ищет запись в базе по параметрам

        :return: Генератор с найденными данными в базе
        """
        print('Вы можете искать записи по одному из критериев:\n'
              '> номер/дата добавления/дата изменения/категория/сумма')
        data: str = input('Введите критерий поиска:\n> ').lower()
        if re.search(r'(id)|(номер)', data):
            id: int = int(input('Введите id записи, которую нужно вывести:\n> '))
            return self.wallet.search_items(id=id)
        elif re.search(r'(добав)', data):
            date: str = input('Введите дату добавления записей, которые нужно вывести (в формате "YYYY-MM-DD"):\n> ')
            return self.wallet.search_items(add_date=date)
        elif re.search(r'(измен)', data):
            date: str = input('Введите дату изменения записей, которые нужно вывести (в формате "YYYY-MM-DD"):\n> ')
            return self.wallet.search_items(change_date=date)
        elif re.search(r'(категория)', data):
            category: str = input('Введите категорию записей, которые нужно вывести:\n> ')
            return self.wallet.search_items(category=category)
        elif re.search(r'(сумм)', data):
            money: int = int(input('Введите сумму записей, которые нужно вывести:\n> '))
            return self.wallet.search_items(money=money)
        else:
            print('Неверно введенные данные. Попробуйте еще раз\n')
            self.search()

    def main(self) -> None:
        """
        Используя экземпляр класса Wallet запускает работу кошелька

        :return: None
        """
        print('Добро пожаловать в личный финансовый кошелек, которая поможет Вам управлять вашими деньгами')
        while True:
            print('\nКакую операцию хотите выполнить:\n'
                  '> Вывод баланса\n'
                  '> Добавление записи дохода или расхода\n'
                  '> Редактирование записи по id\n'
                  '> Поиск по записям\n'
                  '> Выйти\n')
            action: str = input('Введите название операции:\n> ').lower()

            if re.search(r'(вывод)|(баланс)', action):
                print(self.wallet.show_money())

            elif re.search(r'(добав)|(доход)|(расход)', action):
                print(self.add())

            elif re.search(r'(редакт)|(измен)', action):
                print(self.edit())

            elif re.search(r'(поиск)|(искать)', action):
                for elem in self.search():
                    print(elem)

            elif action == 'выйти':
                print(f'К концу работы с кошелком, у Вас:\n')
                print(self.wallet.show_money())
                break

            else:
                print('Неверно введенные данные. Попробуйте еще раз\n')


if __name__ == '__main__':
    # pydoc.writedoc('main')
    # with open('wallet_data.json', 'w') as file:
    #     data: Dict[str, list] = {"wallet_data": [{"доход": 0, "расход": 0, "итог": 0}]}
    #     json.dump(data, file, indent=4, ensure_ascii=False)

    Realization().main()




