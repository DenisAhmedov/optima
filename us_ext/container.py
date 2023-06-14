from us_ext.dao import ContractsDAO
from us_ext.services import ContractsService

contracts_dao: ContractsDAO = ContractsDAO()
contracts_service: ContractsService = ContractsService(contracts_dao)
