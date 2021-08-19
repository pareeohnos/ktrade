from ktrade.models import Configuration

def is_configured():
    count = Configuration.query.count()
    return count != 0