from unittest import TestCase
import json
from typing import Iterator

from main import Realization, Wallet

WALLET_DATA= {
    "wallet_data": [
        {
            "доход": 18500,
            "расход": 3900,
            "итог": 14600
        },
        {
            "номер": 1,
            "дата добавления": "2024-05-05",
            "дата изменения": "",
            "категория": "доход",
            "сумма": 6500,
            "описание": ""
        },
        {
            "номер": 2,
            "дата добавления": "2024-05-05",
            "дата изменения": "",
            "категория": "доход",
            "сумма": 12000,
            "описание": ""
        },
        {
            "номер": 3,
            "дата добавления": "2024-05-05",
            "дата изменения": "",
            "категория": "расход",
            "сумма": 1200,
            "описание": ""
        },
        {
            "номер": 4,
            "дата добавления": "2024-05-05",
            "дата изменения": "",
            "категория": "расход",
            "сумма": 2100,
            "описание": ""
        },
        {
            "номер": 5,
            "дата добавления": "2024-05-05",
            "дата изменения": "2024-05-05",
            "категория": "расход",
            "сумма": 600,
            "описание": "памперс"
        }
    ]
}

class TestWallet(TestCase):
    def setUp(self):
        with open('wallet_data.json', 'w') as file:
            json.dump(WALLET_DATA, file, indent=4, ensure_ascii=False)
        self.wallet = Wallet()
        self.realization = Realization()

    def test_print_balance(self):
        data = self.wallet.show_money()
        self.assertTrue('Доход' in data)

    def test_add_record(self):
        data = self.wallet.add_record('доход', 2000)
        self.assertTrue('успешно' in data)

    def test_edit_record(self):
        data = self.wallet.edit_record(9, 4200)
        self.assertTrue('успешно', 'еще раз' in data)

    def test_search_record(self):
        data = self.wallet.search_items(id=9)
        self.assertIsInstance(data, Iterator)
