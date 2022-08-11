'''This module defines Easy Equities data access components.'''
from datetime import datetime
from logging import debug, info
import json
from easy_equities_client.clients import EasyEquitiesClient
from easy_equities_client.accounts.types import Account
from frostaura.data_access.resources_data_access import IResourcesDataAccess
from frostaura.data_access.personal_asset_data_access import IPersonalAssetDataAccess

class EasyEquitiesPersonalAssetDataAccess(IPersonalAssetDataAccess):
    '''EasyEquities-related functionality.'''

    def __init__(self, resource_data_access: IResourcesDataAccess, username: str, password: str):
        self.resource_data_access = resource_data_access
        self.client = EasyEquitiesClient()
        self.username = username
        self.password = password

    def __get_accounts__(self) -> list:
        info(f'Signing into EasyEquities as "{self.username}".')
        self.client.login(username=self.username, password=self.password)
        
        return self.client.accounts.list()

    def __get_account_by_name__(self, account_name: str) -> Account:
        accounts: list = self.__get_accounts__()
        
        debug(f'Filtering accounts list by name "{account_name}".')
        return [a for a in accounts if a.name == account_name][0]

    def __get_account_holdings__(self, account_name: str) -> list:
        account: Account = self.__get_account_by_name__(account_name=account_name)
        
        info(f'Getting account holdings for account "{account.name}" ({account.id}).')
        return self.client.accounts.holdings(account.id, include_shares=True)

    def __get_account_valuation__(self, account_name: str) -> list:
        account: Account = self.__get_account_by_name__(account_name=account_name)
        
        info(f'Getting account valuation for account "{account.name}" ({account.id}).')
        return self.client.accounts.valuations(account.id)

    def get_supported_assets(self) -> list:
        '''Get all supported asset names and symbols.'''

        info('Fetching EasyEquities supported symbols from a static source.')

        with self.resource_data_access.get_resource(path='easy_equities_us_stocks.json') as file:
            return json.load(file)

    def get_personal_transactions(self) -> list:
        '''Get all personal transactions made on an EasyEquities account.'''

        return {
            'TSLA': {
                'name': 'Tesla Inc.',
                'symbol': 'TSLA',
                'transactions': [
                    { 'value': 0.0688, 'date': datetime(2022, 7, 28, 0, 0) }
                ]
            },
            'AAPL': {
                'name': 'Apple Inc.',
                'symbol': 'AAPL',
                'transactions': [
                    { 'value': 0.4317, 'date': datetime(2022, 7, 1, 0, 0) }
                ]
            },
            'DDD': {
                'name': '3D Systems Corporation',
                'symbol': 'DDD',
                'transactions': [
                    { 'value': 8.8925, 'date': datetime(2022, 8, 5, 0, 0) }
                ]
            },
            'SBSW': {
                'name': 'Sibanye Stillwater Ltd',
                'symbol': 'SBSW',
                'transactions': [
                    { 'value': 1.1265, 'date': datetime(2022, 8, 5, 0, 0) }
                ]
            },
        }
