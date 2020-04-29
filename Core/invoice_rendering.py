import random

from Core.dbconn import get_database_connection
from Core.mailing import generate_pwd_reset_token, get_random_string


def genrate_invoice_token() -> str:
    """

    :return: token that identifies the invoice for download
    """
    token = ""
    for i in range(0, 6):
        token += get_random_string()
        for i in range(0, 2):
            token += str(random.randint(0, 255))
    print("Length of token: >> " + str(len(token)))
    return token


def create_invoice_db_entry(customer_id: int, booked_package_description: str, booked_package_duration_in_months: int,
                            booked_total_amount: float, token: str) -> None:
    """
    This function creates an db-entry that contains all neceesary information about the package-booking to render the
    invoice in future.

    :param customer_id: required to join the company table with the invoice-data (to get all information for
    pdf-rendering like the address or USt.-Id of the customer (in this case only companies))
    :param booked_package_description: This is a part of the description which is shown on the invoice
    :param booked_package_duration_in_months: the description on the invoice is composed out od this field-entry and the
     package name
    :param booked_total_amount: the total_amount is also used to compute the amount excluding taxes and for computing
     the tax-amount
    :return: /
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    print(token)

    cursor.execute("""
    INSERT INTO invoice_data(token, company_identifier, booked_package_description, 
    booked_package_duration_in_month, booked_package_total_amount) 
    VALUES(%s, %s, %s, %s, %s)
    """, (
        token,
        customer_id,
        booked_package_description,
        booked_package_duration_in_months,
        booked_total_amount
    ))

    dbconnection.commit()
    cursor.close()
    dbconnection.close()


def get_data_of_invoice_with_uuid(uuid: str) -> dict:
    """

    :param uuid:
    :return:
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    print("The UUID is. >>" + uuid)

    cursor.execute("""
    SELECT invoice_number_asc, DATE(booked_date), booked_package_description, 
    booked_package_duration_in_month, booked_package_total_amount, company_name, contact_person, street_house_number, postcode, place, language_abbr
     FROM invoice_data JOIN company c on invoice_data.company_identifier = c.company_identifier WHERE token = %s
    """, (
        uuid,
    ))

    print(cursor.statement)

    keys = cursor.column_names
    result = cursor.fetchall()[0]

    if result:
        return_dict = {}
        for i in range(0, len(keys)):
            return_dict[keys[i]] = result[i]
    else:
        print(result)
    cursor.close()
    dbconnection.close()

    return return_dict


def get_book_confirmation_mailing_data_usind_the_uuid(uuid: str) -> dict:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""
    SELECT company_name, contact_person, contact_email, booked_package, expire_date, token, booked_date,
     booked_package_duration_in_month, booked_package_total_amount, language_abbr FROM company
        JOIN invoice_data id on company.company_identifier = id.company_identifier
    WHERE token = %s;
    """, (
        uuid,
    ))

    keys = cursor.column_names
    invoice_entry = cursor.fetchone()

    cursor.close()
    dbconnection.close()

    # TODO: Implement a check if entry was found
    return_dict = {}
    for index in range(0, len(keys)):
        return_dict[keys[index]] = invoice_entry[index]

    return return_dict
