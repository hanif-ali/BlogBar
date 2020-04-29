from Core.dbconn import get_database_connection


def unpin_user_from_campaign(influencer_identifier: int, campaign_identifier: int) -> bool:
    dbconnection = get_database_connection()

    cursor = dbconnection.cursor()

    cursor.execute("""DELETE FROM is_pinned_on_campaign WHERE campaign_identifier=%s and influencer_identifier = %s;""",
                   (campaign_identifier, influencer_identifier))

    dbconnection.commit()

    cursor.close()

    dbconnection.close()

    return True


def delete_campaign_db(campaign_identifier: int) -> bool:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""DELETE FROM campaign WHERE campaign_identifier=%s;""",
                   (campaign_identifier,))

    dbconnection.commit()

    cursor.close()
    dbconnection.close()

    return True


def pin_influencer(campaign_identifier: int, influencer_identifier: int, remark: str) -> bool:
    sql = """
    INSERT INTO is_pinned_on_campaign(influencer_identifier, campaign_identifier, remark) 
    VALUES (%s, %s, %s)
    """

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute(sql, (influencer_identifier, campaign_identifier, remark))

    dbconnection.commit()

    cursor.close()
    dbconnection.close()
    return True


def store_search(search: str, title: str, company_identifier: int) -> bool:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()
    try:
        cursor.execute(
            """INSERT INTO company_stores_search(company_identifier, search_href, title) VALUES (%s, %s, %s);""",
            (company_identifier, search.split("?")[1], title))
        print("EXECUTEED")
    except IndexError:
        return False

    dbconnection.commit()

    cursor.close()
    dbconnection.close()

    return True


def delete_public_campaign_with_identifier(campaign_identifier: int, company_identifier: int) -> bool:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    stmt = """DELETE FROM company_offers_campaign WHERE campaign_identifier = %s AND company_identifier = %s"""

    cursor.execute(stmt, (campaign_identifier, company_identifier))

    dbconnection.commit()

    cursor.close()
    dbconnection.close()

    return True  # How to check without any affected_rows method ?!
