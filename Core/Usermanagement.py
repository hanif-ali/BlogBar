from Core.Exceptions.User import UserNotLoggedIn
from Core.dbconn import get_database_connection
from passlib.hash import bcrypt
import mysql
import random
from Core.mailing import send_double_opt_in_request


def get_rnd_str() -> str:
    """

    :return:
    """
    alphabeth = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "q", "r", "s",
                 "t", "u", "u", "v", "w", "x", "y", "z"]
    string = ""
    for i in range(0, 5):
        string += alphabeth[random.randint(0, len(alphabeth) - 1)]
    return string


def generate_pwd_key():
    """
    :return:
    """
    token = ""
    for i in range(0, 20):
        token += get_rnd_str()
        for i in range(0, 2):
            token += str(random.randint(0, 255))

    return token


def check_if_email_already_taken(email: str) -> bool:
    """
    This function is part of the Usermanagement and checks if a passed email is already used for authentication
    and known in the database

    :type email: String
    :return: Boolean that indicates the exiting of the email-address (passed as str-param) ==> True: mail exists already
    """
    dbconnection = get_database_connection()
    database_cursor = dbconnection.cursor()

    sql_parameterized_query = """SELECT * FROM mail_addresses WHERE mail = %s;"""

    database_cursor.execute(sql_parameterized_query, (email,))

    if database_cursor.fetchall():
        database_cursor.close()
        dbconnection.close()
        return True
    else:
        database_cursor.close()
        dbconnection.close()
        return False


def hash_password(pwd: str) -> str:
    """
    The returned hashValue is for storing a clear password pseudo-encrypted in the database

    :type pwd: String
    :return: String, which is the hash value of a passed string
    """
    return bcrypt.hash(pwd)  # TODO: check if this is a proper way of salting!


def verify_password(plain_text_password, hashed_password) -> bool:
    """
    :rtype: bool that is true if an appropriate password was passed
    """
    return bcrypt.verify(plain_text_password, hashed_password)


def create_user(lastName: str, firstName: str, mail: str, telephoneNumber: str, gender: int, birthyear: str, pwd: str,
                language_abbr: str) -> bool:
    """
    This function creates user (only influencer, no companies) by validating the input and translate ids to texts (for example: gender ID)

    :param lastName the input of the sign-Up-form with name=last_name (required)
    :param firstName the input of the sign-Up-form with name=first_name (required)
    :param email the input of the sign-Up-form with name=mail (required, Primary Key)
    :param telephoneNumber the input of the sign-Up-form with name=phone_number
    :param gender the input of the sign-Up-form with name=gender (select) TODO: Check if the option-values of the select-picker are equal to this internal identifiers
    :param birthyear the input of the sign-Up-form with name=birthyear
    :param pwd the input of the sign-Up-form with name=pwd or name=pwd-confirm (confirm them before). The pwd-param mustn't be hashed before.

    :rtype: bool, that confirms if the user was successfully added to the database
    """
    pwd_hash = hash_password(pwd)

    if check_if_email_already_taken(mail):
        raise Exception("email-address already taken")

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    sql_parameterized_query = """
    INSERT INTO influencer(last_name, first_name, email, phone_number, gender, birthyear, pwd_hash, language_abbr)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"""

    gen = 'male'
    if gender == "1":
        gen = 'male'
    elif gender == "2":
        gen = 'female'
    elif gender == "3":
        gen = "d"
    else:
        raise IndexError("Unknown gender-index: " + gender)

    cursor.execute(sql_parameterized_query,
                   (lastName, firstName, mail, telephoneNumber, gen, int(birthyear + "", 10), pwd_hash, language_abbr))
    dbconnection.commit()
    cursor.close()
    dbconnection.close()

    send_double_opt_in_request(mail, firstName, 1, language=language_abbr)

    return True  # TODO: check if the user really added successful!


def create_company_profile(companyName: str, contact: str, contactMail: str, streetWithHouseNumber: str, postcode: str,
                           place: str, pwd: str, ust_id: str, language_abbr: str) -> bool:
    """
    This functions creates a profile for a company (specified by the passed params.

    :param companyName the input of the sign-Up-form with name=companyName
    :param contact the input of the sign-Up-form with name=contact
    :param contactMail the input of the sign-Up-form with name=contactMail (must be unique in the database [view=mail_addresses])
    :param streetWithHouseNumber the input of the sign-Up-form with name=streetWithHouseNumber
    :param postcode the input of the sign-Up-form with name=postcode
    :param place the input of the sign-Up-form with name=place
    :param pwd the input of the sign-Up-form with name=pwd or pwd-confirm (Mustn't be hashed, but should be validated before profile-creation-call)
    :param ust_id 'Umsatzsteueridentifikationsnummer' for receipt and internal usage (not required)
    :rtype: bool, that confirms the sign-up (if it was successful)
    """
    pwd_hash = hash_password(pwd)

    if check_if_email_already_taken(contactMail):
        raise Exception("email-address already taken")

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    sql_parameterized_query = """
    INSERT INTO company(company_name, contact_person, contact_email, street_house_number, postcode, place, ust_id, pwd_hash, language_abbr)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    try:
        cursor.execute(sql_parameterized_query, (
        companyName, contact, contactMail, streetWithHouseNumber, postcode, place, ust_id, pwd_hash, language_abbr))
    except(mysql.connector.errors.DataError):
        raise Exception("Invalid UST-ID")

    dbconnection.commit()

    cursor.close()
    dbconnection.close()

    send_double_opt_in_request(contactMail, contact, 2, language=language_abbr)

    return True  # TODO: check if this is the correct way


def validate_data(mail: str, pwd: str) -> (bool, int, int):
    """
    !!! DEPRECATED !!!

    :param pwd The given password. This funtion verifies it using the sotred hash-value
    :param mail The input mail with name=mail of the sign-up-form
    :rtype: (bool, int, int) True: Login-Success The first int is the id of the company/influencer, the second int specifies the type: 0: Influencer, 1: company
            OR returns a (bool, str). The str is the error-string which tells the reason why the login wasnt successful
    """
    sql_parameterized_statement = """SELECT influencer_identifier, pwd_hash FROM influencer WHERE email=%s;"""

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(sql_parameterized_statement, (mail,))
    try:
        entry = cursor.fetchall()[0]
    except IndexError:
        pass
    if entry:
        if verify_password(pwd, entry[1]):
            return True, entry[0], 0
        else:
            return False, "Passwort falsch (Influencerkonto)"
    else:
        sql_parameterized_statement = """SELECT company_identifier, pwd_hash FROM company WHERE contact_email=%s;"""
        cursor.execute(sql_parameterized_statement, (mail,))
        try:
            entry = cursor.fetchall()[0]
            cursor.close()
            dbconnection.close()
        except:
            return False, "Mail-Adresse nicht vergeben."
        if entry:
            if verify_password(pwd, entry[1]):
                return True, entry[0], 1
            else:
                return False, "Passwort falsch (Unternehmenskonto)"
        else:
            return False, "Nutzerkonto mit der angegebenen Email-Adresse existiert nicht."


def validate_data_using_union_view(mail: str, pwd: str) -> (bool, int, int):
    """
    :param pwd The given password. This funtion verifies it using the sotred hash-value
    :param mail The input mail with name=mail of the sign-up-form
    :rtype: (bool, int, int) True: Login-Success The first int is the id of the company/influencer, the second int specifies the type: 0: Influencer, 1: company
            OR returns a (bool, str). The str is the error-string which tells the reason why the login wasnt successful
    """
    sql_parameterized_statement = """SELECT IDENTIFIER, PWD_HASH, KIND, CONFIRMED FROM sign_up_view WHERE MAIL=%s;"""

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(sql_parameterized_statement, (mail,))

    try:
        result = cursor.fetchall()
        cursor.close()
        dbconnection.close()

        try:
            if verify_password(pwd, result[0][1]):
                if result[0][3] == 1:
                    return True, result[0][0], result[0][2]
                else:
                    return False, "EMail-Addresse noch nicht bestätigt."  # ToDo: Language-specific-error-message-implementation is missing >> Add it here using the lang_abbr as third param
            else:
                return False, "Passwort ist nicht korrekt."  # ToDo: see above (lang-branching in error-msg)
        except IndexError:
            return False, "Es exisitert kein Konto für die gegebene EMail-Adresse."  # ToDo: see above (lang-branching in error-msg)

    except mysql.connector.errors.DataError:
        return False, "Error: Kontaktieren Sie bitte den technischen Support."  # ToDo: see above (lang-branching in error-msg)


def set_confirm_status_to_true(key: str) -> bool:
    """

    :param key:
    :return:
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""
    UPDATE influencer SET confirmed = True 
    WHERE email IN (SELECT email FROM confirm_keys WHERE token = %s );""", (key,))

    print(cursor.statement)

    cursor.execute("""
        UPDATE company SET confirmed = True 
        WHERE contact_email IN (SELECT email FROM confirm_keys WHERE token = %s );""", (key,))

    print(cursor.statement)

    dbconnection.commit()

    cursor.close()
    dbconnection.close()

    return True


def set_new_password(pwd, token):
    """

    :param pwd:
    :param token:
    :return:
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""
    UPDATE influencer SET pwd_hash = %s WHERE email IN (SELECT email FROM pwd_reset_tokens WHERE token = %s);""",
                   (hash_password(pwd), token))
    print(cursor.statement)

    dbconnection.commit()

    cursor.close()

    cursor = dbconnection.cursor()

    cursor.execute("""
        UPDATE company SET pwd_hash = %s WHERE contact_email IN (SELECT email FROM pwd_reset_tokens WHERE token = %s);""",
                   (hash_password(pwd), token))

    dbconnection.commit()
    cursor.close()

    dbconnection.close()

    return True


def get_subscription_package_of_company_with_identifier(company_identifier: int) -> str:
    """

    :param company_identifier: int
    :return: str
    """
    assert company_identifier is not None, UserNotLoggedIn

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""SELECT booked_package FROM company WHERE company_identifier = %s;""", (company_identifier,))

    result = cursor.fetchone()[0]

    cursor.close()
    dbconnection.close()

    return result


def report_influencer(influencer_identifier: int, contact_mail: str, reason_identifier: str, remark: str) -> None:
    """

    :param influencer_identifier:
    :param contact_mail:
    :param reason_identifier:
    :param remark:
    :return:
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    try:
        cursor.execute("""
            INSERT INTO reported_influencers(influencer_identifier, report_reason_identifier, contact_mail, remark)
            VALUES (%s, %s, %s, %s);
            """, (
            influencer_identifier,
            reason_identifier,
            contact_mail,
            remark
        )
                       )
    # ToDo: Alter the catching-conditions to catch just MySQL-Errors
    except:
        print("ERROR DURING INFLUENCER_PROFILE_REPORT")

    dbconnection.commit()
    cursor.close()
    dbconnection.close()
