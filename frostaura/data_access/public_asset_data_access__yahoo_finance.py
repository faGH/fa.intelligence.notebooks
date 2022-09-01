'''This module defines Yahoo Finance data access components.'''
import yfinance as yf
import swifter
import pandas as pd
from logging import info, warning
from frostaura.data_access.public_asset_data_access import IPublicAssetDataAccess
from frostaura.models.symbol_data import SymbolData

class YahooFinanceDataAccess(IPublicAssetDataAccess):
    '''Yahoo Finance public asset-related functionality.'''

    def __init__(self, config: dict = {}):
        self.config = config

    def get_symbol_history(self, symbol: str) -> pd.DataFrame:
        '''Get historical price movements for a given symbol.'''

        info(f'Fetching historical price movements for symbol "{symbol}".')

        ticker = yf.Ticker(symbol)
        value = ticker.history(period='max')

        return value

    def augment_symbols_info(self, symbols: pd.DataFrame) -> pd.DataFrame:
        '''Add info to a daraframe containing symbols.'''
        __symbols__: pd.DataFrame = symbols.copy()

        def async_apply(symbol: str) -> object:
            ticker = yf.Ticker(symbol)
            stats = ticker.stats()
            ticker_info = ticker.info
            analysis = ticker.analysis

            if not 'longName' in ticker_info:
                warning(f'No longName key found in info for symbol "{symbol}". Info Type: {type(ticker_info)}, Info: {ticker_info}')
                return None

            data = {
                'company_name': ticker_info['longName'],
                'annual_dividend_percentage': ticker_info['dividendYield'],
                'eps_ttm': ticker_info['trailingEps'],
                'current_price': ticker_info['previousClose'],
                'pe_ratio': ticker_info['forwardPE']
            }

            if stats is not None:
                data['shares_outstanding'] = stats['defaultKeyStatistics']['sharesOutstanding']
                data['free_cash_flow'] = stats['financialData']['freeCashflow']
            else:
                data['shares_outstanding'] = None
                data['free_cash_flow'] = None

            if analysis is not None:
                data['future_growth_rate'] = analysis.loc['+5Y']['Growth']
            else:
                data['future_growth_rate'] = None

            return data

        __symbols__['info'] = __symbols__['symbol'].swifter.apply(async_apply)
        __symbols__['company_name'] = __symbols__['info'].apply(lambda i: i['company_name'])
        __symbols__['annual_dividend_percentage'] = __symbols__['info'].apply(lambda i: i['annual_dividend_percentage'])
        __symbols__['eps_ttm'] = __symbols__['info'].apply(lambda i: i['eps_ttm'])
        __symbols__['current_price'] = __symbols__['info'].apply(lambda i: i['current_price'])
        __symbols__['pe_ratio'] = __symbols__['info'].apply(lambda i: i['pe_ratio'])
        __symbols__['shares_outstanding'] = __symbols__['info'].apply(lambda i: i['shares_outstanding'])
        __symbols__['free_cash_flow'] = __symbols__['info'].apply(lambda i: i['free_cash_flow'])
        __symbols__['future_growth_rate'] = __symbols__['info'].apply(lambda i: i['future_growth_rate'])

        return __symbols__.drop(['info'], axis=1)

    def get_symbol_data(self, symbol: str) -> SymbolData:
        '''Get detailed information about a given symbol.'''

        info(f'Fetching historical price movements for symbol "{symbol}".')
        ticker = yf.Ticker(symbol)
        stats = ticker.stats()
        analysis = ticker.analysis
        future_growth_rate: float = analysis.loc['+5Y']['Growth']
        shares_outstanding: float = stats['defaultKeyStatistics']['sharesOutstanding']
        free_cash_flow: float = stats['financialData']['freeCashflow']
        company_name: str = ticker.info['longName']
        annual_dividend_percentage: float = ticker.info['dividendYield']
        eps_ttm: float = ticker.info['trailingEps']
        current_price: float = ticker.info['previousClose']
        pe_ratio: float = ticker.info['forwardPE']
        value: SymbolData = SymbolData(free_cash_flow=free_cash_flow,
                                        future_growth_rate=future_growth_rate,
                                        shares_outstanding=shares_outstanding,
                                        symbol=symbol,
                                        company_name=company_name,
                                        annual_dividend_percentage=annual_dividend_percentage,
                                        eps_ttm=eps_ttm,
                                        current_price=current_price,
                                        pe_ratio=pe_ratio)

        return value
