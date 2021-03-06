from flask import g
import os
import redis

_db_config = None # Holds database config

def init(app):
    """ Function must be called to initalize this module """

    global _db_config
    global close_connection
#   _db_config = app.config['DATABASE']
#    Manually apply @app.teardown_appcontext decorator
#    close_connection = app.teardown_appcontext(close_connection)

def _datastore_connect():
#    if _db_config is None:
#        raise Exception('Call init first') # or whatever error you want
    try:
        if 'PYCHARM_HOSTED'  in os.environ.keys():
            redis_db = redis.StrictRedis(host='127.0.0.1', port=7379, db=10, charset="utf-8", decode_responses=True)
            return redis_db
        else:
            return redis.StrictRedis(host='dev-cockpit-redis', port=6379,  db=10, charset="utf-8", decode_responses=True)
    except:
        print ("ERROR cannot conenct to redis")
        raise

def get_datastore():
    datastore  = getattr(g, '_datastore', None)
    if datastore is None:
        datastore = g._datastore = _datastore_connect()
    return datastore

def close_connection(exception):
    datastore = getattr(g, '_datastore', None)
    if datastore is not None:
# TODO close and cleanup redis connection, is there anything to do
        print ("Close the connection")