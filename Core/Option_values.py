import os
from builtins import enumerate

from mysql.connector.errors import *
from werkzeug.datastructures import ImmutableMultiDict
from Core.Exceptions.User import UserCoversNotTheRequestedChannel, UsernameAlreadyExists
from Core.Usermanagement import hash_password, verify_password
from Core.dbconn import get_database_connection

# Category: Profile
from Core.mailing import send_goodbye_message


def get_user_data(user_id: int) -> {str: any}:
    """
    This function helps to render a specific preferences-submenu

    :param user_id: int (user_id should be stored in the session with key=identifier)
    :return: all variable values that are required in the jinja2-template of the preferences menu
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    parameterized_query = """SELECT first_name, last_name, email, gender, birthyear, price, homebase, phone_number 
                                FROM influencer 
                                WHERE influencer_identifier=%s;"""

    cursor.execute(parameterized_query, (int(user_id),))

    keys = cursor.column_names
    values = cursor.fetchone()

    if values is None:
        raise UserCoversNotTheRequestedChannel

    print(values)

    return_dict = {}

    for index in range(0, len(keys)):
        try:
            return_dict[keys[index]] = values[index]
        except IndexError:
            raise IndexError("Internal error during assignment (for-loop dict-generation)")

    cursor.close()

    cursor = dbconnection.cursor()

    parameterized_query = """SELECT topic_identifier FROM influencer_covers_topic WHERE influencer_identifier=%s;"""
    cursor.execute(parameterized_query, (user_id,))

    return_dict["topicidentifiers"] = [topicIdentifier[0] for topicIdentifier in cursor.fetchall()]
    cursor.close()

    cursor = dbconnection.cursor()

    parameterized_query = """SELECT deal_identifier FROM influencer_deal WHERE influencer_identifier=%s;"""
    cursor.execute(parameterized_query, (user_id,))

    return_dict["dealidentifiers"] = [deal_identifier[0] for deal_identifier in cursor.fetchall()]

    cursor.close()
    dbconnection.close()

    return return_dict


def get_pwd_data(user_id: int) -> {str: any}:
    """
    This function helps to render a specific preferences-submenu

    :param user_id: int (user_id should be stored in the session with key=identifier)
    :return: all variable values that are required in the jinja2-template of the preferences menu
    """
    return {}


def get_profile_pictures_sources(user_id: int) -> {str: any}:
    """
    This function helps to render a specific preferences-submenu

    :param user_id: int (user_id should be stored in the session with key=identifier)
    :return: all variable values that are required in the jinja2-template of the preferences menu
    """
    try:
        files = os.listdir("{}/{}".format("/root/webapplication/static/pb", user_id))
    except FileNotFoundError:
        return {"images": ["/static/img/placeholder/unknown_male.jpg", None, None, None, None]}
    paths = {str(file).split("_")[-1].split(".")[0]: "/static/pb/{}/{}".format(user_id, file) for file in files}

    images = []

    for i in range(0, 5):
        try:
            images.append(paths.get(str(i), None))
        except FileNotFoundError:
            images.append(None)

    return {"images": images}


def get_support_data(user_id: int) -> {str: any}:
    """
    This function helps to render a specific preferences-submenu

    :param user_id: int (user_id should be stored in the session with key=identifier)
    :return: all variable values that are required in the jinja2-template of the preferences menu
    """
    return {}


def get_deactivate_data(user_id: int) -> {str: any}:
    """
    This function helps to render a specific preferences-submenu

    :param user_id: int (user_id should be stored in the session with key=identifier)
    :return: all variable values that are required in the jinja2-template of the preferences menu
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""SELECT * FROM influencer_had_previous_cooperation WHERE influencer_identifier = %s;""", (
        user_id,
    ))

    results = cursor.fetchall()
    keys = cursor.column_names

    cursor.close()
    dbconnection.close()

    return_list = []
    for dataset in results:
        temp_dict = {}
        for key_index in range(0, len(keys)):
            temp_dict[keys[key_index]] = dataset[key_index]
        return_list.append(temp_dict)

    return {"cooperations": return_list}


def get_delete_data(user_id: int) -> {str: any}:
    """
    This function helps to render a specific preferences-submenu

    :param user_id: int (user_id should be stored in the session with key=identifier)
    :return: all variable values that are required in the jinja2-template of the preferences menu
    """

    return {}


########################################################################################################################
# Company: Logo-Handling


def set_company_logo_data(company_identifier, passed_logo) -> bool:
    """

    :param company_identifier:
    :param passed_logo:
    :return:
    """


def get_company_logo_data(company_identifier: int) -> {str: str}:
    """

    :param company_identifier:
    :return:
    """
    try:
        files = os.listdir("/root/webapplication/static/company_logos")
    except FileNotFoundError:
        return {"path": None}

    for file in files:
        if file.split(".")[0].endswith("logo_company_{}".format(company_identifier)):
            return {"path": file}

    return {"path": None}


########################################################################################################################
# Category: Channels


def get_instagram_data(user_id: int) -> {str: any}:
    """
    This function helps to render a specific preferences-submenu

    :param user_id: int (user_id should be stored in the session with key=identifier)
    :return: all variable values that are required in the jinja2-template of the preferences menu
    """
    return union_dicts([get_channel_kpis_of(user_id, 'is_listed_on_instagram'),
                        get_content_types(user_id, 1),
                        get_active_countries(user_id, 1)
                        ])


def get_facebook_data(user_id: int) -> {str: any}:
    """
    This function helps to render a specific preferences-submenu

    :param user_id: int (user_id should be stored in the session with key=identifier)
    :return: all variable values that are required in the jinja2-template of the preferences menu
    """
    return union_dicts([get_channel_kpis_of(user_id, 'is_listed_on_facebook'),
                        get_content_types(user_id, 2),
                        get_active_countries(user_id, 2)])


def get_youtube_data(user_id: int) -> {str: any}:
    """
    This function helps to render a specific preferences-submenu

    :param user_id: int (user_id should be stored in the session with key=identifier)
    :return: all variable values that are required in the jinja2-template of the preferences menu
    """
    return union_dicts([get_channel_kpis_of(user_id, 'is_listed_on_youtube'),
                        get_active_countries(user_id, 3)])


def get_pinterest_data(user_id: int) -> {str: any}:
    """
    This function helps to render a specific preferences-submenu

    :param user_id: int (user_id should be stored in the session with key=identifier)
    :return: all variable values that are required in the jinja2-template of the preferences menu
    """
    return union_dicts([get_channel_kpis_of(user_id, 'is_listed_on_pinterest'),
                        get_content_types(user_id, 4)])


def get_blog_data(user_id: int) -> {str: any}:
    """
    This function helps to render a specific preferences-submenu

    :param user_id: int (user_id should be stored in the session with key=identifier)
    :return: all variable values that are required in the jinja2-template of the preferences menu
    """
    return union_dicts([get_channel_kpis_of(user_id, 'is_listed_on_personal_blog'),
                        get_content_types(user_id, 5)])


### COMPANIES:
def get_book_data(company_identifier: int) -> dict:
    """

    :param company_identifier:
    :return:
    """
    dbconnection = get_database_connection()

    cursor = dbconnection.cursor()

    cursor.execute("""SELECT booked_package, expire_date FROM company WHERE company_identifier = %s""",
                   (company_identifier,))

    package = cursor.fetchone()

    cursor.close()
    dbconnection.close()

    return {"package": package[0], "expires": package[1]}


def get_company_pwd_data(company_identifier: int) -> dict:
    return {}


def get_base_data(company_identifier: int) -> dict:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(
        """SELECT company_identifier, company_name, contact_person, contact_email, street_house_number, postcode, place, ust_id, pwd_hash, confirmed, booked_package, expire_date, created_on FROM company WHERE company_identifier = %s;""",
        (company_identifier,))

    keys = cursor.column_names
    entry = cursor.fetchone()

    return_dict = {}

    for index in range(0, len(keys)):
        return_dict[keys[index]] = entry[index]

    cursor.close()
    dbconnection.close()

    return return_dict


def set_book_data(company_identifier: int) -> dict:
    return {}


def set_company_pwd_data(company_identifier: int, dict: ImmutableMultiDict) -> dict:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""SELECT pwd_hash FROM company WHERE company_identifier = %s;""", (company_identifier,))

    if verify_password(dict.get("currentPWD"), cursor.fetchone()[0]):
        insert_new_pwd_hash_comp(company_identifier, dict.get("newPWD"))
    return {}


def set_base_data(company_identifier: int, dict: ImmutableMultiDict) -> dict:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    sql_stmt = """UPDATE company SET contact_email = %s, company_name = %s, contact_person = %s, street_house_number = %s,
                                      postcode = %s, place = %s, ust_id = %s WHERE company_identifier = %s;"""
    try:
        cursor.execute(sql_stmt, (dict.get("contactMail"), dict.get("companyName"), dict.get("contact"),
                                  dict.get("streetWithHouseNumber"), dict.get("postcode"), dict.get("place"),
                                  dict.get("ust_id"), company_identifier))

        dbconnection.commit()

        cursor.close()
        dbconnection.close()
    except:
        pass
    return {}


def get_channel_kpis_of(user_id: int, channel_relation_name) -> {str: any}:
    """
    This function returns all datasets of a specified channel (channel relation name is hard coded and must be a passed
    param)

    :param user_id: int (user_id should be stored in the session with key=identifier)
    :param channel_relation_name: str This is the nam of the relation (DB: Main [Hetzner])
    :return: all datasets that are associative with the user (that is stored with its identifier in in the session)
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    parameterized_query = """SELECT * FROM {channel_relation_name} WHERE influencer_identifier=%s;""".format(
        channel_relation_name=channel_relation_name)

    cursor.execute(parameterized_query, (int(user_id),))

    keys = cursor.column_names
    values = cursor.fetchone()

    if values is None:
        raise UserCoversNotTheRequestedChannel

    print(values)

    return_dict = {}

    for index in range(0, len(keys)):
        try:
            return_dict[keys[index]] = values[index]
        except IndexError:
            raise IndexError("Internal error during assignment (for-loop dict-generation)")

    cursor.close()
    dbconnection.close()

    return return_dict


def insert_instagram_data(user_id: int, username, follower_amount, post_amount, rhythm, age_distribution_min,
                          age_distribution_max, gender_distribution_male, gender_distribution_female,
                          engagement_rate_min, engagement_rate_max, follower_ratio_min, follower_ratio_max,
                          listing_on) -> bool:
    """

    :param user_id:
    :param username:
    :param follower_amount:
    :param post_amount:
    :param rhythm:
    :param age_distribution_min:
    :param age_distribution_max:
    :param gender_distribution_male:
    :param gender_distribution_female:
    :param engagement_rate_min:
    :param engagement_rate_max:
    :param follower_ratio_min:
    :param follower_ratio_max:
    :param listing_on
    :return:
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()
    cursor.execute("""SELECT * 
                        FROM is_listed_on_instagram 
                        WHERE influencer_identifier = %s""", (user_id,))

    if cursor.fetchall():
        # TODO: Update DONE, but not tested
        parameterized_query = """UPDATE is_listed_on_instagram 
                                    SET instagram_username = %s, 
                                        instagram_follower_amount = %s,
                                        instagram_post_amount = %s,
                                        instagram_rhythm = %s,
                                        instagram_gender_distribution_female = %s,
                                        instagram_gender_distribution_male = %s,
                                        instagram_age_distribution_min = %s,
                                        instagram_age_distribution_max = %s,
                                        instagram_engagement_rate_min = %s,
                                        instagram_engagement_rate_max = %s,
                                        instagram_follower_ratio_min = %s,
                                        instagram_follower_ratio_max = %s,
                                        listing_on = %s
                                    WHERE influencer_identifier = %s;"""

        update_cursor = dbconnection.cursor()

        update_cursor.execute(parameterized_query, (username,
                                                    follower_amount,
                                                    post_amount,
                                                    rhythm,
                                                    gender_distribution_female,
                                                    gender_distribution_male,
                                                    age_distribution_min,
                                                    age_distribution_max,
                                                    engagement_rate_min,
                                                    engagement_rate_max,
                                                    follower_ratio_min,
                                                    follower_ratio_max,
                                                    listing_on,
                                                    user_id,))

        update_cursor.close()

    else:
        # TODO: Insert DONE, but not tested
        parameterized_query = """INSERT INTO is_listed_on_instagram(influencer_identifier,
                                                                    instagram_username,
                                                                    instagram_follower_amount,
                                                                    instagram_post_amount,
                                                                    instagram_rhythm, 
                                                                    instagram_gender_distribution_male,
                                                                    instagram_gender_distribution_female,
                                                                    instagram_age_distribution_min,
                                                                    instagram_age_distribution_max, 
                                                                    instagram_engagement_rate_min, 
                                                                    instagram_engagement_rate_max, 
                                                                    instagram_follower_ratio_min, 
                                                                    instagram_follower_ratio_max,
                                                                    listing_on
                                                                    )
                                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        insert_cursor = dbconnection.cursor()

        insert_cursor.execute(parameterized_query, (
            user_id, username, follower_amount, post_amount, rhythm, gender_distribution_male,
            gender_distribution_female,
            age_distribution_min, age_distribution_max, engagement_rate_min, engagement_rate_max, follower_ratio_min,
            follower_ratio_max, int(1)  # IF the user is adding a channel, then make ik by default visible
        ))

        insert_cursor.close()

    cursor.close()
    try:
        dbconnection.commit()
        dbconnection.close()
        return True
    except:
        return False


def insert_facebook_data(user_id: int, username, follower_amount, post_amount, facebook_rhythm_types,
                         gender_distribution_female,
                         gender_distribution_male, page_activity, page_views,
                         likes, reach, post_interaction, listing_on: int) -> bool:
    """

    :param user_id:
    :param username:
    :param follower_amount:
    :param post_amount:
    :param facebook_rhythm_types:
    :param gender_distribution_female:
    :param gender_distribution_male:
    :param page_activity:
    :param page_views:
    :param likes:
    :param reach:
    :param post_interaction:
    :param listing_on:
    :return:
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()
    cursor.execute("""SELECT * 
                        FROM is_listed_on_facebook 
                        WHERE influencer_identifier = %s""", (user_id,))

    if cursor.fetchall():
        # TODO: Update DONE, but not tested
        parameterized_query = """UPDATE is_listed_on_facebook 
                                    SET facebook_username = %s, 
                                        facebook_follower_amount = %s,
                                        facebook_post_amount = %s,
                                        facebook_rhythm = %s,
                                        facebook_gender_distribution_female = %s,
                                        facebook_gender_distribution_male = %s,
                                        facebook_page_activity_amount = %s,
                                        facebook_page_views = %s,
                                        facebook_likes_amount = %s,
                                        facebook_reach_value = %s,
                                        facebook_post_interaction = %s,
                                        listing_on = %s
                                    WHERE influencer_identifier = %s;"""

        update_cursor = dbconnection.cursor()

        update_cursor.execute(parameterized_query, (username, follower_amount, post_amount, facebook_rhythm_types,
                                                    gender_distribution_female, gender_distribution_male, page_activity,
                                                    page_views, likes, reach, post_interaction, listing_on, user_id))

        update_cursor.close()

    else:
        # TODO: Insert DONE, but not tested
        print("INSERT")
        parameterized_query = """INSERT INTO is_listed_on_facebook(influencer_identifier, 
                                    facebook_username, facebook_follower_amount, facebook_post_amount, facebook_rhythm, 
                                    facebook_gender_distribution_male, facebook_gender_distribution_female, 
                                    facebook_page_activity_amount, facebook_page_views, facebook_likes_amount, 
                                    facebook_reach_value, facebook_post_interaction, listing_on)
                                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        insert_cursor = dbconnection.cursor()

        insert_cursor.execute(parameterized_query, (
            user_id, username, follower_amount, post_amount, facebook_rhythm_types,
            gender_distribution_male, gender_distribution_female, page_activity,
            page_views, likes, reach, post_interaction, int(1)
        ))

        insert_cursor.close()

    cursor.close()
    try:
        dbconnection.commit()
        dbconnection.close()
        return True
    except:
        return False


def insert_youtube_data(user_id: int, username, follower_amount: int, post_amount: int, rhythm: int,
                        age_distribution_min: int,
                        age_distribution_max: float, gender_distribution_male: int, gender_distribution_female: int,
                        page_views_amount: int, impressions_rate: int, click_rate: int, listing_on: int) -> bool:
    """

    :param user_id:
    :param username:
    :param follower_amount:
    :param post_amount:
    :param rhythm:
    :param age_distribution_min:
    :param age_distribution_max:
    :param gender_distribution_male:
    :param gender_distribution_female:
    :param page_views_amount:
    :param impressions_rate:
    :param click_rate:
    :param listing_on:
    :return:
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()
    cursor.execute("""SELECT * 
                            FROM is_listed_on_youtube 
                            WHERE influencer_identifier = %s""", (user_id,))

    if cursor.fetchall():
        # TODO: Update DONE, but not tested
        parameterized_query = """UPDATE is_listed_on_youtube 
                                    SET youtube_username = %s, youtube_follower_amount = %s,
                                        youtube_post_amount = %s, youtube_rhythm = %s,
                                        youtube_gender_distribution_female = %s, youtube_gender_distribution_male = %s,
                                        youtube_age_distribution_min = %s, youtube_age_distribution_max = %s,
                                        youtube_page_views = %s, youtube_impressions_amount = %s,
                                        youtube_click_rate = %s, listing_on = %s
                                    WHERE influencer_identifier = %s;"""

        update_cursor = dbconnection.cursor()

        update_cursor.execute(parameterized_query, (username,
                                                    follower_amount,
                                                    post_amount,
                                                    rhythm,
                                                    gender_distribution_female,
                                                    gender_distribution_male,
                                                    age_distribution_min,
                                                    age_distribution_max,
                                                    page_views_amount,
                                                    impressions_rate,
                                                    click_rate,
                                                    int(listing_on),
                                                    user_id,))

        update_cursor.close()

    else:
        # TODO: Insert DONE, but not tested
        parameterized_query = """INSERT INTO is_listed_on_youtube(influencer_identifier, youtube_username, 
        youtube_follower_amount, youtube_post_amount, youtube_rhythm, youtube_gender_distribution_male, 
        youtube_gender_distribution_female, youtube_age_distribution_min, youtube_age_distribution_max, 
        youtube_page_views, youtube_impressions_amount, youtube_click_rate, listing_on)
                                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        insert_cursor = dbconnection.cursor()

        insert_cursor.execute(parameterized_query, (
            user_id, username, follower_amount, post_amount, rhythm, gender_distribution_male,
            gender_distribution_female,
            age_distribution_min, age_distribution_max, page_views_amount, impressions_rate,
            click_rate, int(1)  # IF the user is adding a channel, then make ik by default visible
        ))

        insert_cursor.close()

    cursor.close()
    try:
        dbconnection.commit()
        dbconnection.close()
        return True
    except:
        return False


def insert_pinterest_data(user_id: int, username, follower_amount: int, post_amount: int, rhythm: int,
                          pinterest_viewer_amount: int, listing_on: int) -> bool:
    """

    :param user_id:
    :param username:
    :param follower_amount:
    :param post_amount:
    :param rhythm:
    :param pinterest_viewer_amount:
    :param listing_on:
    :return:
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()
    cursor.execute("""SELECT * 
                        FROM is_listed_on_pinterest 
                        WHERE influencer_identifier = %s""", (user_id,))

    if cursor.fetchall():
        # TODO: Update DONE, but not tested
        parameterized_query = """UPDATE is_listed_on_pinterest 
                                        SET pinterest_username = %s, pinterest_follower_amount = %s,
                                            pinterest_post_amount = %s, pinterest_rhythm = %s,
                                            pinterest_viewer_amount = %s, listing_on = %s
                                        WHERE influencer_identifier = %s;"""

        update_cursor = dbconnection.cursor()

        update_cursor.execute(parameterized_query, (username, follower_amount, post_amount, rhythm,
                                                    pinterest_viewer_amount, listing_on, user_id,))

        update_cursor.close()

    else:
        # TODO: Insert DONE, but not tested
        parameterized_query = """INSERT INTO is_listed_on_pinterest(influencer_identifier, pinterest_username, 
        pinterest_follower_amount, pinterest_post_amount, pinterest_rhythm, pinterest_viewer_amount, listing_on)
                                     VALUES (%s, %s, %s, %s, %s, %s, %s);"""

        insert_cursor = dbconnection.cursor()

        insert_cursor.execute(parameterized_query, (
            user_id, username, follower_amount, post_amount, rhythm, pinterest_viewer_amount, int(1),
        # If the user is adding a channel, then make ik by default visible
        ))

        insert_cursor.close()

    cursor.close()
    try:
        dbconnection.commit()
        dbconnection.close()
        return True
    except:
        return False


def insert_blog_data(user_id: int, url, follower_amount: int, post_amount: int, rhythm: int,
                     blog_viewer_amount: int, listing_on: int) -> bool:
    """

    :param user_id:
    :param url:
    :param follower_amount:
    :param post_amount:
    :param rhythm:
    :param blog_viewer_amount:
    :param listing_on:
    :return:
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()
    cursor.execute("""SELECT * 
                        FROM is_listed_on_personal_blog 
                        WHERE influencer_identifier = %s""", (user_id,))

    if cursor.fetchall():
        # TODO: Update DONE, but not tested
        parameterized_query = """UPDATE is_listed_on_personal_blog 
                                        SET blog_domain = %s, blog_follower_amount = %s,
                                            blog_post_amount = %s, blog_rhythm = %s,
                                            blog_page_views_amount = %s, listing_on = %s
                                        WHERE influencer_identifier = %s;"""

        update_cursor = dbconnection.cursor()

        update_cursor.execute(parameterized_query, (url, follower_amount, post_amount, rhythm,
                                                    blog_viewer_amount, int(listing_on), user_id,))

        update_cursor.close()

    else:
        # TODO: Insert DONE, but not tested
        parameterized_query = """INSERT INTO is_listed_on_personal_blog(influencer_identifier, blog_domain, 
        blog_follower_amount, blog_post_amount, blog_rhythm, blog_page_views_amount, listing_on) 
                                     VALUES (%s, %s, %s, %s, %s, %s, %s);"""

        insert_cursor = dbconnection.cursor()

        try:
            insert_cursor.execute(parameterized_query, (
                user_id, url, follower_amount, post_amount, rhythm, blog_viewer_amount, int(1)
            # If the user is adding a channel, then make ik by default visible
            ))
        except IntegrityError:
            raise UsernameAlreadyExists

        insert_cursor.close()

    cursor.close()
    try:
        dbconnection.commit()
        dbconnection.close()
        return True
    except:
        return False


def insert_active_countries(countries, user_id, channel_identifier=1):
    sql_paramaterized = """DELETE FROM countries_of_channel
                                WHERE influencer_identifier = %s and channel_identifier = %s;"""

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(sql_paramaterized, (user_id, channel_identifier,))

    dbconnection.commit()

    cursor.close()

    cursor = dbconnection.cursor()
    if len(countries) > 0:
        sql_paramaterized = """INSERT INTO countries_of_channel(channel_identifier, influencer_identifier, country_identifier) 
                                    VALUES """

        for content_type in countries:
            sql_paramaterized += """ (%s, %s, %s)"""
            if content_type is countries[-1]:
                sql_paramaterized += """;"""
            else:
                sql_paramaterized += """, """

        param_arr = []

        for content_type in countries:
            param_arr.append(channel_identifier)
            param_arr.append(user_id)
            param_arr.append(content_type)

        param_tuple = tuple(x for x in param_arr)

        print(param_tuple)
        print(sql_paramaterized)

        cursor.execute(sql_paramaterized, param_tuple)

        try:
            dbconnection.commit()
        except:
            return False

    cursor.close()
    dbconnection.close()


def insert_content_types(content_types, user_id, channel_identifier=1):
    sql_paramaterized = """DELETE FROM content_of_channel
                            WHERE influencer_identifier = %s and channel_identifier = %s"""

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(sql_paramaterized, (user_id, channel_identifier,))

    dbconnection.commit()

    cursor.close()

    cursor = dbconnection.cursor()
    if len(content_types) > 0:
        sql_paramaterized = """INSERT INTO content_of_channel(channel_identifier, influencer_identifier, content_type_identifier) 
                                VALUES """

        for content_type in content_types:
            sql_paramaterized += """ (%s, %s, %s)"""
            if content_type is content_types[-1]:
                sql_paramaterized += """;"""
            else:
                sql_paramaterized += """, """

        param_arr = []

        for content_type in content_types:
            param_arr.append(channel_identifier)
            param_arr.append(user_id)
            param_arr.append(content_type)

        param_tuple = tuple(x for x in param_arr)

        print(param_tuple)
        print(sql_paramaterized)

        cursor.execute(sql_paramaterized, param_tuple)

        try:
            dbconnection.commit()
        except:
            return False

    cursor.close()
    dbconnection.close()


def set_instagram_data(user_id: int, dict: ImmutableMultiDict) -> bool:
    """

    :param user_id:
    :param dict: Multidict that must contain all the Form-values
    :return:
    """

    try:
        print("GENDERS:>>> " + str(dict.get("gender_distribution_male")))
        insert_instagram_data(user_id, dict.get("username"), follower_amount=dict.get("follower"),
                              post_amount=dict.get("post_amount"),
                              rhythm=dict.get("instagram_rhythm_types"),
                              age_distribution_min=get_age_distribution_min(dict.get("age_distribution")),
                              age_distribution_max=get_age_distribution_max(dict.get("age_distribution")),
                              gender_distribution_male=100.00 - float(dict.get("gender_distribution_female")),
                              gender_distribution_female=dict.get("gender_distribution_female"),
                              engagement_rate_min=get_engagement_rate_min(dict.get("engagement_rate")),
                              engagement_rate_max=get_engagement_rate_max(dict.get("engagement_rate")),
                              follower_ratio_min=get_follower_ratio_min(dict.get("follower_ratio")),
                              follower_ratio_max=get_follower_ratio_max(dict.get("follower_ratio")),
                              listing_on=int(get_listing_state(dict.get("listing_on", "off"))),
                              )
        insert_content_types(content_types=dict.getlist("instagram_content"), user_id=user_id, channel_identifier=1)
        insert_active_countries(countries=dict.getlist("instagram_countries"), user_id=user_id, channel_identifier=1)
    except KeyError:
        raise KeyError("LOOK IN FORMS FOR MANIPULATED NAMES")

    except IntegrityError:
        raise UsernameAlreadyExists

    return True


def get_listing_state(listing_on: str) -> int:
    """

    :param listing_on:
    :return:
    """
    print(listing_on)
    if listing_on == "on":
        return 1
    return 0


def get_follower_ratio_min(selectpicker_id: str) -> int:
    """

    :param selectpicker_id:
    :return:
    """
    min_values = {
        "1": 0,
        "2": 1,
        "3": 2,
        "4": 3,
        "5": 4,
        "6": 5,
        "7": 6,
        "8": 7,
        "9": 8,
        "10": 9,
        "11": 10,
        "12": 15,
        "13": 20,
        "14": 30,
        "15": 40,
        "16": 50
    }
    return min_values.get(selectpicker_id, 0)


def get_follower_ratio_max(selectpicker_id: str) -> int:
    """

    :param selectpicker_id:
    :return:
    """
    max_values = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "11": 15,
        "12": 20,
        "13": 30,
        "14": 40,
        "15": 50,
        "16": 99
    }
    return max_values.get(selectpicker_id, 99)


def get_age_distribution_min(selectpicker_id: str) -> int:
    """

    :param selectpicker_id:
    :return:
    """
    min_values = {
        "0": 0,
        "1": 19,
        "2": 26,
        "3": 36,
        "4": 46,
        "5": 56
    }
    return min_values.get(selectpicker_id, 0)


def get_age_distribution_max(selectpicker_id: str) -> int:
    """

    :param selectpicker_id:
    :return:
    """
    min_values = {
        "0": 18,
        "1": 25,
        "2": 35,
        "3": 45,
        "4": 55,
        "5": 99
    }
    return min_values.get(selectpicker_id, 99)


def get_engagement_rates_min_max(selectpicker_id: str) -> (int, int):
    """
    Delegate method

    :param selectpicker_id:
    :return: tuple(int, int) -> (min, max)-values of the engagement-rate
    """
    return get_engagement_rate_min(selectpicker_id), get_engagement_rate_max(selectpicker_id)


def get_engagement_rate_min(selectpicker_id: str) -> int:
    """
    Min-Delegate-target of get_engagement_rates_min_max (dac-pattern)

    :param selectpicker_id:
    :return: int -> min-value of engagement-rate
    """
    min_values = {
        "1": 0,
        "2": 1,
        "3": 2,
        "4": 3,
        "5": 4,
        "6": 5,
        "7": 6,
        "8": 7,
        "9": 8,
        "10": 9,
        "11": 10,
        "12": 15,
        "13": 20,
        "14": 30,
        "15": 40,
        "16": 50
    }
    return min_values.get(selectpicker_id, 0)


def get_engagement_rate_max(selectpicker_id: str) -> int:
    """
    Max-Delegate-target of get_engagement_rates_min_max (dac-pattern)

    :param selectpicker_id:
    :return: int -> max-value of engagement-rate
    """
    max_values = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "11": 15,
        "12": 20,
        "13": 30,
        "14": 40,
        "15": 50,
        "16": 99
    }
    return max_values.get(selectpicker_id, 99)


def set_facebook_data(user_id: int, dict: ImmutableMultiDict) -> bool:
    """

    :param user_id:
    :param dict:
    :return:
    """
    try:
        insert_facebook_data(user_id, username=dict.get("username"), follower_amount=dict.get("follower"),
                             post_amount=dict.get("post_amount"),
                             facebook_rhythm_types=dict.get("facebook_rhythm_types"),
                             gender_distribution_female=dict.get("gender_distribution_female"),
                             gender_distribution_male=100.00 - float(dict.get("gender_distribution_female")),
                             page_activity=dict.get("page_activity"), page_views=dict.get("page_views"),
                             likes=dict.get("likes"),
                             reach=dict.get("reach"), post_interaction=dict.get("post_interaction"),
                             listing_on=get_listing_state(dict.get("listing_on"))
                             )
        insert_content_types(content_types=dict.getlist("facebook_content"), user_id=user_id, channel_identifier=2)
        insert_active_countries(countries=dict.getlist("facebook_countries"), user_id=user_id, channel_identifier=2)
    except KeyError:
        raise KeyError("LOOK IN FORMS FOR MANIPULATED NAMES")

    except IntegrityError:
        raise UsernameAlreadyExists

    return True


def set_youtube_data(user_id: int, dict: ImmutableMultiDict) -> bool:
    """

    :param user_id:
    :param dict:
    :return:
    """
    try:
        insert_youtube_data(user_id=user_id, username=dict.get("username"), follower_amount=dict.get("follower"),
                            post_amount=dict.get("post_amount"), rhythm=dict.get("youtube_rhythm_types"),
                            age_distribution_min=get_age_distribution_min(dict.get("age_distribution")),
                            age_distribution_max=get_age_distribution_max(dict.get("age_distribution")),
                            gender_distribution_male=100.00 - float(dict.get("gender_distribution_female")),
                            gender_distribution_female=dict.get("gender_distribution_female"),
                            page_views_amount=dict.get("page_views"), impressions_rate=dict.get("impressions"),
                            click_rate=dict.get("post_interaction"),
                            listing_on=get_listing_state(dict.get("state_listing")))
        insert_active_countries(countries=dict.getlist("youtube_countries"), user_id=user_id, channel_identifier=3)
    except KeyError:
        raise KeyError("LOOK IN FORMS FOR MANIPULATED NAMES")

    except IntegrityError:
        raise UsernameAlreadyExists

    return True


def set_pinterest_data(user_id: int, dict: ImmutableMultiDict) -> bool:
    """

    :param user_id:
    :param dict:
    :return:
    """
    try:
        insert_pinterest_data(user_id=user_id, username=dict.get("username"), follower_amount=dict.get("follower"),
                              post_amount=dict.get("post_amount"), rhythm=dict.get("pinterest_rhythm_types"),
                              pinterest_viewer_amount=dict.get("page_views"),
                              listing_on=get_listing_state(dict.get("listing_on")))
        insert_content_types(dict.getlist("pinterest_content"), user_id=user_id, channel_identifier=4)
    except KeyError:
        raise KeyError("LOOK IN FORMS FOR MANIPULATED NAMES")

    except IntegrityError:
        raise UsernameAlreadyExists

    return True


def set_personal_blog_data(user_id: int, dict: ImmutableMultiDict) -> bool:
    """

    :param user_id:
    :param dict:
    :return:
    """
    try:
        insert_blog_data(user_id=user_id, url=dict.get("username"), follower_amount=dict.get("follower"),
                         post_amount=dict.get("post_amount"), rhythm=dict.get("blog_rhythm_types"),
                         blog_viewer_amount=dict.get("blog_page_views"),
                         listing_on=get_listing_state(dict.get("listing_on")))

        insert_content_types(user_id=user_id, content_types=dict.getlist("blog_content"), channel_identifier=5)
    except KeyError:
        raise KeyError("LOOK IN FORMS FOR MANIPULATED NAMES")

    except IntegrityError:
        raise UsernameAlreadyExists


def set_user_data(user_id: int, dict: ImmutableMultiDict):
    try:
        if insert_covered_topics(user_id=user_id, topics=dict.getlist("topics")) and \
                insert_deal_types(user_id=user_id, deal_types=dict.getlist("deal")) and \
                insert_user_data(user_id, dict.get("firstName"), dict.get("lastName"), dict.get("mailAddress"),
                                 dict.get("phoneNumber"), get_gender(dict.get("gender")),
                                 birthyear=dict.get("birthyear"),
                                 homebase=dict.get("homebase"), price=dict.get("price")):
            return True
        else:
            return False
    except KeyError:
        raise KeyError("FORM-names were manipulated! TODO: check")


def get_gender(gender: str) -> str:
    """

    :param gender:
    :return:
    """
    gen = 'male'
    if gender == "0":
        gen = 'male'
    elif gender == "1":
        gen = 'female'
    elif gender == "2":
        gen = "d"
    else:
        raise IndexError("Unknown gender-index: " + gender)

    return gen


def set_pwd_data(user_id: int, dict: ImmutableMultiDict):
    """

    :param user_id:
    :param dict:
    :return:
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""SELECT pwd_hash FROM influencer WHERE influencer_identifier = %s;""", (user_id,))

    if verify_password(dict.get("currentPWD"), cursor.fetchone()[0]):
        insert_new_pwd_hash(user_id, dict.get("newPWD"))

    cursor.close()
    dbconnection.close()


def set_delete_data(user_id: int, dict: ImmutableMultiDict):
    """

    :param user_id:
    :param dict:
    :return:
    """
    if dict["deletePersistent"] == "on":

        dbconnection = get_database_connection()
        cursor = dbconnection.cursor()

        cursor.execute("""SELECT email, first_name, language_abbr FROM influencer WHERE influencer_identifier = %s""",
                       (user_id,))

        result = cursor.fetchone()
        cursor.close()

        send_goodbye_message(result[0], result[1], result[2])

        insert_profile_deleion_reason(dict["deletionReason"], "Influencer")

        cursor = dbconnection.cursor()

        cursor.execute("""DELETE FROM influencer WHERE influencer_identifier = %s;""", (user_id,))

        dbconnection.commit()

        cursor.close()

        # print("REASON: ")

        return True

    else:
        return False


def set_deactivate_data(user_id: int, dict: ImmutableMultiDict):
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""
    INSERT INTO influencer_had_previous_cooperation(influencer_identifier, title_of_cooperation, date_of_cooperation, description)
    VALUES(%s, %s, %s, %s)""", (
        user_id, dict.get("title"), dict.get("date"), dict.get("description")
    ))

    dbconnection.commit()
    cursor.close()
    dbconnection.close()

    return True


def get_content_types(user_id: int, channel_identifier: int) -> dict:
    """

    :param user_id:
    :param channel_identifier:
    :return:
    """
    sql_parameterized = """SELECT content_type_identifier FROM content_of_channel 
                            WHERE influencer_identifier = %s and channel_identifier = %s"""

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(sql_parameterized, (user_id, channel_identifier,))

    result = cursor.fetchall()

    content_types = []

    for item in result:
        content_types.append(item[0])

    cursor.close()

    return {"content_types": content_types}


def get_active_countries(user_id: int, channel_identifier: int) -> dict:
    """

    :param user_id:
    :param channel_identifier:
    :return:
    """
    sql_parameterized = """SELECT country_identifier FROM countries_of_channel 
                            WHERE influencer_identifier = %s and channel_identifier = %s"""

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(sql_parameterized, (user_id, channel_identifier,))

    result = cursor.fetchall()

    countries = []

    for item in result:
        countries.append(item[0])

    cursor.close()
    dbconnection.close()

    return {"active_countries": countries}


def union_dicts(dicts: list) -> dict:
    """

    :param dicts:
    :return:
    """
    merged = {}

    for dic in dicts:
        try:
            for key in dic.keys():
                merged[key] = dic[key]
        except Exception:
            raise TypeError("Dicts are as input required.")

    return merged


def insert_deal_types(user_id: int, deal_types: list) -> bool:
    """

    :param user_id:
    :param deal_types:
    :return:
    """
    dbconnection = get_database_connection()
    sql_paramaterized = """DELETE FROM influencer_deal
                            WHERE influencer_identifier = %s"""

    cursor = dbconnection.cursor()

    cursor.execute(sql_paramaterized, (user_id,))

    dbconnection.commit()

    cursor.close()

    cursor = dbconnection.cursor()
    if len(deal_types) > 0:
        sql_paramaterized = """INSERT INTO influencer_deal(influencer_identifier, deal_identifier) 
                                VALUES """

        for deal_type in deal_types:
            sql_paramaterized += """ (%s, %s)"""
            if deal_type is deal_types[-1]:
                sql_paramaterized += """;"""
            else:
                sql_paramaterized += """, """

        param_arr = []

        for deal_type in deal_types:
            param_arr.append(user_id)
            param_arr.append(deal_type)

        param_tuple = tuple(x for x in param_arr)

        print(param_tuple)
        print(sql_paramaterized)

        cursor.execute(sql_paramaterized, param_tuple)

        try:
            dbconnection.commit()
        except:
            return False

    cursor.close()
    dbconnection.close()

    return True


def insert_covered_topics(user_id: int, topics: list) -> bool:
    """

    :param user_id:
    :param topics:
    :return:
    """
    sql_paramaterized = """DELETE FROM influencer_covers_topic
                                WHERE influencer_identifier = %s"""

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(sql_paramaterized, (user_id,))

    dbconnection.commit()

    cursor.close()

    cursor = dbconnection.cursor()
    if len(topics) > 0:
        sql_paramaterized = """INSERT INTO influencer_covers_topic(influencer_identifier, topic_identifier) 
                                    VALUES """

        for topic in topics:
            sql_paramaterized += """ (%s, %s)"""
            if topic is topics[-1]:
                sql_paramaterized += """;"""
            else:
                sql_paramaterized += """, """

        param_arr = []

        for topic in topics:
            param_arr.append(user_id)
            param_arr.append(topic)

        param_tuple = tuple(x for x in param_arr)

        print(param_tuple)
        print(sql_paramaterized)

        cursor.execute(sql_paramaterized, param_tuple)

        try:
            dbconnection.commit()
        except:
            cursor.close()
            dbconnection.close()
            return False

    cursor.close()
    dbconnection.close()
    return True


def insert_new_pwd_hash(user_id: int, pwd: str):
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""UPDATE influencer SET pwd_hash = %s WHERE influencer_identifier = %s""",
                   (hash_password(pwd), user_id))

    dbconnection.commit()

    cursor.close()
    dbconnection.close()


def insert_new_pwd_hash_comp(company_identifier: int, pwd: str):
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""UPDATE company SET pwd_hash = %s WHERE company_identifier = %s""",
                   (hash_password(pwd), company_identifier))

    dbconnection.commit()

    cursor.close()
    dbconnection.close()


def insert_rhytm_data(user_id: int, rythm: list) -> bool:
    pass


def insert_user_data(user_id: int, first_name: str, lastName: str, mailAddress: str, phoneNumber: str, gender: str,
                     birthyear: int, homebase: str,
                     price: float) -> bool:
    """

    :param user_id:
    :param first_name:
    :param lastName:
    :param mailAddress:
    :param phoneNumber:
    :param gender:
    :param birthyear:
    :param homebase:
    :param price:
    :param topics:
    :return:
    """
    try:
        dbconnection = get_database_connection()
        cursor = dbconnection.cursor()

        sql_paramterized = """UPDATE influencer 
                                SET 
                                    last_name = %s, first_name = %s, email = %s, phone_number = %s, gender = %s,
                                    birthyear = %s, homebase = %s, price = %s
                                WHERE influencer_identifier = %s"""

        cursor.execute(sql_paramterized,
                       (lastName, first_name, mailAddress, phoneNumber, gender, birthyear, homebase, price, user_id))

        dbconnection.commit()

        cursor.close()
        dbconnection.close()

    except:
        return False

    return True


def get_logo_path_of_company_with_identifier(comapny_identifier: int) -> str:
    result = get_company_logo_data(company_identifier=comapny_identifier)["path"]
    print(result)
    return result


def set_delete_data_company(company_identifier: int, dict: ImmutableMultiDict) -> bool:
    """

    :param user_id:
    :param dict:
    :return: bool
    """
    if dict["deletePersistent"] == "on":

        dbconnection = get_database_connection()
        cursor = dbconnection.cursor()

        cursor.execute(
            """SELECT contact_email, contact_person, language_abbr FROM company WHERE company_identifier = %s""",
            (company_identifier,))

        result = cursor.fetchone()
        cursor.close()

        send_goodbye_message(result[0], result[1], result[2])

        insert_profile_deleion_reason(dict["deletionReason"], "Company")

        cursor = dbconnection.cursor()

        cursor.execute("""DELETE FROM company WHERE company_identifier = %s;""", (company_identifier,))

        dbconnection.commit()

        cursor.close()

        print("REASON: ")

        return True

    else:
        return False


def get_delete_data_company(company_identifier: int):
    return {}


def insert_profile_deleion_reason(reason_identifier: int, type_str: str) -> None:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    try:
        cursor.execute("""
        INSERT INTO profile_deletion(reason, type) VALUES (%s, %s);""", (
            reason_identifier, type_str
        ))
    except:
        print("ERROR DURING THE INSERT OF THE DELETION REASON")

    dbconnection.commit()
    cursor.close()
    dbconnection.close()


def delete_cooperation(cooperation_identifier: int, user_identifier: int):
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""DELETE FROM influencer_had_previous_cooperation WHERE influencer_identifier = %s and ID = %s""", (
        user_identifier, cooperation_identifier
    ))

    dbconnection.commit()
    cursor.close()
    dbconnection.close()
