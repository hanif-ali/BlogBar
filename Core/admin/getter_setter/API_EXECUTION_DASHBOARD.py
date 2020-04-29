from Core.dbconn import get_database_connection


def get_dates():
    dates = []
    for i in [7, 6, 5, 4, 3, 2, 1, 0]:
        dates.append(get_date_of_timedelta(i))

    return dates


def get_signup_data_sevendays_influencer():
    dbconnection = get_database_connection()

    cursor = dbconnection.cursor()

    cursor.execute("""
    SELECT DATE(created_on), COUNT(*) AS amount
    FROM influencer
    WHERE DATE(created_on) >= (DATE(NOW()) - INTERVAL 7 DAY)
    GROUP BY DATE(created_on)
    ORDER BY DATE(created_on) ASC;
    """)

    results = cursor.fetchall()
    keys = cursor.column_names

    cursor.close()
    dbconnection.close()

    temp = {}

    dates = []
    for i in [7, 6, 5, 4, 3, 2, 1, 0]:
        dates.append(get_date_of_timedelta(i))

    if len(results) == 0:
        return None

    if len(results) == 0 or results is None:
        pass

    for i in range(0, len(results)):
        temp[results[i][0]] = results[i][1]

    return_dict = {}
    for date in dates:
        return_dict[date] = temp.get(date, 0)

    return return_dict


def get_signup_data_today_influencer():
    dbconnection = get_database_connection()

    cursor = dbconnection.cursor()

    cursor.execute("""
    SELECT HOUR(created_on), COUNT(*)
    FROM influencer
    WHERE DATE(created_on) = DATE(NOW())
    GROUP BY HOUR(created_on);
    """)

    results = cursor.fetchall()

    if len(results) == 0 or results is None:
        return_dict = {}
        for i in range(0, 24):
            return_dict[i] = 0

    temp_dict = {}
    for entry in results:
        temp_dict[str(entry[0])] = entry[1]

    return_dict = {}
    for i in range(0, 24):
        return_dict[i] = temp_dict.get(str(i), 0)

    return return_dict


def get_signup_data_sevendays_company():
    dbconnection = get_database_connection()

    cursor = dbconnection.cursor()

    cursor.execute("""
    SELECT DATE(created_on), COUNT(*) AS amount
    FROM company
    WHERE DATE(created_on) >= (DATE(NOW()) - INTERVAL 7 DAY)
    GROUP BY DATE(created_on)
    ORDER BY DATE(created_on) ASC;
    """)

    results = cursor.fetchall()
    keys = cursor.column_names

    cursor.close()
    dbconnection.close()

    if len(results) == 0:
        return None

    if len(results) == 0 or results is None:
        return [0, 0, 0, 0, 0, 0, 0]  # Does this fix the issue?

    # temp = []
    #
    # for i in range(0, len(results)):
    #     temp_dict = {}
    #     for k in range(0, len(keys)):
    #         temp_dict[keys[k]] = results[i][k]
    #
    #     temp.append(temp_dict)

    temp = {}

    for i in range(0, len(results)):
        temp[results[i][0]] = results[i][1]

    dates = []
    for i in [7, 6, 5, 4, 3, 2, 1, 0]:
        dates.append(get_date_of_timedelta(i))

    return_dict = {}
    for date in dates:
        return_dict[date] = temp.get(date, 0)

    return return_dict


def get_signup_data_today_company():
    dbconnection = get_database_connection()

    cursor = dbconnection.cursor()

    cursor.execute("""
    SELECT HOUR(created_on), COUNT(*)
    FROM company
    WHERE DATE(created_on) = DATE(NOW())
    GROUP BY HOUR(created_on);
    """)

    results = cursor.fetchall()

    if len(results) == 0 or results is None:
        return_dict = {}
        for i in range(0, 24):
            return_dict[i] = 0

    temp_dict = {}
    for entry in results:
        temp_dict[str(entry[0])] = entry[1]

    return_dict = {}
    for i in range(0, 24):
        return_dict[i] = temp_dict.get(str(i), 0)

    return return_dict


def get_kpis() -> dict:
    dbconnection = get_database_connection()

    cursor = dbconnection.cursor()

    cursor.execute("""SELECT * FROM kpi_dashboard;""")

    entries = cursor.fetchall();
    cursor.close()
    dbconnection.close()

    return_dict = {}
    for entry in entries:
        return_dict[entry[0]] = entry[1]

    return return_dict


def get_date_of_timedelta(daycount: int):
    import datetime
    return (datetime.datetime.now() - datetime.timedelta(days=daycount)).date()
