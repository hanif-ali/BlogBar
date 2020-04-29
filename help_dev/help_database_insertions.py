import mysql.connector
from Core.Usermanagement import hash_password
from random import Random

database_connection = mysql.connector.connect(host="116.203.87.185",
                                              database="BlogBar",
                                              user="develop",
                                              password="testingpw")

# with open("/Users/benwegener/Library/Mobile Documents/com~apple~CloudDocs/BlogBar/BlogBar-webapplication/help_dev/categories.txt", mode="r") as file:
#     cursor = database_connection.cursor()
#     for category in file.readlines():
#         cursor.execute("INSERT INTO topics(topic_name, topic_description) VALUES ('"+category+"', NULL)")
#         database_connection.commit()
#     cursor.close()

# with open("/Users/benwegener/Library/Mobile Documents/com~apple~CloudDocs/BlogBar/BlogBar-webapplication/help_dev/countries.txt", mode="r") as file:
#     cursor = database_connection.cursor()
#     for line in file.readlines():
#         param_str = """INSERT INTO countries(country_name) VALUES(%s);"""
#
#         cursor.execute(param_str, (line,))
#
#         database_connection.commit()
#
#     cursor.close()

random = Random()


def get_random_str() -> str:
    alphabeth = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "q", "r", "s", "t", "u", "u", "v", "w", "x", "y", "z"]
    string = ""
    for i in range(0,12):
        string += alphabeth[random.randint(0,len(alphabeth)-1)]
    return string


def get_random_email() -> str:
    return "{name}.{name2}@gmail.com".format(name=get_random_str(), name2=get_random_str())


def get_random_phone_number() -> str:
    number = ""
    for i in range(0,11):
        if i == 0:
            number += "0 "
        if i == 3:
            number += " "
        number += str(random.randint(0,9))

    return number


def get_random_birthyear() -> int:
    return random.randint(1980, 2007)


def get_random_price() -> int:
    return random.randint(100,399)


def get_random_gender() -> str:
    genders = ["male", "female"]

    return genders[random.randint(0,1)]

cursor = database_connection.cursor()

for i in range(0, 3000):
    cursor.execute("""INSERT INTO influencer(last_name, first_name, email, phone_number, price, gender, homebase, birthyear, pwd_hash)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                   (get_random_str(),get_random_str(),get_random_email(),get_random_phone_number(), get_random_price(),
                    get_random_gender(), get_random_str(), get_random_birthyear(), hash_password(get_random_str())))
    database_connection.commit()
    print("executed: " + str(i))

cursor.close()

# with open("/Users/benwegener/Library/Mobile Documents/com~apple~CloudDocs/BlogBar/BlogBar-webapplication/help_dev/ins.txt", mode="w") as file:
#     sql = """INSERT INTO influencer(last_name, first_name, email, phone_number, price, gender, homebase, birthyear, pwd_hash)
#                         VALUES """
#
#     for i in range(0, 2000):
#         print(i)
#         sql += """('{}','{}','{}','{}',{},'{}','{}',{},'{}')""".format(get_random_str(),get_random_str(),get_random_email(),get_random_phone_number(), get_random_price(),
#                         get_random_gender(), get_random_str(), get_random_birthyear(), hash_password(get_random_str()))
#
#         if i != 1999:
#             sql += ",\n"
#         else:
#             sql += ";"
#
#     file.write(sql)

print(get_random_email())