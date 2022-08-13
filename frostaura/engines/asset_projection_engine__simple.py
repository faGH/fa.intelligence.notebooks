'''This module defines projection engine components.'''
from logging import debug
import pandas as pd
from frostaura.engines.asset_projection_engine import IAssetProjectionEngine

class SimpleAssetProjectionEngine(IAssetProjectionEngine):
    '''Calculations-related functionality using some maths under-the-hood.'''

    def project_monthly_asset_growth(self,
                                     n_months: int,
                                     annual_growth_rate: float,
                                     principal_value: float,
                                     monthly_deposit: float = 0) -> pd.DataFrame:
        '''Determine an asset's growth at a given annual rate over a specified number of months while applying a monthly deposit.'''

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
            data['accrued_interest'].append(data['accrued_interest'][-1] + data['interest'][-1])
            data['total_deposits_withdrawals'].append(data['total_deposits_withdrawals'][-1] + monthly_deposit)
            data['balance'].append(data['interest'][-1] + data['balance'][-1] + monthly_deposit)

        return pd.DataFrame(data)
