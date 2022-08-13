'''This module defines projection engine components.'''
import pandas as pd

class IAssetProjectionEngine:
    '''Component to perform functions related to asset projections.'''

    def project_daily_asset_growth(self,
                                   n_months: int,
                                   annual_growth_rate: float,
                                   principal_value: float,
                                   monthly_deposit: float) -> pd.DataFrame:
        '''Determine an asset's growth at a given annual rate over a specified number of months while applying a monthly deposit.'''

        raise NotImplementedError()
