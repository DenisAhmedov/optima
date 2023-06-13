from us_ext.dao import ContractsDAO
from us_ext.services import ContractsService

contracts_dao = ContractsDAO()
contracts_service = ContractsService(contracts_dao)
