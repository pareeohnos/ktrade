from functools import wraps
from flask import g, request, redirect, url_for
from ktrade.models import Configuration

def check_required(f):
  @wraps(f)
  def decorated_function(*args, **kwards):
    count = Configuration.query.count()
    print f'COUNT {count}'
    if count == 0
      return redirect(url_for('initial_setup'))

    return f(*args, **kwargs)

  return decor
