import datetime
from Core.dbconn import get_database_connection


def delete_influencer_account_with_mail_address_from_database(mailaddress: str):
    """

    :param mailaddress:
    :return:
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""DELETE FROM influencer WHERE email=%s""", (mailaddress,))

    dbconnection.commit()

    cursor.close()
    dbconnection.close()


def use_db_connection(function):
    """

    :param function:
    :return:
    """

    def inner(mail, placeholder=None):
        """

        :param mail:
        :param placeholder:
        :return:
        """
        dbconnection = get_database_connection()
        cursor = dbconnection.cursor()

        function(mail, cursor)

        dbconnection.commit()

        cursor.close()
        dbconnection.close()

    return inner


@use_db_connection
def delete_instagram_entry(mail: str, cursor=None):
    """

    :param mail:
    :param cursor:
    :return:
    """
    cursor.execute("DELETE FROM is_listed_on_instagram WHERE influencer_identifier IN (SELECT influencer_identifier "
                   "FROM influencer WHERE email = %s);", (mail,))


@use_db_connection
def delete_facebook_entry(mail: str, cursor=None):
    """

    :param mail:
    :param cursor:
    :return:
    """
    cursor.execute("DELETE FROM is_listed_on_facebook WHERE influencer_identifier IN (SELECT influencer_identifier "
                   "FROM influencer WHERE email = %s);", (mail,))


@use_db_connection
def delete_youtube_entry(mail: str, cursor=None):
    """

    :param mail:
    :param cursor:
    :return:
    """
    cursor.execute("DELETE FROM is_listed_on_youtube WHERE influencer_identifier IN (SELECT influencer_identifier "
                   "FROM influencer WHERE email = %s);", (mail,))


@use_db_connection
def delete_pinterest_entry(mail: str, cursor=None):
    """

    :param mail:
    :param cursor:
    :return:
    """
    cursor.execute("DELETE FROM is_listed_on_pinterest WHERE influencer_identifier IN (SELECT influencer_identifier "
                   "FROM influencer WHERE email = %s);", (mail,))


@use_db_connection
def delete_personal_blog_entry(mail: str, cursor=None):
    """

    :param mail:
    :param cursor:
    :return:
    """
    cursor.execute(
        "DELETE FROM is_listed_on_personal_blog WHERE influencer_identifier IN (SELECT influencer_identifier "
        "FROM influencer WHERE email = %s);", (mail,))


@use_db_connection
def delete_company_profile(mail, cursor=None):
    """

    :param mail:
    :param cursor:
    :return:
    """
    cursor.execute("DELETE FROM company WHERE contact_email=%s;", (mail,))


def book_package(mail, package, duration=None):
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    if duration is not None:
        expr = calculate_expiration(duration)
    else:
        expr = None

    cursor.execute("""UPDATE company SET booked_package = %s, expire_date = %s WHERE contact_email = %s;""",
                   (package, expr, mail), )

    dbconnection.commit()

    cursor.close()
    dbconnection.close()


def calculate_expiration(months):
    import datetime
    return (datetime.datetime.now() + datetime.timedelta(days=30 * months)).date()


def get_all_reported_profiles() -> list:
    """

    :return: List that contains dictionaries as datastructures for each report-entry od the db
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""
    SELECT * FROM reported_influencers 
        JOIN report_reasons rr 
            on reported_influencers.report_reason_identifier = rr.report_reason_identifier 
        JOIN influencer i 
            on reported_influencers.influencer_identifier = i.influencer_identifier
    WHERE ignored = 0;""")

    entries = cursor.fetchall()
    keys = cursor.column_names

    cursor.close()
    dbconnection.close()

    return_list = []
    for entry in entries:
        temp_dict = {}
        for index in range(0, len(keys)):
            temp_dict[keys[index]] = entry[index]
        return_list.append(temp_dict)

    return return_list


def ignore_reported_influencer_db_execution(report_identifier) -> bool:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""
    UPDATE reported_influencers SET ignored = 1 WHERE report_identifier = %s;
    """, (report_identifier,))

    dbconnection.commit()
    cursor.close()
    dbconnection.close()

    return True


def delete_influencer_with_id(influencerIdentifier: int) -> bool:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""
    DELETE FROM influencer WHERE influencer_identifier = %s""", (influencerIdentifier,))

    dbconnection.commit()
    cursor.close()
    dbconnection.close()

    return True
