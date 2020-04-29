from Core.Option_values import get_profile_pictures_sources
from Core.dbconn import get_database_connection


def get_campaigns_basic_view(user_id: int) -> list:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""
    SELECT campaign.campaign_identifier, company_identifier, name, description, Count_Result
    FROM campaign
            LEFT OUTER JOIN
        (SELECT campaign_identifier, COUNT(*) as Count_Result FROM is_pinned_on_campaign GROUP BY (campaign_identifier)) as aggr_func_count_result
            on aggr_func_count_result.campaign_identifier = campaign.campaign_identifier
    WHERE company_identifier = %s;""", (user_id,))

    result = parse_result(cursor.column_names, cursor.fetchall())

    cursor.close()
    dbconnection.close()

    return result


def parse_result(keys: list, values: list) -> list:
    return_list = []

    for i in range(0, len(values)):
        temp_dict = {}
        for k in range(0, len(keys)):
            temp_dict[keys[k]] = values[i][k]

        return_list.append(temp_dict)

    print(return_list)
    return return_list


def get_campaigns(user_id: int) -> list:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""
        SELECT campaign.campaign_identifier, company_identifier, name, description
        FROM campaign
        WHERE company_identifier = %s;""", (user_id,))

    cursor.close()
    dbconnection.close()

    return parse_result(cursor.column_names, cursor.fetchall())


def get_data_of_specific_campaign(campaign_id: int) -> dict:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    sql_parameterized_query = """
    SELECT campaign.campaign_identifier, company_identifier, name, description, is_pinned_on_campaign.influencer_identifier, remark, last_name, first_name, email, phone_number, price, gender, homebase, birthyear, pwd_hash, joined_at, listing_on, Count_Result, position, path
    FROM campaign
        LEFT OUTER JOIN
        is_pinned_on_campaign
            on campaign.campaign_identifier = is_pinned_on_campaign.campaign_identifier
        LEFT OUTER JOIN influencer
            on influencer.influencer_identifier = is_pinned_on_campaign.influencer_identifier
        LEFT OUTER JOIN (SELECT campaign_identifier, COUNT(*) as Count_Result FROM is_pinned_on_campaign GROUP BY (campaign_identifier)) as aggr_func_count_result
            on aggr_func_count_result.campaign_identifier = campaign.campaign_identifier
        LEFT OUTER JOIN influencer_picture_path
            on influencer.influencer_identifier = influencer_picture_path.influencer_identifier and position = '1'
        WHERE campaign.campaign_identifier = %s;"""

    cursor.execute(sql_parameterized_query, (campaign_id,))

    return_dict = {}

    print(cursor.statement)

    keys = cursor.column_names

    result = cursor.fetchall()

    print(result)

    print(cursor.statement)

    for index in range(0, 4):
        return_dict[keys[index]] = result[0][index]

    entry_count = 0
    outer_list = []
    temp_list = []
    for entry in result:
        if entry_count == 4:
            entry_count = 0
            outer_list.append(temp_list)
            temp_list = []

        temp_dict = {}

        for index in range(4, len(keys)):
            temp_dict[keys[index]] = entry[index]
            print(entry[index])

        temp_dict["profile_image"] = get_profile_pictures_sources(entry[4])["images"][0]
        temp_list.append(temp_dict)
        entry_count += 1
    outer_list.append(temp_list)

    return_dict["influencer"] = outer_list

    print(return_dict)

    cursor.close()
    dbconnection.close()

    return return_dict


def add_campaign(name: str, description: str, owner: int) -> bool:
    sql = """INSERT INTO campaign(company_identifier, name, description) VALUES (%s, %s, %s);"""

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(sql, (owner, name, description))

    dbconnection.commit()

    cursor.close()
    dbconnection.close()

    return True


def edit_campaign(internal_identifier: int, name: str, description: str, owner: int) -> bool:
    sql = """UPDATE campaign SET description = %s, name = %s WHERE campaign_identifier= %s;"""

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(sql, (description, name, internal_identifier))

    dbconnection.commit()

    cursor.close()
    dbconnection.close()
    return True
