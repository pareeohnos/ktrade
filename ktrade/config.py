from ktrade.models import Configuration
from sqlalchemy_utils import database_exists

def is_configured():
  """Check if KTrade has been configured.
  This will simply check for the existence of any configuration
  records in the database
  """
  try:
    count = Configuration.query.count()
    return count != 0
  except:
    return False

def configuration_for(key):
  """Retrieve the configuration value for a specified key"""

  try:
    return Configuration.query.filter_by(key=key).first()
  except:
    return None
