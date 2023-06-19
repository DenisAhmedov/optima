from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import CONTRACTS_PARENT_ID
from us_ext.container import contracts_service
from us_ext.permissions import IsAllowedAddress


class ContractsView(APIView):
    permission_classes = [IsAllowedAddress]

    def post(self, request):
        contract_number: str = request.data.get('contract_number')
        if not contract_number:
            return Response({'error': 'Ожидается параметр contract_number'}, status=400)

        parent_id: int = request.data.get('parent_id', CONTRACTS_PARENT_ID)
        name: str = request.data.get('name', contract_number)

        result: dict = contracts_service.create_contract(contract_number=contract_number, parent_id=parent_id, name=name)
        status_code: int = 500 if result.get('error') else 201

        return Response(result, status=status_code)

    def get(self, request):
        try:
            parent_id: int = int(request.query_params.get('parent_id', CONTRACTS_PARENT_ID))
        except ValueError:
            return Response({'error': 'В параметре parent_id ожидается число'}, status=400)

        result: list[dict] = contracts_service.get_contracts(parent_id)
        status_code: int = 500 if (isinstance(result, dict) and result.get('error')) else 200

        return Response(result, status=status_code)


class ContractView(APIView):
    permission_classes = [IsAllowedAddress]

    def get(self, request, contract_number: str):
        result: dict = contracts_service.get_contract(contract_number)
        status_code: int = 500 if result.get('error') else 200

        return Response(result, status=status_code)

    def patch(self, request, contract_number: str):
        json_data: dict = request.data
        if not json_data:
            return Response({'error': 'Нет данных для обновления'}, status=400)
        result: dict = contracts_service.update_contract(contract_number, json_data)
        status_code: int = 500 if result.get('error') else 200

        return Response(result, status=status_code)

    def put(self, request, contract_number: str):
        json_data: dict = request.data

        if sorted(json_data.keys()) != sorted(['contract_number', 'name', 'parent_id']):
            return Response({'error': 'Отправлены неверные данные для обновления'}, status=400)
        result: dict = contracts_service.update_contract(contract_number, json_data)
        status_code: int = 500 if result.get('error') else 200

        return Response(result, status=status_code)

    def delete(self, request, contract_number: str):
        result: dict = contracts_service.delete_contract(contract_number)
        status_code: int = 500 if result.get('error') else 204

        return Response(result, status=status_code)
