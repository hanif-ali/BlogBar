from Core.dbconn import get_database_connection


def track_search(channel: str, package: str):
    try:
        dbconnection = get_database_connection()
        cursor = dbconnection.cursor()

        cursor.execute("""INSERT INTO searches(package, channel) VALUES (%s, %s);""", (package, channel))

        dbconnection.commit()
        cursor.close()
        dbconnection.close()
    except:
        pass
