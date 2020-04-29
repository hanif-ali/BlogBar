import os

from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename

from Core.API.API_Execution import delete_public_campaign_with_identifier
from Core.Exceptions.Search import CampaignDoesNotExist
from Core.Option_values import get_logo_path_of_company_with_identifier
from Core.dbconn import get_database_connection
from Core.search import tuple_of_list


def add_public_campaign(company_identifier: int, passed_params: ImmutableMultiDict, passed_files) -> bool:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()
    try:
        cursor.execute("""
        INSERT INTO company_offers_campaign(company_identifier, campaign_title, campaign_description, topic, format, remuneration)
        VALUES(%s, %s, %s, %s, %s, %s);""", (
            company_identifier,
            passed_params.get(
                "campaign_name"
            ),
            passed_params.get(
                "campaign_description"
            ),
            passed_params.get(
                "topic"
            ),
            passed_params.get(
                "format"
            ),
            passed_params.get(
                "remuneration"
            ),
        ))

        dbconnection.commit()
        cursor.close()
        dbconnection.close()

        insert_associated_channels_of_campaign(
            get_public_campaign_identifier(
                company_identifier,
                passed_params.get(
                    "campaign_name"
                )
            ),
            passed_params.getlist(
                "channels"
            )
        )

        DIR = "/root/webapplication/static/"
        UPLOAD_PDFS = "/root/webapplication/static/campaigns"

        if 'pdf_further_information' not in passed_files:
            print("NOT IN")
        else:
            campaign_identifier = str(
                get_public_campaign_identifier(
                    company_identifier,
                    passed_params.get(
                        "campaign_name"
                    )
                )
            )

            file = passed_files.get("pdf_further_information")
            file.filename = "details_campaign_reference_no_{0}".format(
                campaign_identifier
            )
            if file:
                filename = secure_filename(file.filename)

                for item in os.listdir(UPLOAD_PDFS):
                    if item.startswith("details_campaign_reference_no_{0}".format(campaign_identifier)):
                        try:
                            os.remove("{}/{}".format(UPLOAD_PDFS,
                                                     "details_campaign_reference_no_{0}".format(campaign_identifier)))
                        except:
                            pass
                file.save(
                    os.path.join(UPLOAD_PDFS, "details_campaign_reference_no_{0}.pdf".format(campaign_identifier)))
            else:
                print(file)
                print("NO FILE")

        return True
    except IndexError:
        return False


def get_public_campaign_identifier(company_identifier: int, campaign_title: str) -> any:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""
    SELECT campaign_identifier 
    FROM company_offers_campaign 
    WHERE company_identifier = %s 
        and campaign_title = %s;""", (company_identifier, campaign_title))
    try:
        result = cursor.fetchone()[0]
    except IndexError:
        result = None

    cursor.close()
    dbconnection.close()

    return result


def insert_associated_channels_of_campaign(campaign_identifier: int, channels: list) -> bool:
    insert_str = """INSERT INTO public_campaign_channels(campaign_identifier, channel_identifier) VALUES """
    values_str = """"""
    params_arr = []

    for channel in channels:

        values_str += """(%s, %s)"""
        params_arr.append(campaign_identifier)
        params_arr.append(channel)

        if channel is not channels[-1]:
            values_str += """, """

        else:
            values_str += """;"""

    insert_str += values_str

    if len(params_arr) > 0:
        prm_tuple = tuple(x for x in params_arr)

        dbconnection = get_database_connection()
        cursor = dbconnection.cursor()

        print(prm_tuple)
        print(insert_str)

        try:
            cursor.execute(insert_str, prm_tuple)

            dbconnection.commit()

            cursor.close()
            dbconnection.close()
            return True

        except:
            return False


def get_all_public_campaigns() -> list:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""
    SELECT DISTINCT company_offers_campaign.campaign_identifier, campaign_title, campaign_description,
                company_offers_campaign.company_identifier, topic_identifier, company_name, contact_email,
                contact_person, published_on
    FROM company_offers_campaign
        JOIN topics
            on topic_identifier = topic
        LEFT OUTER JOIN public_campaign_channels pcc
            on company_offers_campaign.campaign_identifier = pcc.campaign_identifier
        LEFT OUTER JOIN company c
            on company_offers_campaign.company_identifier = c.company_identifier 
    ORDER BY published_on DESC ;
    """)

    keys = cursor.column_names
    entries = cursor.fetchall()

    results = []

    if len(entries) > 0:
        for entry in entries:
            temp_dict = {}
            for index in range(0, len(keys)):
                temp_dict[keys[index]] = entry[index]
            temp_dict["logo"] = get_logo_path_of_company_with_identifier(temp_dict["company_identifier"])
            results.append(temp_dict)

    else:
        results = []

    cursor.close()
    dbconnection.close()

    return results


def get_all_public_campaigns_that_fit_with(topics: list, channels: list) -> list:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    sql_stmt = """
    SELECT DISTINCT company_offers_campaign.campaign_identifier, campaign_title, campaign_description,
                company_offers_campaign.company_identifier, topic_identifier, company_name, contact_email,
                contact_person, published_on
    FROM company_offers_campaign
        JOIN topics
            on topic_identifier = topic
        LEFT OUTER JOIN public_campaign_channels pcc
            on company_offers_campaign.campaign_identifier = pcc.campaign_identifier
        LEFT OUTER JOIN company c
            on company_offers_campaign.company_identifier = c.company_identifier
    WHERE confirmed = 1 """

    if topics is not None and len(topics) > 0:
        sql_stmt += """ and topic_identifier in """ + tuple_of_list(topics)  # TODO: WARNING: RISKY!

    if channels is not None and len(channels) > 0:
        sql_stmt += """ and channel_identifier in """ + tuple_of_list(channels)  # TODO: WARNING: RISKY!

    sql_stmt += " ORDER BY published_on DESC;"

    print(sql_stmt)

    cursor.execute(sql_stmt)

    keys = cursor.column_names
    entries = cursor.fetchall()

    results = []

    if len(entries) > 0:
        for entry in entries:
            temp_dict = {}
            for index in range(0, len(keys)):
                temp_dict[keys[index]] = entry[index]
            temp_dict["logo"] = get_logo_path_of_company_with_identifier(temp_dict["company_identifier"])
            results.append(temp_dict)

    else:
        results = []

    cursor.close()

    dbconnection.close()

    print(results)

    return results


def get_details_of_public_campaign_with_identifier(campaign_identifier: int) -> dict:
    sql_stmt = """
    SELECT DISTINCT company_offers_campaign.campaign_identifier, campaign_title, campaign_description,
                company_offers_campaign.company_identifier, topic_identifier, company_name, contact_email,
                contact_person, format, remuneration
    FROM company_offers_campaign
        JOIN topics
            on topic_identifier = topic
        LEFT OUTER JOIN public_campaign_channels pcc
            on company_offers_campaign.campaign_identifier = pcc.campaign_identifier
        LEFT OUTER JOIN company c
            on company_offers_campaign.company_identifier = c.company_identifier
    WHERE company_offers_campaign.campaign_identifier = %s;"""

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(sql_stmt, (campaign_identifier,))

    return_dict = {}

    keys = cursor.column_names
    entry = cursor.fetchone()

    cursor.close()

    if entry is not None:
        for index in range(0, len(keys)):
            return_dict[keys[index]] = entry[index]
        return_dict["logo"] = get_logo_path_of_company_with_identifier(return_dict["company_identifier"])
    else:
        raise CampaignDoesNotExist

    sql_stmt = """
        SELECT DISTINCT channel_internal_idenetifier, official_name
    FROM company_offers_campaign
        JOIN public_campaign_channels
            on company_offers_campaign.campaign_identifier = public_campaign_channels.campaign_identifier
        JOIN channels
            on channel_internal_idenetifier = channel_identifier
    WHERE company_offers_campaign.campaign_identifier = %s;"""

    cursor = dbconnection.cursor()

    cursor.execute(sql_stmt, (campaign_identifier,))

    print(cursor.statement)

    keys = cursor.column_names
    entries = cursor.fetchall()

    cursor.close()
    dbconnection.close()

    channels = []
    for entry in entries:
        temp_dict = {}
        for index in range(0, len(keys)):
            temp_dict[keys[index]] = entry[index]
        channels.append(temp_dict)

    return_dict["channel_data"] = channels
    return_dict["channel_identifiers"] = [entry[0] for entry in entries]
    return_dict["document"] = get_pdf_source(campaign_identifier)

    print(return_dict)

    return return_dict


def get_campaigns_of_company_with_identifier(company_identifier: int) -> list:
    dbconn = get_database_connection()
    cursor = dbconn.cursor()

    cursor.execute("""
        SELECT campaign_identifier, campaign_title 
        FROM company_offers_campaign
        WHERE company_identifier = %s""", (company_identifier,))

    entries = cursor.fetchall()
    keys = cursor.column_names

    return_list = []

    for entry in entries:
        tmp_dict = {}
        for index in range(0, len(keys)):
            tmp_dict[keys[index]] = entry[index]

        return_list.append(tmp_dict)

    cursor.close()

    return return_list


def get_pdf_source(campaign_identifier) -> str or None:
    """

    :param campaign_identifier:
    :return:
    """
    try:
        return os.path.exists(
            "/root/webapplication/static/campaigns/details_campaign_reference_no_{0}.pdf".format(campaign_identifier))
    except TypeError:
        return False


def update_campaign(campaign_identifier: int, company_identifier, dictioanry: ImmutableMultiDict, passed_files) -> bool:
    delete_public_campaign_with_identifier(campaign_identifier=campaign_identifier,
                                           company_identifier=company_identifier)
    add_public_campaign(company_identifier, dictioanry, passed_files)
