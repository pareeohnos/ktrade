"""Creating thread safe and managed sessions using SQLAlchemy.

The sessions that are created are expected to be:
- thread safe
- handle committing
- handle rolling back on errors
- handle session removal/releasing once context or thread is closed.

Author: Nitish Reddy Koripalli
License: MIT

# Resources for creating thread safe sessions.
SOURCE: https://docs.sqlalchemy.org/en/latest/orm/session_basics.html#getting-a-session
SOURCE: https://docs.sqlalchemy.org/en/latest/orm/contextual.html#unitofwork-contextual
SOURCE: https://stackoverflow.com/questions/21078696/why-is-my-scoped-session-raising-an-attributeerror-session-object-has-no-attr

################################################################################
# Documentation & Motivations for this entire module.
################################################################################

#######################################
# Motivations
#######################################
* What we would like to have is a unified way to get a database session in order to make transactions with the database.
* At this very moment we are not interested in the techinical details of the interactions our code has with the database.
  What we want is a way to interact with a way without worrying about:
  - thread safety
  - memory leaks i.e. not returning connections to the connection pools etc.
* Finally we would want a method that returns a database session object that inherently takes care of the above concerns
  without the user having to take care of those concerns.
* Although it is not enforced by SQLAlchemy, it does recommended to separate individual db operations from session
  creation. That is, it recommends not create sessions right next to where you make a single database query.
  We will try to follow this pattern recommendation blindly.
* We want a universal database session creation for offline and online (flask) applications.

#######################################
# Implementation & Notes
#######################################
* SQLAlchemy provides the sessionmaker function which generates a new Session object whenever it is called.
  The recommended way to use it is to have a global variable that has a configured sessionmaker object which can
  then be used by other parts of the application to create sessions.
  ```
  session_factory = sessionmaker(bind=engine)
  session = session_factory()  # This can be called from elsewhere in the application.
  ```
  However the sessionmaker does not generate Sessions that are meant to be used in a multi-threaded way for example in
  a webserver.

  You can release resources for such a session by using `session.close()`.

* In order to abstract away thread handling from the user, SQLAlchemy provides scoped_session functionality, that
  maintains a session per thread registry. That is, (if I'm not mistaken) scoped_session always maintain one session per
  threading.local(). If somehow in the same thread, we created a new session using scoped_session, it will return
  the same session object unless the session object has been explicity removed/closed in between.
  The recommended way to use it is to have a global variable that has a configured scoped_session object which can
  then be used by other parts of the application to create sessions.
  ```
  thread_safe_session_factory = scoped_session(sessionmaker(bind=engine))
  session = thread_safe_session_factory()  # This can be called from elsewhere in the application from any thread.
  ```
  You can release resources for such a session by using `thread_safe_session_factory.remove()` and not `session.remove()`
  since `thread_safe_session_factory` maintains the registry.

* Finally we provided a ManagedSession function that returns thread safe sessions and takes care committing, closing,
  removing and rolling back the session on errors. We expect the ManagedSession to be used as follows:
  ```
  with ManagedSession() as session:            # multiple db_operations are done within one session.
      db_operations.select(session, **kwargs)  # db_operations is expected not to worry about session handling.
      db_operations.insert(session, **kwargs)  # after the with statement, the session commits to the database.
  ```
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
import contextlib

engine = None
thread_safe_session_factory = None


def init_engine(uri, **kwargs):
    """Initialize the engine.

    Args:
        uri (str): The string database URI. Examples:
            - sqlite:///database.db
            - postgresql+psycopg2://username:password@0.0.0.0:5432/database
    """
    global engine
    if engine is None:
        engine = create_engine(uri, **kwargs)
    return engine


def init_session_factory():
    """Initialize the thread_safe_session_factory."""
    global engine, thread_safe_session_factory
    if engine is None:
        raise ValueError("Initialize engine by calling init_engine before calling init_session_factory!")
    if thread_safe_session_factory is None:
        thread_safe_session_factory = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
    return thread_safe_session_factory


@contextlib.contextmanager
def ManagedSession():
    """Get a session object whose lifecycle, commits and flush are managed for you.

    Expected to be used as follows:
    ```
    with ManagedSession() as session:            # multiple db_operations are done within one session.
        db_operations.select(session, **kwargs)  # db_operations is expected not to worry about session handling.
        db_operations.insert(session, **kwargs)  # after the with statement, the session commits to the database.
    ```
    """
    global thread_safe_session_factory
    if thread_safe_session_factory is None:
        raise ValueError("Call init_session_factory before using ManagedSession!")
    session = thread_safe_session_factory()
    try:
        yield session
        session.commit()
        session.flush()
    except Exception:
        session.rollback()
        # When an exception occurs, handle session session cleaning,
        # but raise the Exception afterwards so that user can handle it.
        raise
    finally:
        # source: https://stackoverflow.com/questions/21078696/why-is-my-scoped-session-raising-an-attributeerror-session-object-has-no-attr
        thread_safe_session_factory.remove()
