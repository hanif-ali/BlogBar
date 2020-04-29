import mysql.connector


# database_connection = mysql.connector.connect(host="116.203.87.185",
#                                               database="BlogBar",
#                                               user="develop",
#                                               password="testingpw")


def get_database_connection() -> any:
    return mysql.connector.connect(
        host="116.203.87.185",
        database="BlogBar",
        user="develop",
        password="testingpw"
    )
