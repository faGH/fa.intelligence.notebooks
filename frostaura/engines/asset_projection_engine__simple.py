'''This module defines projection engine components.'''
import pandas as pd
from frostaura.engines.asset_projection_engine import IAssetProjectionEngine
from frostaura.engines.asset_valuation_engine import IAssetValuationEngine
from frostaura.models.valuation_result import ValuationResult
from frostaura.data_access.public_asset_data_access import IPublicAssetDataAccess

class SimpleAssetProjectionEngine(IAssetProjectionEngine):
    '''Calculations-related functionality using some maths under-the-hood.'''

    def __init__(self,
                 asset_valuation_engine: IAssetValuationEngine,
                 public_asset_data_access: IPublicAssetDataAccess,
                 config: dict = {}):
        self.asset_valuation_engine = asset_valuation_engine
        self.public_asset_data_access = public_asset_data_access
        self.config = config

    def project_monthly_asset_growth(self,
                                     n_months: int,
                                     symbol: str,
                                     principal_value: float,
                                     monthly_deposit: float = 0) -> pd.DataFrame:
        '''Determine an asset's growth at a given annual rate over a specified number of months while applying a monthly deposit.'''

        valuation: ValuationResult = self.asset_valuation_engine.valuate(symbol=symbol)
        annual_growth_rate: float = valuation.eps_five_years
        divident_payout_frequency_in_months: int = None # TODO: Determine this from YahooFinance (public_asset_data_access.get_dividend_payout_frequency_in_months)
        data = {
            'month': list(),
            'deposits_withdrawals': list(),
            'interest': list(),
            'total_deposits_withdrawals': list(),
            'accrued_interest': list(),
            'balance': list()
        }

        data['month'].append(0)
        data['deposits_withdrawals'].append(0)
        data['interest'].append(0)
        data['total_deposits_withdrawals'].append(0)
        data['accrued_interest'].append(0)
        data['balance'].append(principal_value)

        for i in range(1, n_months + 1):
            data['month'].append(i)
            data['deposits_withdrawals'].append(monthly_deposit)
            data['interest'].append((annual_growth_rate / 12) * data['balance'][-1])

            if divident_payout_frequency_in_months is not None and i % divident_payout_frequency_in_months == 0:
                annual_dividend_rate: float = valuation.annual_dividend_percentage / 100
                data['interest'].append((annual_dividend_rate / 12 / divident_payout_frequency_in_months) * data['balance'][-1])

            data['accrued_interest'].append(data['accrued_interest'][-1] + data['interest'][-1])
            data['total_deposits_withdrawals'].append(data['total_deposits_withdrawals'][-1] + monthly_deposit)
            data['balance'].append(data['interest'][-1] + data['balance'][-1] + monthly_deposit)

        response: pd.DataFrame = pd.DataFrame(data)

        return response.set_index('month')

    def project_monthly_holdings_growth(self,
                                   n_months: int,
                                   holdings_with_profits: pd.DataFrame,
                                   monthly_deposits: list) -> pd.DataFrame:
        '''Determine a comprehensive holdings growth at a given annual rates over a specified numbers of months while applying a monthly deposits.'''

        annual_growth_rates: list = list()
        principal_values: list = list()
        symbols: list = list()

        for row_index, row in holdings_with_profits.iterrows():
            symbol_valuation: ValuationResult = self.asset_valuation_engine.valuate(symbol=row['symbol'])
            annual_growth_rate: float = symbol_valuation.eps_five_years

            if symbol_valuation.annual_dividend_percentage is not None:
                annual_growth_rate += (symbol_valuation.annual_dividend_percentage / 100)

            annual_growth_rates.append(annual_growth_rate)
            principal_values.append(row['total_current_usd'])
            symbols.append(row['symbol'])

        projections: list = list()

        for month_index in range(len(annual_growth_rates)):
            projection = self.project_monthly_asset_growth(n_months=n_months,
                                                           symbol=symbols[month_index],
                                                           principal_value=principal_values[month_index],
                                                           monthly_deposit=monthly_deposits[month_index])

            projections.append(projection)

        data = {
            'month': list(),
            'deposits_withdrawals': list(),
            'interest': list(),
            'total_deposits_withdrawals': list(),
            'accrued_interest': list(),
            'balance': list()
        }

        for month_index in range(1, n_months + 1):
            data['month'].append(month_index)
            data['deposits_withdrawals'].append(sum([p.loc[month_index]['deposits_withdrawals'] for p in projections]))

            previous_row_balances: float = sum([p.loc[month_index - 1]['balance'] for p in projections])
            current_row_balances: float = sum([p.loc[month_index]['balance'] for p in projections])
            current_deposits: float = sum([p.loc[month_index]['deposits_withdrawals'] for p in projections])
            interest = 1 - previous_row_balances / (current_row_balances - current_deposits)

            data['interest'].append(interest)
            data['total_deposits_withdrawals'].append(sum([p.loc[month_index]['total_deposits_withdrawals'] for p in projections]))
            data['accrued_interest'].append(sum([p.loc[month_index]['accrued_interest'] for p in projections]))
            data['balance'].append(sum([p.loc[month_index]['balance'] for p in projections]))

        return pd.DataFrame(data)
