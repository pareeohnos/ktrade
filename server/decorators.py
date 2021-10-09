# -*- coding: utf-8 -*-

from functools import wraps
from flask import redirect, url_for
from server.config import is_configured

def check_configured(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if (not is_configured()):
      return redirect('/initial_setup')

    return f(*args, **kwargs)

  return decorated_function
