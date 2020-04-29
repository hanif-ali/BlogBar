import json
import pdfkit
import os
from Core.Exceptions.User import UserCoversNotTheRequestedChannel
from Core.Option_values import delete_cooperation
from Core.profile_views import get_data_for_profile_view
from Core.PayPal_Integration import change_subscription_package
from flask import Flask, render_template
from flask import url_for
from werkzeug.utils import secure_filename

from flask import (
    redirect,
    request,
    session,
    send_file
)
from Core.API.API_Permnissions import (
    check_if_user_owns_campaign
)
from Core.Exceptions.Search import (
    InvalidGETRequest,
    CampaignDoesNotExist
)
from Core.Exceptions.User import (
    UserNotLoggedIn,
    UsernameAlreadyExists
)
from Core.admin.getter_setter.API_EXECUTION_DASHBOARD import (
    get_signup_data_sevendays_influencer,
    get_signup_data_sevendays_company,
    get_signup_data_today_influencer,
    get_signup_data_today_company,
    get_kpis,
    get_dates
)
from Core.admin.usermanagement import (
    delete_influencer_account_with_mail_address_from_database,
    delete_instagram_entry,
    delete_facebook_entry,
    delete_youtube_entry,
    delete_pinterest_entry,
    delete_personal_blog_entry,
    delete_company_profile,
    book_package,
    get_all_reported_profiles,
    delete_influencer_with_id,
    ignore_reported_influencer_db_execution
)
from Core.categories import (
    get_templates_getters_and_setters,
    get_view_data_of_admin_view
)
from Core.dbconn import get_database_connection
from Core.invoice_rendering import (
    create_invoice_db_entry,
    get_data_of_invoice_with_uuid,
    genrate_invoice_token,
    get_book_confirmation_mailing_data_usind_the_uuid
)
from Core.mailing import (
    send_pwd_reset_token,
    send_log_in_alert,
    send_booked_package_confirmation_mail
)
from Core.API.API_Execution import (
    unpin_user_from_campaign,
    delete_campaign_db,
    pin_influencer,
    store_search,
    delete_public_campaign_with_identifier
)
from Core.Usermanagement import (
    check_if_email_already_taken,
    create_user,
    create_company_profile,
    validate_data_using_union_view,
    set_confirm_status_to_true,
    set_new_password,
    get_subscription_package_of_company_with_identifier,
    report_influencer)
from Core.campaigns import (
    get_campaigns_basic_view,
    get_data_of_specific_campaign,
    add_campaign, edit_campaign
)
from Core.public_campaigns import (
    add_public_campaign,
    get_all_public_campaigns,
    get_all_public_campaigns_that_fit_with,
    get_details_of_public_campaign_with_identifier,
    get_campaigns_of_company_with_identifier,
    get_pdf_source, update_campaign)
from Core.search import (
    search_influencer_related,
    search_instagrammer,
    get_matching_profiles_as_list,
    get_passed_params_back,
    get_stored_queries_of_company,
    delete_stored_query
)
