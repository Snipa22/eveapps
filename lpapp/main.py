from DBUtils.PooledDB import PooledDB
import mysql.connector
pool_size = 20
pool = PooledDB(mysql.connector, pool_size, database='eve', user='eve', host='192.168.134.114', pass='JQ8YtqaFPtMq91UJeF1KgqYD')


def before_request():
    g.dbconn = pool.connection()

def teardown_request(exception):
    g.dbconn.close()
