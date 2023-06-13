from us_ext.dao import ContractsDAO


class ContractsService:
    def __init__(self, dao: ContractsDAO):
        self.dao = dao

    @staticmethod
    def format_contract_data(data):
        """Приводит словарь с данными по договору к сжатому виду, отбрасывая ненужные поля"""

        data['result']['fields'] = {
            'name': data['result']['fields']['name'],
            'contract_number': data['result']['fields']['contract_number'],
            'parent_id': data['result']['fields']['parent_id']
        }

        return data['result']

    def get_contract(self, contract_number):
        """Получение информации по номеру договора"""

        result = self.dao.get_contract(contract_number)
        if result.get('error'):
            return result

        # Заменяем поле abonent_id_users на has_account
        if result['result']['fields'].pop('abonent_id_users'):
            result['result']['fields']['has_account'] = True
        else:
            result['result']['fields']['has_account'] = False
        return result['result']

    def create_contract(self, contract_number, parent_id, name=None):
        """Создание договора с номером contract_num в папке с id = parent_id"""

        if not name:
            name = contract_number
        result = self.dao.create_contract(contract_number, parent_id, name)
        if result.get('error'):
            return result

        return self.format_contract_data(result)

    def get_contracts(self, parent_id):
        """Вывод всех номеров договоров в указанной папке"""

        result = self.dao.get_contracts(parent_id)
        if result.get('error'):
            return result

        return result['result']

    def update_contract(self, contract_number, changes_data):
        """Обновление номера договора"""

        result = self.dao.update_contract(contract_number, changes_data)
        if result.get('error'):
            return result
        return self.format_contract_data(result)

    def delete_contract(self, contract_number):
        """Удаление договора по его номеру"""

        contract = self.get_contract(contract_number)
        if contract.get('error'):
            return contract
        if contract['fields']['has_account']:
            return {'error': 'Невозможно удалить договор, т.к. к нему привязана одна или более учетных записей'}

        result = self.dao.delete_contract(contract_number)
        if result.get('error'):
            return result

        return {'Result': 'Ok'}
