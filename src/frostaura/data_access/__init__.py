'''A convenience importing mechanism for all data access components.'''
from frostaura.data_access.resources_data_access import IResourcesDataAccess
from frostaura.data_access.resources_data_access__html import HtmlResourcesDataAccess
from frostaura.data_access.resources_data_access__embedded import EmbeddedResourcesDataAccess

from frostaura.data_access.public_asset_data_access import IPublicAssetDataAccess
from frostaura.data_access.public_asset_data_access__yahoo_finance import YahooFinanceDataAccess

from frostaura.data_access.personal_asset_data_access import IPersonalAssetDataAccess
from frostaura.data_access.personal_asset_data_access__easy_equities import EasyEquitiesPersonalAssetDataAccess

from frostaura.data_access.notifications_data_access import INotificationsDataAccess
from frostaura.data_access.notifications_data_access__telegram import TelegramNotificationsDataAccess
