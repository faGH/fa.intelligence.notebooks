'''This module defines Yahoo Finance data access components.'''
import yfinance as yf


class YahooFinanceDataAccess:
    '''Yahoo Finance-related functionality.'''

    def get_symbol_history(self, symbol: str):
        '''Get historical price movements for a given symbol.'''

        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='max')

        return hist
