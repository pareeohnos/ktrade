import logging
from ktrade.models import Account
from db_manager import ManagedSession

log = logging.getLogger(__name__)

class AccountSummaryActions:
  """
  Provides actions for handling responses from the TWS
  client related to account details
  """

  def call(self, account: str, value: str, tag: str):
    """
    Handles the response of an account summary request. This will attempt
    to find the existing account in the database, and if present update
    it. If one is not found, it will create a new one
    """
    log.debug("[IB] Account summary received")

    if tag == "NetLiquidationByCurrency":
      self.account_summary_received(account, float(value))


  def account_summary_received(self, number: str, value: float):
    """
    Updates the total value of the account. This will be used
    for calculating the correct position size
    """
    with ManagedSession() as session:
      account = Account.find_by(session, number=number)

      if account is None:
        account = Account(number=number)
        session.add(account)

      account.total_size = value