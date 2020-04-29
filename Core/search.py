import mysql
from werkzeug.datastructures import ImmutableMultiDict
from Core.Exceptions.Search import InvalidGETRequest
from Core.admin.tracking.searches import track_search
from Core.dbconn import get_database_connection


def search_influencer_related(dictionary: ImmutableMultiDict, booked_package) -> list:
    track_search('global', booked_package)
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    sql_stmt = """
                SELECT DISTINCT influencer.influencer_identifier, email, birthyear, gender, homebase, first_name, last_name
                FROM influencer 
                        LEFT OUTER JOIN influencer_covers_topic on influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
                        LEFT OUTER JOIN influencer_channel_language on influencer.influencer_identifier = influencer_channel_language.influencer_identifier
                        LEFT OUTER JOIN influencer_deal on influencer_deal.influencer_identifier = influencer.influencer_identifier 
                WHERE birthyear >= %s 
                    and birthyear <= %s """

    params = [dictionary.get("birthyear_from"), dictionary.get("birthyear_to")]

    if dictionary.getlist("genders") is not None and len(dictionary.getlist("genders")) > 0:
        sql_stmt += """ and gender in """ + tuple_of_list(dictionary.getlist("genders"))

    if dictionary.get("homebase") is not "":
        sql_stmt += """ and homebase = %s"""
        params.append(dictionary.get("homebase"))

    if dictionary.getlist("deals") is not None and len(dictionary.getlist("deals")) > 0:
        sql_stmt += """ and deal_identifier in """ + tuple_of_list(dictionary.getlist("deals"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("topics") is not None and len(dictionary.getlist("topics")) > 0:
        sql_stmt += """ and topic_identifier in """ + tuple_of_list(
            dictionary.getlist("topics"))  # TODO: WARNING: RISKY!

    # if dictionary.get("usedLanguages") is not None:
    #     sql_stmt += """ and language_identifer in """ + str(tuple_of_list(dictionary.getlist("usedLanguages")))

    sql_stmt += """ LIMIT 20 """

    if dictionary.get("offset"):
        sql_stmt += """ OFFSET """ + dictionary.get("offset")

    sql_stmt += ";"

    prm_tuple = tuple(x for x in params)

    try:
        cursor.execute(sql_stmt, prm_tuple)
    except mysql.connector.errors.ProgrammingError:
        print(sql_stmt)

    print(cursor.statement)

    result = cursor.fetchall()
    column_names = cursor.column_names

    cursor.close()
    dbconnection.close()

    return parse_list_tuples_to_list_dict(result, column_names)


def search_instagrammer(dictionary: ImmutableMultiDict, booked_package) -> list:
    track_search('instagram', booked_package)
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    sql_stmt = """
    SELECT DISTINCT *  FROM (
    SELECT DISTINCT searchable_instagram_profiles.influencer_identifier, instagram_username, instagram_follower_amount, instagram_post_amount, instagram_rhythm, instagram_gender_distribution_male, instagram_gender_distribution_female, instagram_age_distribution_min, instagram_age_distribution_max, instagram_engagement_rate_min, instagram_engagement_rate_max, instagram_follower_ratio_min, instagram_follower_ratio_max

    FROM searchable_instagram_profiles
        LEFT OUTER JOIN content_of_channel
            on channel_identifier = 1
                   and content_of_channel.influencer_identifier = searchable_instagram_profiles.influencer_identifier
        LEFT OUTER JOIN countries_of_channel
            on content_of_channel.channel_identifier = 1
                   and countries_of_channel.influencer_identifier = searchable_instagram_profiles.influencer_identifier
     """

    params = []

    where_clause = []

    if dictionary.get("instagramFollowerFrom") != 'UNDEFINED' and dictionary.get("instagramFollowerFrom") is not None:
        where_clause.append("""instagram_follower_amount >= %s """)
        params.append(dictionary.get("instagramFollowerFrom"))

    if dictionary.get("instagramFollowerTo") != 'UNDEFINED' and dictionary.get("instagramFollowerTo") is not None:
        where_clause.append("""  instagram_follower_amount <= %s """)
        params.append(dictionary.get("instagramFollowerTo"))

    if dictionary.get("instagram_age_distribution_from") != 'UNDEFINED' and dictionary.get(
            "instagram_age_distribution_from") is not None:
        where_clause.append("""  instagram_age_distribution_min >= %s """)
        params.append(dictionary.get("instagram_age_distribution_from"))

    if dictionary.get("instagram_age_distribution_to") != 'UNDEFINED' and dictionary.get(
            "instagram_age_distribution_to") is not None:
        where_clause.append("""  instagram_age_distribution_max <= %s """)
        params.append(dictionary.get("instagram_age_distribution_to"))

    if dictionary.get("instagram_gender_distribution_female_from") != 'UNDEFINED' and dictionary.get(
            "instagram_gender_distribution_female_from") is not None:
        where_clause.append("""  instagram_gender_distribution_male >= %s """)
        params.append(dictionary.get("instagram_gender_distribution_female_from"))

    if dictionary.get("instagram_gender_distribution_female_to") != 'UNDEFINED' and dictionary.get(
            "instagram_gender_distribution_female_to") is not None:
        where_clause.append("""  instagram_gender_distribution_female <= %s """)
        params.append(dictionary.get("instagram_gender_distribution_female_to"))

    if dictionary.get("instagram_gender_distribution_male_from") != 'UNDEFINED' and dictionary.get(
            "instagram_gender_distribution_male_from") is not None:
        where_clause.append("""  instagram_gender_distribution_male >= %s """)
        params.append(dictionary.get("instagram_gender_distribution_male_from"))

    if dictionary.get("instagram_gender_distribution_male_to") != 'UNDEFINED' and dictionary.get(
            "instagram_gender_distribution_male_to") is not None:
        where_clause.append("""  instagram_gender_distribution_male <= %s """)
        params.append(dictionary.get("instagram_gender_distribution_male_to"))

    if dictionary.get("engagementRateFrom") != 'UNDEFINED' and dictionary.get("engagementRateFrom") is not None:
        where_clause.append("""  instagram_engagement_rate_min >= %s """)
        params.append(dictionary.get("engagementRateFrom"))

    if dictionary.get("engagementRateTo") != 'UNDEFINED' and dictionary.get("engagementRateTo") is not None:
        where_clause.append("""  instagram_engagement_rate_max <= %s """)
        params.append(dictionary.get("engagementRateTo"))

    if dictionary.get("instagramfollowerRatioFrom") != 'UNDEFINED' and dictionary.get(
            "instagramfollowerRatioFrom") is not None:
        where_clause.append("""  instagram_follower_ratio_min >= %s """)
        params.append(dictionary.get("instagramfollowerRatioFrom"))

    if dictionary.get("instagramfollowerRatioTo") != 'UNDEFINED' and dictionary.get(
            "instagramfollowerRatioTo") is not None:
        where_clause.append("""  instagram_follower_ratio_max <= %s """)
        params.append(dictionary.get("instagramfollowerRatioTo"))

    if dictionary.get("instagram_post_amount_from") != 'UNDEFINED' and dictionary.get(
            "instagram_post_amount_from") is not None:
        where_clause.append("""  instagram_post_amount >= %s """)
        params.append(dictionary.get("instagram_post_amount_from"))

    if dictionary.get("instagram_post_amount_to") != 'UNDEFINED' and dictionary.get(
            "instagram_post_amount_to") is not None:
        where_clause.append("""  instagram_post_amount <= %s """)
        params.append(dictionary.get("instagram_post_amount_to"))

    # TODO: Implement content-types

    if len(where_clause) > 0:
        sql_stmt += "WHERE "
        for item in where_clause:
            if item is not where_clause[-1]:
                sql_stmt += item + " and "
            else:
                sql_stmt += item
    tempory = 0
    if len(where_clause) > 0:
        if dictionary.getlist("instagram_content") is not None and len(dictionary.getlist("instagram_content")) > 0:
            sql_stmt += """ and content_type_identifier in """ + tuple_of_list(dictionary.getlist("instagram_content"))
            tempory += 1
    else:
        if dictionary.getlist("instagram_content") is not None and len(dictionary.getlist("instagram_content")) > 0:
            sql_stmt += """ WHERE content_type_identifier in """ + tuple_of_list(
                dictionary.getlist("instagram_content"))
            tempory += 1

    if dictionary.getlist("instagram_rhythm_types") is not None and len(
            dictionary.getlist("instagram_rhythm_types")) > 0:
        tuple_of_list(dictionary.getlist("instagram_rhythm_types"))
        if len(where_clause) > 0 or tempory == 1:
            sql_stmt += """ and instagram_rhythm in """ + tuple_of_list(dictionary.getlist("instagram_rhythm_types"))
        else:
            sql_stmt += """ WHERE instagram_rhythm in """ + tuple_of_list(
                dictionary.getlist("instagram_rhythm_types"))

    sql_stmt += """ ) as c1
    
    INNER JOIN 

    (
        SELECT DISTINCT influencer.influencer_identifier, birthyear, email, gender, homebase, first_name, last_name

    FROM influencer LEFT OUTER JOIN influencer_covers_topic
                        on influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
                    LEFT OUTER JOIN influencer_channel_language
                        on influencer.influencer_identifier = influencer_channel_language.influencer_identifier
                    LEFT OUTER JOIN influencer_deal
                        on influencer_deal.influencer_identifier = influencer.influencer_identifier

    WHERE 
        birthyear >= %s
        and birthyear <= %s """

    params.append(dictionary.get("birthyear_from"))
    params.append(dictionary.get("birthyear_to"))

    if dictionary.getlist("genders") is not None and len(dictionary.getlist("genders")) > 0:
        sql_stmt += """ and gender in """ + tuple_of_list(dictionary.getlist("genders"))

    if dictionary.get("homebase") is not "":
        sql_stmt += """ and homebase = %s"""
        params.append(dictionary.get("homebase"))

    if dictionary.getlist("deals") is not None and len(dictionary.getlist("deals")) > 0:
        sql_stmt += """ and deal_identifier in """ + tuple_of_list(dictionary.getlist("deals"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("topics") is not None and len(dictionary.getlist("topics")) > 0:
        sql_stmt += """ and topic_identifier in """ + tuple_of_list(
            dictionary.getlist("topics"))  # TODO: WARNING: RISKY!

    # if dictionary.get("usedLanguages") is not None:
    #     sql_stmt += """ and language_identifer in """+str(tuple_of_list(dictionary.getlist("usedLanguages")))

    sql_stmt += """) as c2 on c1.influencer_identifier = c2.influencer_identifier LIMIT 20"""

    if dictionary.get("offset"):
        if int(dictionary.get("offset")) >= 0 and int(dictionary.get("offset")) % 20 == 0:
            sql_stmt += """ OFFSET """ + dictionary.get("offset")

    sql_stmt += ";"

    prm_tuple = tuple(x for x in params)

    try:
        cursor.execute(sql_stmt, prm_tuple)
    except mysql.connector.errors.ProgrammingError:
        print(sql_stmt)

    print(cursor.statement)

    result = cursor.fetchall()
    column_names = cursor.column_names

    cursor.close()
    dbconnection.close()

    return parse_list_tuples_to_list_dict(result, column_names)


def search_facebook_user(dictionary: ImmutableMultiDict, booked_package) -> list:
    track_search('facebook', booked_package)
    sql_stmt = """
    SELECT DISTINCT influencer.influencer_identifier, last_name, first_name, email, price, gender, homebase, birthyear,
                facebook_username, facebook_follower_amount, facebook_page_views, facebook_post_amount, facebook_rhythm,
                facebook_gender_distribution_male, facebook_gender_distribution_female, facebook_page_activity_amount,
                facebook_likes_amount, facebook_reach_value, facebook_post_interaction
    FROM influencer
        JOIN is_listed_on_facebook
            on is_listed_on_facebook.influencer_identifier = influencer.influencer_identifier
        LEFT OUTER JOIN content_of_channel
            on content_of_channel.influencer_identifier = influencer.influencer_identifier
                   and channel_identifier = 2
        LEFT OUTER JOIN influencer_covers_topic
            on influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
        LEFT OUTER JOIN influencer_deal
            on influencer.influencer_identifier = influencer_deal.influencer_identifier
        LEFT OUTER JOIN countries_of_channel
            on influencer.influencer_identifier = countries_of_channel.influencer_identifier
                   and countries_of_channel.channel_identifier = 2
        WHERE influencer.listing_on = 1 """

    parameters = []
    if dictionary.get("facebookFollowerFrom") != "UNDEFINED" and dictionary.get("facebookFollowerFrom") is not None:
        sql_stmt += """ and facebook_follower_amount >= %s """
        parameters.append(dictionary.get("facebookFollowerFrom", 0))

    if dictionary.get("facebookFollowerTo") != "UNDEFINED" and dictionary.get("facebookFollowerTo") is not None:
        sql_stmt += """ and facebook_follower_amount <= %s """
        parameters.append(dictionary.get("facebookFollowerTo", 0))

    if dictionary.get("birthyear_from") != "UNDEFINED" and dictionary.get("birthyear_from") is not None:
        sql_stmt += """ and birthyear >= %s """
        parameters.append(dictionary.get("birthyear_from", 0))

    if dictionary.get("birthyear_to") != "UNDEFINED" and dictionary.get("birthyear_to") is not None:
        sql_stmt += """ and birthyear <= %s """
        parameters.append(dictionary.get("birthyear_to", 0))

    # if dictionary.get("facebook_reach_from") != "UNDEFINED" and dictionary.get("facebook_reach_from") is not None:
    #     sql_stmt += """ and facebook_reach_value >= %s """
    #     parameters.append(dictionary.get("facebook_reach_from", 0))
    #
    # if dictionary.get("facebook_reach_to") != "UNDEFINED" and dictionary.get("facebook_reach_to") is not None:
    #     sql_stmt += """ and facebook_reach_value <= %s """
    #     parameters.append(dictionary.get("facebook_reach_to", 0))

    if dictionary.get("facebook_post_interaction_From") != "UNDEFINED" and dictionary.get(
            "facebook_post_interaction_From") is not None:
        sql_stmt += """ and facebook_post_interaction >= %s """
        parameters.append(dictionary.get("facebook_post_interaction_From", 0))

    if dictionary.get("facebook_post_interaction_To") != "UNDEFINED" and dictionary.get(
            "facebook_post_interaction_To") is not None:
        sql_stmt += """ and facebook_post_interaction <= %s """
        parameters.append(dictionary.get("facebook_post_interaction_To", 0))

    if dictionary.get("facebook_post_amount_from") != "UNDEFINED" and dictionary.get(
            "facebook_post_amount_from") is not None:
        sql_stmt += """ and facebook_post_amount >= %s """
        parameters.append(dictionary.get("facebook_post_amount_from", 0))

    if dictionary.get("facebook_post_amount_to") != "UNDEFINED" and dictionary.get(
            "facebook_post_amount_to") is not None:
        sql_stmt += """ and facebook_post_amount <= %s """
        parameters.append(dictionary.get("facebook_post_amount_to", 0))

    if dictionary.get("facebook_page_calls_From") != "UNDEFINED" and dictionary.get(
            "facebook_page_calls_From") is not None:
        sql_stmt += """ and facebook_page_views >= %s """
        parameters.append(dictionary.get("facebook_page_calls_From", 0))

    if dictionary.get("facebook_page_calls_To") != "UNDEFINED" and dictionary.get("facebook_page_calls_To") is not None:
        sql_stmt += """ and facebook_page_views <= %s """
        parameters.append(dictionary.get("facebook_page_calls_To", 0))

    if dictionary.get("facebook_page_activity_From") != "UNDEFINED" and dictionary.get(
            "facebook_page_activity_From") is not None:
        sql_stmt += """ and facebook_page_activity_amount >= %s """
        parameters.append(dictionary.get("facebook_page_activity_From", 0))

    if dictionary.get("facebook_page_activity_To") != "UNDEFINED" and dictionary.get(
            "facebook_page_activity_To") is not None:
        sql_stmt += """ and facebook_page_activity_amount <= %s """
        parameters.append(dictionary.get("facebook_page_activity_To", 0))

    if dictionary.get("facebook_likes_From") != "UNDEFINED" and dictionary.get("facebook_likes_From") is not None:
        sql_stmt += """ and facebook_likes_amount >= %s """
        parameters.append(dictionary.get("facebook_likes_From", 0))

    if dictionary.get("facebook_likes_To") != "UNDEFINED" and dictionary.get("facebook_likes_To") is not None:
        sql_stmt += """ and facebook_likes_amount <= %s """
        parameters.append(dictionary.get("facebook_likes_To", 0))

    if dictionary.get("facebook_gender_distribution_female_from") != "UNDEFINED" and dictionary.get(
            "facebook_gender_distribution_female_from") is not None:
        sql_stmt += """ and facebook_gender_distribution_female >= %s """
        parameters.append(dictionary.get("facebook_gender_distribution_female_from", 0))

    if dictionary.get("facebook_gender_distribution_female_to") != "UNDEFINED" and dictionary.get(
            "facebook_gender_distribution_female_to") is not None:
        sql_stmt += """ and facebook_gender_distribution_female <= %s """
        parameters.append(dictionary.get("facebook_gender_distribution_female_to", 0))

    if dictionary.get("facebook_gender_distribution_male_from") != "UNDEFINED" and dictionary.get(
            "facebook_gender_distribution_male_from") is not None:
        sql_stmt += """ and facebook_gender_distribution_male >= %s """
        parameters.append(dictionary.get("facebook_gender_distribution_male_from", 0))

    if dictionary.get("facebook_gender_distribution_male_to") != "UNDEFINED" and dictionary.get(
            "facebook_gender_distribution_male_to") is not None:
        sql_stmt += """ and facebook_gender_distribution_male <= %s """
        parameters.append(dictionary.get("facebook_gender_distribution_male_to", 0))

    if dictionary.getlist("facebook_rhythm_types") is not None and len(dictionary.getlist("facebook_rhythm_types")) > 0:
        sql_stmt += """ and facebook_rhythm in """ + tuple_of_list(
            dictionary.getlist("facebook_rhythm_types"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("facebook_content") is not None and len(dictionary.getlist("facebook_content")) > 0:
        sql_stmt += """ and content_type_identifier in """ + tuple_of_list(
            dictionary.getlist("facebook_content"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("genders") is not None and len(dictionary.getlist("genders")) > 0:
        sql_stmt += """ and gender in """ + tuple_of_list(dictionary.getlist("genders"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("topics") is not None and len(dictionary.getlist("topics")) > 0:
        sql_stmt += """ and topic_identifier in """ + tuple_of_list(
            dictionary.getlist("topics"))  # TODO: WARNING: RISKY!

    if dictionary.get("homebase") is not "":
        sql_stmt += """ and homebase = %s"""
        parameters.append(dictionary.get("homebase"))

    if dictionary.getlist("deals") is not None and len(dictionary.getlist("deals")) > 0:
        sql_stmt += """ and deal_identifier in """ + tuple_of_list(dictionary.getlist("deals"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("facebook_countries") is not None and len(dictionary.getlist("facebook_countries")) > 0:
        sql_stmt += """ and country_identifier in """ + tuple_of_list(
            dictionary.getlist("facebook_countries"))  # TODO: WARNING: RISKY!

    sql_stmt += """ LIMIT 20 """
    if dictionary.get("offset"):
        if int(dictionary.get("offset")) >= 0 and int(dictionary.get("offset")) % 20 == 0:
            sql_stmt += """ OFFSET """ + dictionary.get("offset")
        else:
            return False

    sql_stmt += ";"

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    prm_tuple = tuple(x for x in parameters)
    try:
        cursor.execute(sql_stmt, prm_tuple)
        print(cursor.statement)
    except:
        print(sql_stmt)
        print(prm_tuple)
        print(cursor.statement)

    result = parse_list_tuples_to_list_dict(cursor.fetchall(), cursor.column_names)

    cursor.close()
    dbconnection.close()

    return result


def search_youtubers(dictionary: ImmutableMultiDict, booked_package) -> list:
    track_search('youtube', booked_package)
    sql_stmt = """
    SELECT DISTINCT influencer.influencer_identifier, last_name, first_name, email, phone_number, price, gender, homebase,
                birthyear, pwd_hash, joined_at, confirmed, youtube_username, youtube_follower_amount, youtube_post_amount,
                youtube_rhythm, youtube_gender_distribution_male, youtube_gender_distribution_female, youtube_age_distribution_min,
                youtube_age_distribution_max, youtube_page_views, youtube_impressions_amount, youtube_click_rate
    FROM influencer
        JOIN is_listed_on_youtube
            on influencer.influencer_identifier = is_listed_on_youtube.influencer_identifier
        LEFT OUTER JOIN influencer_covers_topic
            on influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
        LEFT OUTER JOIN influencer_deal
            on influencer.influencer_identifier = influencer_deal.influencer_identifier
        LEFT OUTER JOIN countries_of_channel
            on influencer.influencer_identifier = countries_of_channel.influencer_identifier and channel_identifier = 3
    WHERE is_listed_on_youtube.listing_on = 1 """

    parameters = []
    if dictionary.get("birthyear_from") != "UNDEFINED" and dictionary.get("birthyear_from") is not None:
        sql_stmt += """ AND birthyear >= %s """
        parameters.append(dictionary.get("birthyear_from", 0))

    if dictionary.get("birthyear_to") != "UNDEFINED" and dictionary.get("birthyear_to") is not None:
        sql_stmt += """ AND birthyear <= %s """
        parameters.append(dictionary.get("birthyear_to", 0))

    if dictionary.get("youtubeFollowerFrom") != "UNDEFINED" and dictionary.get("youtubeFollowerFrom") is not None:
        sql_stmt += """ AND youtube_follower_amount >= %s """
        parameters.append(dictionary.get("youtubeFollowerFrom", 0))

    if dictionary.get("youtubeFollowerTo") != "UNDEFINED" and dictionary.get("youtubeFollowerTo") is not None:
        sql_stmt += """ AND youtube_follower_amount <= %s """
        parameters.append(dictionary.get("youtubeFollowerTo", 0))

    if dictionary.get("youtube_age_distribution_from") != "UNDEFINED" and dictionary.get(
            "youtube_age_distribution_from") is not None:
        sql_stmt += """ AND youtube_age_distribution_min >= %s """
        parameters.append(dictionary.get("youtube_age_distribution_from", 0))

    if dictionary.get("youtube_age_distribution_to") != "UNDEFINED" and dictionary.get(
            "youtube_age_distribution_to") is not None:
        sql_stmt += """ AND youtube_age_distribution_max <= %s """
        parameters.append(dictionary.get("youtube_age_distribution_to", 0))

    if dictionary.get("youtube_gender_distribution_female_from") != "UNDEFINED" and dictionary.get(
            "youtube_gender_distribution_female_from") is not None:
        sql_stmt += """ AND youtube_gender_distribution_female >= %s """
        parameters.append(dictionary.get("youtube_gender_distribution_female_from", 0))

    if dictionary.get("youtube_gender_distribution_female_to") != "UNDEFINED" and dictionary.get(
            "youtube_gender_distribution_female_to") is not None:
        sql_stmt += """ AND youtube_gender_distribution_female <= %s """
        parameters.append(dictionary.get("youtube_gender_distribution_female_to", 0))

    if dictionary.get("youtube_gender_distribution_male_from") != "UNDEFINED" and dictionary.get(
            "youtube_gender_distribution_male_from") is not None:
        sql_stmt += """ AND youtube_gender_distribution_male >= %s """
        parameters.append(dictionary.get("youtube_gender_distribution_male_from", 0))

    if dictionary.get("youtube_gender_distribution_male_to") != "UNDEFINED" and dictionary.get(
            "youtube_gender_distribution_male_to") is not None:
        sql_stmt += """ AND youtube_gender_distribution_male <= %s """
        parameters.append(dictionary.get("youtube_gender_distribution_male_to", 0))

    if dictionary.get("youtube_click_rate_From") != "UNDEFINED" and dictionary.get(
            "youtube_click_rate_From") is not None:
        sql_stmt += """ AND youtube_click_rate >= %s """
        parameters.append(dictionary.get("youtube_click_rate_From", 0))

    if dictionary.get("youtube_click_rate_To") != "UNDEFINED" and dictionary.get("youtube_click_rate_To") is not None:
        sql_stmt += """ AND youtube_click_rate <= %s """
        parameters.append(dictionary.get("youtube_click_rate_To", 0))

    if dictionary.get("youtube_impressions_from") != "UNDEFINED" and dictionary.get(
            "youtube_impressions_from") is not None:
        sql_stmt += """ AND youtube_impressions_amount >= %s """
        parameters.append(dictionary.get("youtube_impressions_from", 0))

    if dictionary.get("youtube_impressions_to") != "UNDEFINED" and dictionary.get("youtube_impressions_to") is not None:
        sql_stmt += """ AND youtube_impressions_amount <= %s """
        parameters.append(dictionary.get("youtube_impressions_to", 0))

    if dictionary.get("youtube_post_amount_from") != "UNDEFINED" and dictionary.get(
            "youtube_post_amount_from") is not None:
        sql_stmt += """ AND youtube_post_amount >= %s """
        parameters.append(dictionary.get("youtube_post_amount_from", 0))

    if dictionary.get("youtube_post_amount_to") != "UNDEFINED" and dictionary.get("youtube_post_amount_to") is not None:
        sql_stmt += """ AND youtube_post_amount <= %s """
        parameters.append(dictionary.get("youtube_post_amount_to", 0))

    if dictionary.get("youtube_views_From") != "UNDEFINED" and dictionary.get("youtube_views_From") is not None:
        sql_stmt += """ AND youtube_page_views >= %s """
        parameters.append(dictionary.get("youtube_views_From", 0))

    if dictionary.get("youtube_views_To") != "UNDEFINED" and dictionary.get("youtube_views_To") is not None:
        sql_stmt += """ AND youtube_page_views <= %s """
        parameters.append(dictionary.get("youtube_views_To", 0))

    if dictionary.getlist("youtube_rhythm_types") is not None and len(dictionary.getlist("youtube_rhythm_types")) > 0:
        sql_stmt += """ and youtube_rhythm in """ + tuple_of_list(
            dictionary.getlist("youtube_rhythm_types"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("youtube_countries") is not None and len(dictionary.getlist("youtube_countries")) > 0:
        sql_stmt += """ and country_identifier in """ + tuple_of_list(
            dictionary.getlist("youtube_countries"))  # TODO: WARNING: RISKY!

    if dictionary.get("homebase") is not "":
        sql_stmt += """ and homebase = %s"""
        parameters.append(dictionary.get("homebase"))

    if dictionary.getlist("topics") is not None and len(dictionary.getlist("topics")) > 0:
        sql_stmt += """ and topic_identifier in """ + tuple_of_list(
            dictionary.getlist("topics"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("deals") is not None and len(dictionary.getlist("deals")) > 0:
        sql_stmt += """ and deal_identifier in """ + tuple_of_list(dictionary.getlist("deals"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("genders") is not None and len(dictionary.getlist("genders")) > 0:
        sql_stmt += """ and gender in """ + tuple_of_list(dictionary.getlist("genders"))  # TODO: WARNING: RISKY!

    sql_stmt += """ LIMIT 20 """
    if dictionary.get("offset"):
        if int(dictionary.get("offset")) >= 0 and int(dictionary.get("offset")) % 20 == 0:
            sql_stmt += """ OFFSET """ + dictionary.get("offset")
        else:
            return

    sql_stmt += ";"

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    prm_tuple = tuple(x for x in parameters)
    try:
        cursor.execute(sql_stmt, prm_tuple)
    except:
        print(sql_stmt)
        print(prm_tuple)
        print(cursor.statement)

    result = parse_list_tuples_to_list_dict(cursor.fetchall(), cursor.column_names)

    cursor.close()
    dbconnection.close()

    return result


def search_for_pinterest_users(dictionary: ImmutableMultiDict, booked_package) -> list:
    track_search('pinterest', booked_package)
    sql_stmt = """
    SELECT DISTINCT influencer.influencer_identifier, last_name, first_name, email, phone_number, price, gender, homebase,
                birthyear, pwd_hash, pinterest_username, pinterest_follower_amount, pinterest_post_amount, pinterest_rhythm,
                pinterest_viewer_amount
    FROM influencer
        JOIN is_listed_on_pinterest
            ON influencer.influencer_identifier = is_listed_on_pinterest.influencer_identifier
        LEFT OUTER JOIN influencer_covers_topic
            ON influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
        LEFT OUTER JOIN influencer_deal
            ON influencer.influencer_identifier = influencer_deal.influencer_identifier
        LEFT OUTER JOIN content_of_channel
            ON channel_identifier = 4 AND influencer.influencer_identifier = content_of_channel.influencer_identifier
    WHERE is_listed_on_pinterest.listing_on = 1"""

    parameters = []
    if dictionary.get("birthyear_from") != "UNDEFINED" and dictionary.get("birthyear_from") is not None:
        sql_stmt += """ AND birthyear >= %s """
        parameters.append(dictionary.get("birthyear_from", 0))

    if dictionary.get("birthyear_to") != "UNDEFINED" and dictionary.get("birthyear_to") is not None:
        sql_stmt += """ AND birthyear <= %s """
        parameters.append(dictionary.get("birthyear_to", 0))

    if dictionary.get("pinterestFollowerFrom") != "UNDEFINED" and dictionary.get("pinterestFollowerFrom") is not None:
        sql_stmt += """ AND pinterest_follower_amount >= %s """
        parameters.append(dictionary.get("pinterestFollowerFrom", 0))

    if dictionary.get("pinterestFollowerTo") != "UNDEFINED" and dictionary.get("pinterestFollowerTo") is not None:
        sql_stmt += """ AND pinterest_follower_amount <= %s """
        parameters.append(dictionary.get("pinterestFollowerTo", 0))

    if dictionary.get("pinterest_pins_amount_from") != "UNDEFINED" and dictionary.get(
            "pinterest_pins_amount_from") is not None:
        sql_stmt += """ AND pinterest_post_amount >= %s """
        parameters.append(dictionary.get("pinterest_pins_amount_from", 0))

    if dictionary.get("pinterest_pins_amount_to") != "UNDEFINED" and dictionary.get(
            "pinterest_pins_amount_to") is not None:
        sql_stmt += """ AND pinterest_post_amount <= %s """
        parameters.append(dictionary.get("pinterest_pins_amount_to", 0))

    if dictionary.get("pinterest_page_calls_From") != "UNDEFINED" and dictionary.get(
            "pinterest_page_calls_From") is not None:
        sql_stmt += """ AND pinterest_viewer_amount >= %s """
        parameters.append(dictionary.get("pinterest_page_calls_From", 0))

    if dictionary.get("pinterest_page_calls_To") != "UNDEFINED" and dictionary.get(
            "pinterest_page_calls_To") is not None:
        sql_stmt += """ AND pinterest_viewer_amount <= %s """
        parameters.append(dictionary.get("pinterest_page_calls_To", 0))

    if dictionary.getlist("pinterest_rhythm_types") is not None and len(
            dictionary.getlist("pinterest_rhythm_types")) > 0:
        sql_stmt += """ and pinterest_rhythm in """ + tuple_of_list(
            dictionary.getlist("pinterest_rhythm_types"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("topics") is not None and len(dictionary.getlist("topics")) > 0:
        sql_stmt += """ and topic_identifier in """ + tuple_of_list(
            dictionary.getlist("topics"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("deals") is not None and len(dictionary.getlist("deals")) > 0:
        sql_stmt += """ and deal_identifier in """ + tuple_of_list(dictionary.getlist("deals"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("genders") is not None and len(dictionary.getlist("genders")) > 0:
        sql_stmt += """ and gender in """ + tuple_of_list(dictionary.getlist("genders"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("pinterest_content") is not None and len(dictionary.getlist("pinterest_content")) > 0:
        sql_stmt += """ and content_type_identifier in """ + tuple_of_list(
            dictionary.getlist("pinterest_content"))  # TODO: WARNING: RISKY!

    if dictionary.get("homebase") is not "":
        sql_stmt += """ and homebase = %s"""
        parameters.append(dictionary.get("homebase"))

    sql_stmt += """ LIMIT 20 """
    if dictionary.get("offset"):
        if int(dictionary.get("offset")) >= 0 and int(dictionary.get("offset")) % 20 == 0:
            sql_stmt += """ OFFSET """ + dictionary.get("offset")
        else:
            return

    sql_stmt += ";"

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    prm_tuple = tuple(x for x in parameters)
    try:
        cursor.execute(sql_stmt, prm_tuple)
    except:
        print(sql_stmt)
        print(prm_tuple)
        print(cursor.statement)

    result = parse_list_tuples_to_list_dict(cursor.fetchall(), cursor.column_names)

    cursor.close()
    dbconnection.close()

    return result


def search_for_blogger(dictionary: ImmutableMultiDict, booked_package) -> list:
    track_search('blog', booked_package)
    sql_stmt = """
    SELECT DISTINCT influencer.influencer_identifier, last_name, first_name, email, phone_number, price, gender, homebase,
                birthyear, pwd_hash, joined_at, blog_domain, blog_follower_amount, blog_post_amount, blog_rhythm,
                blog_page_views_amount
    FROM influencer
        JOIN is_listed_on_personal_blog
            ON influencer.influencer_identifier = is_listed_on_personal_blog.influencer_identifier
        LEFT OUTER JOIN influencer_covers_topic
            ON influencer.influencer_identifier = influencer_covers_topic.influencer_identifier
        LEFT OUTER JOIN influencer_deal
            ON influencer.influencer_identifier = influencer_deal.influencer_identifier
        LEFT OUTER JOIN content_of_channel
            ON channel_identifier = 5 AND influencer.influencer_identifier = content_of_channel.influencer_identifier
    WHERE is_listed_on_personal_blog.listing_on = 1"""

    parameters = []
    if dictionary.get("birthyear_from") != "UNDEFINED" and dictionary.get("birthyear_from") is not None:
        sql_stmt += """ AND birthyear >= %s """
        parameters.append(dictionary.get("birthyear_from", 0))

    if dictionary.get("birthyear_to") != "UNDEFINED" and dictionary.get("birthyear_to") is not None:
        sql_stmt += """ AND birthyear <= %s """
        parameters.append(dictionary.get("birthyear_to", 0))

    if dictionary.get("personal_blogFollowerFrom") != "UNDEFINED" and dictionary.get(
            "personal_blogFollowerFrom") is not None:
        sql_stmt += """ AND blog_follower_amount >= %s """
        parameters.append(dictionary.get("personal_blogFollowerFrom", 0))

    if dictionary.get("personal_blogFollowerTo") != "UNDEFINED" and dictionary.get(
            "personal_blogFollowerTo") is not None:
        sql_stmt += """ AND blog_follower_amount <= %s """
        parameters.append(dictionary.get("personal_blogFollowerTo", 0))

    if dictionary.get("personal_blog_page_calls_From") != "UNDEFINED" and dictionary.get(
            "personal_blog_page_calls_From") is not None:
        sql_stmt += """ AND blog_post_amount >= %s """
        parameters.append(dictionary.get("personal_blog_page_calls_From", 0))

    if dictionary.get("personal_blog_post_amount_from") != "UNDEFINED" and dictionary.get(
            "personal_blog_post_amount_from") is not None:
        sql_stmt += """ AND blog_post_amount >= %s """
        parameters.append(dictionary.get("personal_blog_post_amount_from", 0))

    if dictionary.get("personal_blog_post_amount_to") != "UNDEFINED" and dictionary.get(
            "personal_blog_post_amount_to") is not None:
        sql_stmt += """ AND blog_post_amount <= %s """
        parameters.append(dictionary.get("personal_blog_post_amount_to", 0))

    if dictionary.getlist("personal_blog_rhythm_types") is not None and len(
            dictionary.getlist("personal_blog_rhythm_types")) > 0:
        sql_stmt += """ and blog_rhythm in """ + tuple_of_list(
            dictionary.getlist("personal_blog_rhythm_types"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("topics") is not None and len(dictionary.getlist("topics")) > 0:
        sql_stmt += """ and topic_identifier in """ + tuple_of_list(
            dictionary.getlist("topics"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("personal_blog_content") is not None and len(dictionary.getlist("personal_blog_content")) > 0:
        sql_stmt += """ and content_type_identifier in """ + tuple_of_list(
            dictionary.getlist("personal_blog_content"))  # TODO: WARNING: RISKY!

    if dictionary.getlist("deals") is not None and len(dictionary.getlist("deals")) > 0:
        sql_stmt += """ and deal_identifier in """ + tuple_of_list(dictionary.getlist("deals"))  # TODO: WARNING: RISKY!

    if dictionary.get("homebase") is not "":
        sql_stmt += """ and homebase = %s"""
        parameters.append(dictionary.get("homebase"))

    sql_stmt += """ LIMIT 20 """
    if dictionary.get("offset"):
        if int(dictionary.get("offset")) >= 0 and int(dictionary.get("offset")) % 20 == 0:
            sql_stmt += """ OFFSET """ + dictionary.get("offset")
        else:
            return

    sql_stmt += ";"

    print("PARAMS>>" + str(parameters))

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    prm_tuple = tuple(x for x in parameters)

    print("TUPLE>>" + str(prm_tuple))

    try:
        cursor.execute(sql_stmt, prm_tuple)
    except:
        print(sql_stmt)
        print(prm_tuple)
        print(cursor.statement)

    result = parse_list_tuples_to_list_dict(cursor.fetchall(), cursor.column_names)

    cursor.close()
    dbconnection.close()

    return result


def parse_list_tuples_to_list_dict(db_query_result: list, column_names: list) -> list:
    list_to_return = []

    for entry in db_query_result:
        temp_dict = {}
        for index in range(0, len(column_names)):
            temp_dict[column_names[index]] = entry[index]
        list_to_return.append(temp_dict)

    print(list_to_return)

    return list_to_return


def get_matching_profiles_as_list(get_params: ImmutableMultiDict, booked_package: str) -> list:
    if get_params.get("channelSelect"):
        identifier = int(get_params.get("channelSelect"))
        methods = [search_influencer_related, search_instagrammer, search_facebook_user, search_youtubers,
                   search_for_pinterest_users, search_for_blogger]
        try:
            return methods[identifier](get_params, booked_package)
        except IndexError:
            raise InvalidGETRequest
    else:
        raise InvalidGETRequest


def tuple_of_list(list: list) -> str:
    if len(list) > 0 and len(list) != 1:
        return str(tuple(item for item in list))
    elif len(list) == 1:
        result = "('{}')".format(list[0])
        print(result)
        return result
    else:
        print(list)


def get_passed_params_back(dictionary: ImmutableMultiDict) -> dict:
    return_dict = {}
    for key in dictionary.keys():
        if len(dictionary.getlist(key)) > 1:
            return_dict[key] = dictionary.getlist(key)
        else:
            return_dict[key] = dictionary.get(key)
    return return_dict


def get_stored_queries_of_company(company_identifier: int) -> list:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(
        """SELECT search_identifier, timestamp, search_href, title FROM company_stores_search WHERE company_identifier = %s ORDER BY timestamp DESC;""",
        (company_identifier,))

    result = cursor.fetchall()

    cursor.close()
    dbconnection.close()

    return result


def delete_stored_query(company_identifier: int, search_identifier: str):
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""DELETE FROM company_stores_search WHERE search_identifier = %s and company_identifier = %s;""",
                   (search_identifier, company_identifier))

    dbconnection.commit()

    cursor.close()
    dbconnection.close()
