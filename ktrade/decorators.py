from functools import wraps
from flask import redirect, url_for
from ktrade.models import Configuration

def check_configured(f):
  @wraps(f)
  def decorated_function(*args, **kwards):
    count = Configuration.query.count()
    if (count == 0):
      return redirect('/initial_setup')

    return f(*args, **kwargs)

  return decorated_function
