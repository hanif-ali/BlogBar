#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from Core.dbconn import get_database_connection


def check_if_user_owns_campaign(kind: int, user_id: int, campaign_id: int) -> bool:
    """

    :param kind:
    :param user_id:
    :param campaign_id:
    :return:
    """
    if kind == 2:
        dbconnection = get_database_connection()

        cursor = dbconnection.cursor()

        cursor.execute("""SELECT * FROM campaign WHERE company_identifier = %s and campaign_identifier = %s""",
                       (user_id, campaign_id))

        if len(cursor.fetchall()) > 0:
            return True

        cursor.close()

        dbconnection.close()

    return False
