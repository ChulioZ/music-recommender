import pyodbc
import numpy as np


server = 'mrd.database.windows.net'
database = 'mrd'
username = 'qaywsx'
password = 'w@970881'
connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                            server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = connection.cursor()


def get_all_parameters():
    param = "SELECT loudness,hotttnesss,tempo,timeSig,songkey,mode FROM songs"
    cursor.execute(param)
    paramResults = cursor.fetchall()
    return np.array(paramResults)


def get_all_ids():
    ids = "SELECT id FROM songs"
    cursor.execute(ids)
    return cursor.fetchall()


def get_all_songinfos(entered_ids=None, ids2test=None):
    info_sql = "SELECT id,loudness,hotttnesss,tempo,timeSig,songkey,mode,label FROM songs"
    if entered_ids is not None:
        info_sql += " WHERE label IN (SELECT label FROM songs WHERE "
        for i in range(0, len(entered_ids)-1):
            info_sql += "id='" + entered_ids[i] + "' OR "
        info_sql += "id='" + entered_ids[len(entered_ids)-1] + "')"
    if ids2test is not None:
        info_sql += " WHERE "
        for l in range(0, len(ids2test)-1):
            info_sql += "id='" + ids2test[l] + "' OR "
        info_sql += "id='" + ids2test[len(ids2test)-1] + "'"
    cursor.execute(info_sql)
    info_results = cursor.fetchall()
    return np.array(info_results)
