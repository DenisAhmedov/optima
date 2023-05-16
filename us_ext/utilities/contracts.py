from . import Api


def format_contract_data(data):
    """Приводит словарь с данными по договору к сжатому виду, отбрасывая ненужные поля"""

    data['result']['fields'] = {
        'name': data['result']['fields']['name'],
        'contract_number': data['result']['fields']['contract_number'],
        'parent_id': data['result']['fields']['parent_id']
    }

    return data['result']


def create_contract(contract_number, parent_id, name):
    """Создание договора с номером contract_num в папке с id = parent_id"""

    client = Api()
    params = {
        'method1': 'objects.create',
        'arg1': '{"contract_number": "%s", "parent_id": %s, "name": "%s", "tarif_id": 1}' %
                (contract_number, parent_id, name)
    }
    result = client.call_api(model='Abonents', params=params)
    if result.get('error'):
        return result

    return format_contract_data(result)


def get_contracts(parent_id):
    """Вывод всех номеров договоров в указанной папке"""

    client = Api()
    params = {
        'method1': 'objects.filter',
        'arg1': '{"parent_id": %s, "is_folder": false}' % parent_id,
        'fields': '["contract_number", "name", "parent_id"]'
    }
    result = client.call_api(model='Abonents', params=params)
    if result.get('error'):
        return result

    return result['result']


def get_contract(contract_number):
    """Получение информации по номеру договора"""

    client = Api()
    params = {
        'method1': 'objects.get',
        'arg1': '{"contract_number": "%s"}' % contract_number,
        'fields': '["contract_number", "name", "parent__name", "abonent_id_users"]'
    }
    result = client.call_api(model='Abonents', params=params)
    if result.get('error'):
        return result

    # Заменяем поле abonent_id_users на has_account
    if result['result']['fields'].pop('abonent_id_users'):
        result['result']['fields']['has_account'] = True
    else:
        result['result']['fields']['has_account'] = False
    return result['result']


def update_contract(contract_number, changes_data):
    """Обновление номера договора"""

    # Собираем строку аргументов для ключа arg2
    args_list = []
    for key, value in changes_data.items():
        args_list.append(f'"{key}": "{value}"')
    args_string = '{' + ', '.join(args_list) + '}'

    client = Api()
    params = {
        'method1': 'objects.get',
        'arg1': '{"contract_number": "%s"}' % contract_number,
        'method2': 'set',
        'arg2':  args_string,
        'method3': 'save',
        'arg3': '{}'

    }

    result = client.call_api(model='Abonents', params=params)
    if result.get('error'):
        return result

    return format_contract_data(result)


def delete_contract(contract_number):
    """Удаление договора по его номеру"""
    contract = get_contract(contract_number)
    if contract.get('error'):
        return contract
    if contract['fields']['has_account']:
        return {'error': 'Невозможно удалить договор, т.к. к нему привязана одна или более учетных записей'}

    client = Api()
    params = {
        'method1': 'objects.get',
        'arg1': '{"contract_number": "%s"}' % contract_number,
        'method2': 'delete',
        'arg2': '{}'
    }
    result = client.call_api(model='Abonents', params=params)
    if result.get('error'):
        return result

    return {'Result': 'Ok'}
