from typing import Dict

from . import BillingApiMixin


class ContractsDAO(BillingApiMixin):

    def get_contract(self, contract_number: str):
        params = {
            'method1': 'objects.get',
            'arg1': '{"contract_number": "%s"}' % contract_number,
            'fields': '["contract_number", "name", "parent__name", "abonent_id_users"]'
        }
        return self.call_api(model='Abonents', params=params)

    def create_contract(self, contract_number: str, parent_id: int, name: str) -> dict:
        params = {
            'method1': 'objects.create',
            'arg1': '{"contract_number": "%s", "parent_id": %s, "name": "%s", "tarif_id": 1}' %
                    (contract_number, parent_id, name)
        }
        return self.call_api(model='Abonents', params=params)

    def get_contracts(self, parent_id: str):
        params = {
            'method1': 'objects.filter',
            'arg1': '{"parent_id": %s, "is_folder": false}' % parent_id,
            'fields': '["contract_number", "name", "parent_id"]'
        }
        return self.call_api(model='Abonents', params=params)

    def update_contract(self, contract_number: str, changes_data: dict) -> dict:

        # Собираем строку аргументов для ключа arg2
        args_list: Dict[str] = []
        for key, value in changes_data.items():
            args_list.append(f'"{key}": "{value}"')
        args_string: str = '{' + ', '.join(args_list) + '}'

        params = {
            'method1': 'objects.get',
            'arg1': '{"contract_number": "%s"}' % contract_number,
            'method2': 'set',
            'arg2': args_string,
            'method3': 'save',
            'arg3': '{}'
        }
        return self.call_api(model='Abonents', params=params)

    def delete_contract(self, contract_number: str) -> dict:
        params = {
            'method1': 'objects.get',
            'arg1': '{"contract_number": "%s"}' % contract_number,
            'method2': 'delete',
            'arg2': '{}'
        }
        return self.call_api(model='Abonents', params=params)
