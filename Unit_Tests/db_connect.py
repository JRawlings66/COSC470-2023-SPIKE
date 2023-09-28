import mysql.connector
from datetime import datetime
from mysql.connector import errorcode


def build_response(dname):
    try:
        conn = mysql.connector.connect(user='root',
                                       password='<censored>',
                                       host='localhost',
                                       database='<censored>',
                                       unix_socket='/var/run/mysqld/mysqld.sock')

    except mysql.connector.Error as err:

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    else:
        # primitive attempt at sanitization. At least make sure its alphanumeric only.
        if dname.isalnum() and dname != '':
            curs = conn.cursor(dictionary=True)
            sql_query = "SELECT DName FROM Devices WHERE DName = '{}' ".format(dname)
            curs.execute(sql_query)
            device = curs.fetchone()

            if device is not None:
                # <censored>
                sql_query = "SELECT Temp FROM Temprature t, Devices d " \
                            "WHERE t.ID = d.DvcID AND d.DName = '{}' AND " \
                            "t.Date >=  NOW() - INTERVAL 10 MINUTE " \
                            "ORDER BY Temp " \
                            "DESC LIMIT 1;".format(dname)
                curs.execute(sql_query)
                temprature_dict = curs.fetchone()

                sql_query = "SELECT Hum FROM Humidity h, Devices d " \
                            "WHERE h.ID = d.DvcID AND d.DName = '{}' AND " \
                            "h.Date >=  NOW() - INTERVAL 10 MINUTE " \
                            "ORDER BY Hum " \
                            "DESC LIMIT 1;".format(dname)
                curs.execute(sql_query)
                humidity_dict = curs.fetchone()

                sql_query = "SELECT Pres FROM Pressure p, Devices d " \
                            "WHERE p.ID = d.DvcID AND d.DName = '{}' AND " \
                            "p.Date >=  NOW() - INTERVAL 10 MINUTE " \
                            "ORDER BY Pres " \
                            "DESC LIMIT 1;".format(dname)
                curs.execute(sql_query)
                pressure_dict = curs.fetchone()

                conn.close()

                if temprature_dict is not None:
                    current_temp = float(temprature_dict["Temp"])
                    current_temp = float("{:.1f}".format(current_temp / len(temprature_dict)))
                else:
                    current_temp = "No data"

                if humidity_dict is not None:
                    current_humi = float(humidity_dict["Hum"])
                    current_humi = int(current_humi / len(humidity_dict))
                else:
                    current_humi = "No data"

                if pressure_dict is not None:
                    current_pres = float(pressure_dict["Pres"])
                    current_pres = float("{:.2f}".format(current_pres / len(pressure_dict)))
                else:
                    current_pres = "No data"

                now = datetime.now()

                current_dict = [
                    {'Temp': current_temp, 'Pres': current_pres, 'Hum': current_humi,
                     'Time': now.strftime('%-I:%M')}]

                return current_dict
        # no device found
        return [{"error": "Invalid device."}]
    return [{"error": "Server error."}]