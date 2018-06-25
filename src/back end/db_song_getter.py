import pyodbc
import numpy as np


def get_specific_parameters(parameter_list):
    print('Hole spezifische Parameter aus der Datenbank...')
    server = 'mrd.database.windows.net'
    database = 'mrd'
    username = 'qaywsx'
    password = 'w@970881'
    connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                                server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = connection.cursor()
    param = "SELECT "
    for i in range(0, len(parameter_list) - 1):
        param += parameter_list[i] + ','
    param += parameter_list[-1] + " FROM songs"
    cursor.execute(param)
    ret = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return ret


def get_all_ids():
    print('Hole alle IDs aus der Datenbank...')
    server = 'mrd.database.windows.net'
    database = 'mrd'
    username = 'qaywsx'
    password = 'w@970881'
    connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                                server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = connection.cursor()
    ids = "SELECT id FROM songs"
    cursor.execute(ids)
    ret = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return ret


def get_all_songinfos(ids2test=None):
    print('Hole alle Song-Infos aus der Datenbank...')
    server = 'mrd.database.windows.net'
    database = 'mrd'
    username = 'qaywsx'
    password = 'w@970881'
    connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                                server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = connection.cursor()
    info_sql = "SELECT id,loudness,hotttnesss,tempo,timeSig,songkey,mode,label FROM songs"
    if ids2test is not None:
        info_sql += " WHERE "
        for l in range(0, len(ids2test)-1):
            info_sql += "id='" + ids2test[l] + "' OR "
        info_sql += "id='" + ids2test[len(ids2test)-1] + "'"
    cursor.execute(info_sql)
    ret = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return ret


def get_all_centroids():
    print('Hole alle Centroids aus der Datenbank...')
    server = 'mrd.database.windows.net'
    database = 'mrd'
    username = 'qaywsx'
    password = 'w@970881'
    connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' +
                                server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
    cursor = connection.cursor()
    param = "SELECT loudness,hotttnesss,tempo,timeSig,songkey FROM centroids"
    cursor.execute(param)
    ret = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return ret
