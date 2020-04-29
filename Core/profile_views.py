# basic_view = {
#     "influencer": {
#         "gender": True, "name": True, "mail":
#     }
# }
#
# pro_view = {
#
# }
#
# prime_view = {
#
# }
from Core.Option_values import get_profile_pictures_sources
from Core.dbconn import get_database_connection


def get_topic_name(index: int) -> str:
    """

    :param index:
    :return:
    """
    topics_de = ['Auto und Motorrad', 'Beauty / Kosmetik', 'Bildung', 'Computer und Elektronik', 'DIY', 'Design',
                 'Erfolg und Karriere',
                 'Essen und Trinken / Food', 'Fashion / Mode', 'Finanzen', 'Fotografie', 'Frauen / Männer',
                 'Garten und Natur',
                 'Gesellschaft und Politik', 'Gesundheit', 'Home und Living', 'Humor und Spaß', 'Kinder und Familie',
                 'Kino, Film, TV',
                 'Kunst und Kultur', 'Liebe und Sexualität', 'Lifestyle', 'Luxus', 'Marketing', 'Musik',
                 'Recht und Gesetz',
                 'Reise / Travel', 'Social Media', 'Spiele und Gaming', 'Sport und Fitness', 'Tattos', 'Technik',
                 'Tiere']
    return topics_de[index]


def get_language_name(index: int) -> str:
    """

    :param index:
    :return:
    """
    languages_de = ["Englisch", "Deutsch"]

    return languages_de[index]


def get_deal_name(index: int) -> str:
    """

    :param index:
    :return:
    """
    deals_de = ["Barzahlung", "WKZ", "nach Absprache"]

    return deals_de[index]


def get_content_type_name(index: int) -> str:
    """
    Convert the index to a human interpretable string
    :param index:
    :return: String, that a human being will understand instead of the index
    """
    return ["Post", "Story", "Video"][index - 1]


def get_data_for_profile_view(influencer_identifier: int):
    """

    :param influencer_identifier:
    :return:
    """
    influencer_data = {}
    channel_identifiers = {
        "is_listed_on_facebook": 2,
        "is_listed_on_instagram": 1,
        "is_listed_on_personal_blog": 5,
        "is_listed_on_pinterest": 4,
        "is_listed_on_youtube": 3
    }

    for channel in ["is_listed_on_facebook", "is_listed_on_instagram", "is_listed_on_personal_blog",
                    "is_listed_on_pinterest", "is_listed_on_youtube"]:
        dbconnection = get_database_connection()
        cursor = dbconnection.cursor()

        cursor.execute("SELECT * FROM " + channel + " WHERE influencer_identifier = %s AND listing_on = 1;",
                       (influencer_identifier,))

        print(cursor.statement)

        results = cursor.fetchone()
        keys = cursor.column_names

        cursor.close()

        if results is not None:
            cursor = dbconnection.cursor()
            cursor.execute(
                """SELECT content_type_identifier FROM content_of_channel WHERE influencer_identifier=%s and channel_identifier=%s;""",
                (
                    influencer_identifier, channel_identifiers[channel]
                ))
            content_types = list()

            for content_type in cursor.fetchall():
                content_types.append(get_content_type_name(content_type[0]))

            try:
                channel_data = {}
                for index in range(0, len(keys)):
                    try:
                        channel_data[keys[index]] = results[index]
                    except KeyError:
                        break
                channel_data["content_types"] = content_types
                influencer_data[channel] = channel_data
            except IndexError:
                pass

    cursor = dbconnection.cursor()

    cursor.execute("SELECT * FROM influencer WHERE influencer_identifier = %s", (influencer_identifier,))

    results = cursor.fetchone()
    keys = cursor.column_names

    cursor.close()

    for index in range(0, len(keys)):
        influencer_data[keys[index]] = results[index]

    cursor = dbconnection.cursor()

    cursor.execute("SELECT topic_identifier FROM influencer_covers_topic WHERE influencer_identifier = %s",
                   (influencer_identifier,))

    results = cursor.fetchall()

    topics = []

    try:
        for entry in results:
            topics.append(get_topic_name(entry[0]))
    except IndexError:
        pass

    influencer_data["topics"] = topics

    cursor.close()

    cursor = dbconnection.cursor()

    cursor.execute("SELECT language_identifer FROM influencer_channel_language WHERE influencer_identifier = %s",
                   (influencer_identifier,))

    results = cursor.fetchall()

    languages = []
    try:
        for entry in results:
            languages.append(get_language_name(entry[0]))
    except IndexError:
        pass

    influencer_data["languages"] = languages

    cursor.close()

    cursor = dbconnection.cursor()

    cursor.execute("SELECT deal_identifier FROM influencer_deal WHERE influencer_identifier = %s",
                   (influencer_identifier,))

    results = cursor.fetchall()

    deals = []
    try:
        for entry in results:
            deals.append(get_deal_name(entry[0]))
    except IndexError:
        pass

    influencer_data["deal_types"] = deals

    cursor.close()

    cursor = dbconnection.cursor()

    cursor.execute("SELECT * FROM influencer_had_previous_cooperation WHERE influencer_identifier = %s;", (
        influencer_identifier,
    ))

    results = cursor.fetchall()
    keys = cursor.column_names

    return_list = []
    for dataset in results:
        temp_dict = {}
        for key_index in range(0, len(keys)):
            temp_dict[keys[key_index]] = dataset[key_index]
        return_list.append(temp_dict)

    influencer_data["cooperations"] = return_list

    cursor.close()
    dbconnection.close()

    influencer_data["profile_pictures"] = get_profile_pictures_sources(user_id=influencer_identifier)

    print(influencer_data)

    return influencer_data
