import functools
import yaml
from werkzeug.exceptions import abort
from Core.constants import *
from Core.supporting.imports import *

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/<string:language_abbr>/resetcookiedecision', methods=['GET'])
def resetCookieDecision(language_abbr):
    session['cookiesConfirmed'] = None
    return redirect("/" + language_abbr + "/solution")


@app.route('/')
def index():
    return redirect("/de/solution")


@app.route("/<string:language_abbr>/")
def start_with_language(language_abbr):
    return redirect("/" + language_abbr + "/solution")


@app.route("/<string:language_abbr>")
def start_with_language_without_second_slash(language_abbr):
    return redirect("/" + language_abbr + "/solution")


########################################################################################################################
#### USERMANAGEMENT
####
@app.route("/<string:language_abbr>/signupinfl", methods=["GET"])
def signup_as_influencer(language_abbr) -> any:
    return render_template("usermanagement/signup_influencer.html", signupinfl_act="active", **get_required_params(language_abbr))


@app.route("/<string:language_abbr>/signupinfl", methods=["POST"])
def finish_signup(language_abbr):
    keys = ["firstName", "lastName", "mail", "telephoneNumber", "gender", "birthyear", "pwd"]
    params = {}
    for key in keys:
        params[key] = request.form.get(key)

    print(params)

    error = False
    error_text: str

    if request.form.get("pwd") != request.form.get("pwd2"):
        error = True
        error_text = "Error: Passwörter stimmen nicht überein."

    if check_if_email_already_taken(request.form.get("mail")):
        error = True
        error_text = "Error: eMail-Adresse is bereits vergeben."

    if error:
        return render_template("usermanagement/signup_influencer.html", error=error_text, **params, **get_required_params(language_abbr))

    if create_user(**params, language_abbr=language_abbr):
        return render_template("usermanagement/confirm_invitation.html", **get_required_params(language_abbr))
    return redirect(f"{language_abbr}/signupinfl")


###
### Alternative paths
@app.route("/<string:language_abbr>/signup", methods=['GET'])
def sign_up_rdt(language_abbr):
    return redirect("/{}/signupinfl".format(language_abbr))


@app.route("/<string:language_abbr>/go", methods=['GET'])
def sign_up_redirect(language_abbr):
    return welcome(language_abbr)


@app.route("/<string:language_abbr>/welcome")
def welcome(language_abbr):
    return redirect("/{lang}/signupinfl".format(lang=language_abbr))


@app.route("/<string:language_abbr>/signupcomp", methods=['GET'])
def signup_as_company(language_abbr):
    return render_template("usermanagement/sign_up_company.html", signupcomp_act="active",
                           **get_required_params(language_abbr))


@app.route("/<string:language_abbr>/signupcomp", methods=["POST"])
def finish_signup_comp(language_abbr):
    # TODO: Check if the following three lines are necessary
    keys = ["companyName", "contact", "contactMail", "streetWithHouseNumber", "postcode", "place", "pwd", "ust_id"]
    params = {}
    for key in keys:
        params[key] = request.form.get(key)

    print(params)

    error = False
    error_text: str

    if request.form.get("pwd") != request.form.get("pwd2"):
        error = True
        error_text = "Error: Passwörter stimmen nicht überein."

    if error:
        return render_template("usermanagement/sign_up_company.html", error=error_text, **params,
                               **get_required_params(language_abbr))
    else:
        if check_if_email_already_taken(request.form.get("contactMail")):
            # TODO: English version of this error msg???
            return render_template("usermanagement/sign_up_company.html", error="EMail-Adresse wird bereits verwendet",
                                   **params, **get_required_params(language_abbr))
        if create_company_profile(**params, language_abbr=language_abbr):
            return render_template("usermanagement/confirm_invitation.html", **get_required_params(language_abbr))
        else:
            return render_template("usermanagement/sign_up_company.html",
                                   error="Registrierung nicht möglich. Bitte kontaktieren Sie unseren <u>Support</u>.",
                                   **params,
                                   **get_required_params(language_abbr))


@app.route("/<string:language_abbr>/login", methods=["GET"])
def general_login_view(language_abbr):
    if check_if_logged_in():
        return redirect("/")
    return render_template("usermanagement/sign_in.html", **get_required_params(language_abbr))


@app.route("/<string:language_abbr>/login", methods=["POST"])
def general_login(language_abbr):
    params = {}
    for key in ["mail", "pwd"]:
        params[key] = request.form.get(key)

    check = validate_data_using_union_view(**params)
    if check[0]:
        app.secret_key = os.urandom(24)
        session["identifier"] = check[1]
        session["kind"] = check[2]
        if check[2] == 1:
            send_log_in_alert(check[1])
        return redirect("/profile")
    else:
        try:
            return render_template("usermanagement/sign_in.html", error=check[1], **get_required_params(language_abbr),
                                   **params)
        except UserNotLoggedIn:
            return redirect("/" + language_abbr)


@app.route("/<string:language_abbr>/saved_queries", methods=['GET'])
def get_saved_searches(language_abbr) -> any:
    try:
        if get_kind_of_user() == 2:
            return render_template("enterprise_views/saved_queries.html", **get_required_params(language_abbr),
                                   queries=get_stored_queries_of_company(get_user_identifier()))
        else:
            return redirect("/" + language_abbr)
    except UserNotLoggedIn:
        return redirect("/" + language_abbr)


@app.route("/<string:language_abbr>/preferences")
def show_preferences_overview(language_abbr) -> any:
    try:
        if get_kind_of_user() == 1:
            return render_template("preferences/index.html", **get_required_params(language_abbr),
                                   preferences_act="active")
        elif get_kind_of_user() == 2:
            return render_template("company_preferences/index.jinja2.html", **get_required_params(language_abbr),
                                   preferences_act="active")
    except UserNotLoggedIn:
        return redirect("/" + language_abbr)


# PERSONAL OVERVIEW
@app.route("/<string:language_abbr>/profile")
def get_profile_of_my_profile(language_abbr):
    try:
        if get_kind_of_user() == 1:
            return render_template("profile_overview/public_views/profile_overview_index.jinja2",
                                   **get_required_params(language_abbr),
                                   profile_act="active",
                                   influencer_data=get_data_for_profile_view(get_user_identifier()),
                                   subscription_packet="prime"
                                   )
    except UserNotLoggedIn:
        pass

    return redirect("/" + language_abbr)


# PUBLIC VIEW
@app.route("/<string:language_abbr>/<int:influencer_identifier>/overview")
def get_profile_overview_of(language_abbr, influencer_identifier):
    return render_template("profile_overview/public_views/profile_overview_index.jinja2",
                           **get_required_params(language_abbr),
                           profile_act="active",
                           subscription_packet=get_subscription_package(),
                           influencer_data=get_data_for_profile_view(influencer_identifier)
                           )


@app.route("/<string:language_abbr>/report_influencer_profile/<int:influencer_identifier>", methods=['GET'])
def get_report_options_for_profile(language_abbr, influencer_identifier):
    return render_template("miscellaneous/report_influencer_profile.html",
                           **get_required_params(language_abbr)
                           )


@app.route("/<string:language_abbr>/report_influencer_profile/<int:influencer_identifier>", methods=['POST'])
def receive_complainoing_or_report_of_an_influencer(language_abbr, influencer_identifier):
    report_influencer(
        influencer_identifier,
        request.form.get("contact"),
        request.form.get("reportReason"),
        request.form.get("remark")
    )

    return redirect("/" + language_abbr + "/" + str(influencer_identifier) + "/overview")


@app.route("/<string:language_abbr>/confirm")
def double_opt_in(language_abbr):
    try:
        if set_confirm_status_to_true(request.args.get("key")):
            return render_template("usermanagement/confirm_success.html", status=True,
                                   **get_required_params(language_abbr))
    except:
        return redirect("/")
    return redirect("/")


@app.route("/<string:language_abbr>/logout")
def logout(language_abbr: str) -> any:
    session.clear()
    app.secret_key = os.urandom(24)
    return redirect("/" + language_abbr)


####
####
########################################################################################################################
####Company-views
####
@app.route("/<string:language_abbr>/campaigns", methods=['GET'])
def return_rendered_personal_campaigns(language_abbr: str) -> any:
    if get_type_of_user_identifier() == 2 and check_if_logged_in():
        return render_template("enterprise_views/nonpublic_campaigns.html", **get_required_params(language_abbr),
                               campaigns=get_campaigns_basic_view(get_user_identifier()),
                               nonpublic_campaigns_act="active")
    else:
        return redirect("/" + language_abbr)


@app.route("/<string:language_abbr>/campaigns/<int:campaign_id>", methods=['GET'])
def return_rendered_personal_specific_campagin(language_abbr: str, campaign_id: int) -> any:
    if get_type_of_user_identifier() == 2 and check_if_logged_in():
        data = get_data_of_specific_campaign(campaign_id)
        return render_template("/enterprise_views/specific_campaign.html", **get_required_params(language_abbr),
                               specific_campaign_data=data, nonpublic_campaigns_act="active")
    else:
        return redirect("/" + language_abbr + "/campaigns")


########################################################################################################################
#### Public Views
####
@app.route("/<string:language_abbr>/faq")
def return_rendered_faq(language_abbr):
    return render_template("faq/faq_index.html", **get_required_params(language_abbr), faq_act="active")


@app.route("/<string:language_abbr>/solution")
def render_elevator_pitch(language_abbr):
    return render_template("solution_overview_elevator_pitch.jinja2", solution_act="active",
                           **get_required_params(language_abbr))


@app.route("/<string:language_abbr>/search", methods=['GET'])
def return_search_masks(language_abbr):
    imgs = []
    try:
        package = 'basic_nli'
        try:
            if get_kind_of_user() == 2:
                package = get_subscription_package()
        except:
            pass
        search_results = get_matching_profiles_as_list(request.args, package)
        for influencer in search_results:
            identifier = influencer["influencer_identifier"]
            try:
                dirs = os.listdir(UPLOAD_FOLDER + "/{}".format(identifier))
                for f in dirs:
                    if not f.startswith('.') and f.__contains__("0"):
                        imgs.append("{}/{}/{}".format("/static/pb", identifier, f))
                        break
            except:
                imgs.append(None)
    except IndexError:
        pass
    except InvalidGETRequest:
        search_results = []

    try:
        if get_kind_of_user() == 2:
            campaigns = get_campaigns_basic_view(get_user_identifier())
            subscription_packet = get_subscription_package_of_company_with_identifier(get_user_identifier())
        else:
            campaigns = None
            subscription_packet = "basic"
    except UserNotLoggedIn:
        campaigns = None
        subscription_packet = "basic"

    return render_template("search_and_filter/results.html",
                           search_act="active",
                           subscription_packet=subscription_packet,
                           **get_required_params(language_abbr),
                           **get_passed_params_back(request.args),
                           search_results=search_results,
                           campaigns=campaigns,
                           imgs=imgs
                           )


########################################################################################################################
#### If Influencer is logged in
####
@app.route("/<string:language_abbr>/marketplace")
def return_rendered_market_place(language_abbr):
    return redirect("/" + language_abbr + "publiccampagins")


@app.route("/<string:language_abbr>/preferences/<string:submenue>/<string:suboption>", methods=['GET'])
def return_preferences_template(language_abbr, submenue, suboption):
    try:
        # INFLUENCER:
        if get_kind_of_user() == 1:
            template_getter_setter_dict = get_templates_getters_and_setters().get(submenue, "profile").get(suboption,
                                                                                                           "user")

            try:
                return render_template(
                    template_getter_setter_dict["template"],
                    **template_getter_setter_dict["getter"](user_id=session["identifier"]),
                    **get_required_params(language_abbr))
            except KeyError:
                return redirect("/{lang}".format(lang=language_abbr))
            except UserCoversNotTheRequestedChannel:
                return render_template(template_getter_setter_dict["template"], **get_required_params(language_abbr),
                                       state=False)
        # COMPANY:
        elif get_kind_of_user() == 2:
            if suboption == "delete":
                render_all_invoices_of_company_with_identifier(get_user_identifier())
            template_getter_setter_dict = get_templates_getters_and_setters().get("company").get(suboption, "base")

            try:
                return render_template(template_getter_setter_dict["template"],
                                       **template_getter_setter_dict["getter"](
                                           company_identifier=session["identifier"]),
                                       **get_required_params(language_abbr))
            except KeyError:
                return redirect("/{lang}".format(lang=language_abbr))
    except UserNotLoggedIn:
        pass
    return redirect("/{lang}".format(lang=language_abbr))


@app.route("/<string:language_abbr>/preferences/<string:submenue>/<string:suboption>", methods=['POST'])
def receive_preference_values(language_abbr, submenue, suboption):
    try:
        if suboption == "galery":
            for i in range(0, 5):
                if 'image_file_{}'.format(i) not in request.files:
                    print("NOT IN")
                    continue
                file = request.files['image_file_{}'.format(i)]
                if file.filename == '':
                    continue
                if file:
                    filename = secure_filename(file.filename)
                    if not check_if_logged_in() and get_kind_of_user() == 1:
                        return redirect("/" + language_abbr)
                    if not os.path.exists("{}/{}".format(UPLOAD_FOLDER, get_user_identifier())):
                        os.makedirs("{}/{}".format(UPLOAD_FOLDER, get_user_identifier()))
                    else:
                        for item in os.listdir("{}/{}".format(UPLOAD_FOLDER, get_user_identifier())):
                            if item.startswith("profile_image_{0}".format(i)):
                                os.remove("{}/{}/{}".format(UPLOAD_FOLDER, get_user_identifier(), item))
                    file.save(os.path.join(UPLOAD_FOLDER + "/" + str(get_user_identifier()),
                                           "profile_image_{0}.{1}".format(i, filename.split(".")[-1])))
                else:
                    print(file)
                    print("NO FILE")
            return redirect("/" + language_abbr + "/preferences")

        elif suboption == "logo":
            if 'company_logo' in request.files:
                pass
            file = request.files["company_logo"]
            if file.filename == '':
                pass
            if file:
                filename = secure_filename(file.filename)
                if not check_if_logged_in() and get_kind_of_user() == 2:
                    return redirect("/" + language_abbr)
                else:
                    for item in os.listdir(LOGO_FOLDER):
                        if item.split(".")[0].endswith("logo_company_{}".format(get_user_identifier())):
                            os.remove("{}/{}".format(LOGO_FOLDER, item))
                file.save(
                    os.path.join(
                        LOGO_FOLDER,
                        "logo_company_{0}.{1}".format(
                            get_user_identifier(), filename.split(".")[-1]
                        )
                    )
                )
            else:
                print(file)
                print("NO FILE")
            return redirect("/" + language_abbr + "/preferences")

        elif submenue == "user" and suboption == "delete":
            get_templates_getters_and_setters().get("profile").get("delete").get("setter")(get_user_identifier(),
                                                                                           request.form)
            session.clear()
            app.secret_key = os.urandom(24)
            return redirect("/" + language_abbr)
        else:
            template_getter_setter_dict = get_templates_getters_and_setters().get(submenue, "profile").get(
                suboption, "user")
            try:
                try:
                    if template_getter_setter_dict["setter"](get_user_identifier(), request.form):
                        print("SUCCESS")
                except UsernameAlreadyExists:
                    return render_template(
                        template_getter_setter_dict["template"],
                        **template_getter_setter_dict["getter"](user_id=session["identifier"]),
                        **get_required_params(language_abbr),
                        error="USERNAME/URL_ALREDY_EXISTS"
                    )
                if suboption == "delete":
                    session.clear()
                    app.secret_key = os.urandom(24)
                    return redirect("/" + language_abbr)
            except UserNotLoggedIn:
                return redirect("/" + language_abbr + "/")

        return redirect("/" + language_abbr + "/preferences")
    except UserNotLoggedIn:
        return redirect("/" + language_abbr)


@app.route("/<string:language_abbr>/preferences/<string:submenu>")
def render_submenu(language_abbr: str, submenu: str) -> any:
    if check_if_logged_in():
        try:
            return render_template({
                                       "profile": "preferences/subviews/topic_overviews/profile.html",
                                       "channels": "preferences/subviews/topic_overviews/channels.html"
                                   }[submenu], **get_required_params(language_abbr))
        except KeyError:
            return redirect("/{language_abbr}".format(language_abbr=language_abbr))


def get_type_of_user_identifier() -> int:
    try:
        return session.get("kind")
    except:
        raise UserNotLoggedIn


def get_required_params(language_in_path: str) -> dict:
    return {"logged_in": check_if_logged_in(),
            "language_abbr": get_language_abbreviation(language_in_path),
            "kind": get_type_of_user_identifier(),
            "admin": get_admin_state(),
            "subscribtion_package": get_subscription_package(),
            'cookiesConfirmed': session.get('cookiesConfirmed')}


def check_if_logged_in() -> bool:
    try:
        if session["identifier"]:
            return True
    except KeyError:
        return False


def get_language_abbreviation(language_given_in_path: str) -> str:
    if session.get("language") == None:

        if check_if_logged_in() == True:

            dbconnection = get_database_connection()
            cursor = dbconnection.cursor()

            if get_kind_of_user() == 1:
                cursor.execute("""SELECT language_abbr FROM influencer WHERE influencer_identifier = %s""", (
                    get_user_identifier(),
                ))
            else:
                cursor.execute("""SELECT language_abbr FROM company WHERE company_identifier = %s""", (
                    get_user_identifier(),
                ))
            result = cursor.fetchone()
            cursor.close()
            dbconnection.close()

            lang = result[0]
            session["language"] = lang

            if language_given_in_path != lang:
                set_language_in_session(language_given_in_path)

        session["language"] = "de"
    return session.get("language")


@app.route('/api/set_language', methods=['POST'])
def set_language():
    langauge_abbreveatiom = json.loads(request.data)['abbr']

    set_language_in_session(langauge_abbreveatiom)

    return "CORRECT", 200


def set_language_in_session(abbr: str) -> None:
    session["language"] = abbr

    if check_if_logged_in():
        dbconnection = get_database_connection()
        cursor = dbconnection.cursor()

        if get_kind_of_user() == 1:
            cursor.execute("""UPDATE influencer SET language_abbr = %s WHERE influencer_identifier = %s""", (
                abbr,
                get_user_identifier()
            ))
        else:
            cursor.execute("""UPDATE company SET language_abbr = %s WHERE company_identifier = %s""", (
                abbr,
                get_user_identifier()
            ))

        dbconnection.commit()
        cursor.close()
        dbconnection.close()

    session["language"] = abbr


@app.route("/api/remove_cooperation", methods=['POST'])
def delete_cooperation_api_call():
    if check_if_logged_in():
        if get_kind_of_user() == 1:
            delete_cooperation(json.loads(request.data)['ID'], get_user_identifier())
            return 'CORRECT'


def get_user_identifier() -> int:
    try:
        return session["identifier"]
    except KeyError:
        raise UserNotLoggedIn


def get_kind_of_user() -> int:
    try:
        return session["kind"]
    except KeyError:
        raise UserNotLoggedIn


def get_admin_state():
    try:
        return session["admin"]
    except KeyError:
        return False


####
# Receiver for client-side-actions:


@app.route("/api/unpin_user_from_campaign", methods=['POST'])
def get_post_request():
    data = request.data
    dataDict = json.loads(data)
    print(dataDict)
    try:
        if check_if_user_owns_campaign(get_kind_of_user(), get_user_identifier(), dataDict["campaign_id"]):
            if unpin_user_from_campaign(dataDict["user_id"], dataDict["campaign_id"]):
                return "CORRECT"
            else:
                return "Influencer not pinned on campaign"
    except UserNotLoggedIn:
        return "You must be logged in as campaign-owner"
    except KeyError:
        return "Wrong params"
    return "You must be logged in as campaign-owner"


@app.route("/api/delete_campaign", methods=["POST"])
def delete_campaign():
    data = request.data
    dataDict = json.loads(data)
    print(dataDict)
    try:
        if check_if_user_owns_campaign(get_kind_of_user(), get_user_identifier(), dataDict["campaign_id"]):
            if delete_campaign_db(dataDict["campaign_id"]):
                return "CORRECT"
            return "campaign with given ID does not exist"
    except UserNotLoggedIn:
        return "You must be logged in as campaign-owner"
    except KeyError:
        return "Wrong params"
    return "You must be logged in as campaign-owner"


@app.route("/api/admin/ignore_reported_influencer", methods=["POST"])
def ignore_reported_influencer():
    data = request.data
    dataDict = json.loads(data)
    print(dataDict)
    try:
        if get_admin_state():
            if ignore_reported_influencer_db_execution(dataDict["report_identifier"]):
                return "CORRECT", 200
            return "user with given ID does not exist", 405
        else:
            return "You must be logged in as admin", 403
    except KeyError:
        return "Wrong params", 405
    return "You must be logged in as campaign-owner", 403


@app.route("/api/adminoptions/delete_influencer_profile", methods=["POST"])
def delete_reported_influencer():
    data = request.data
    dataDict = json.loads(data)
    print(dataDict)
    try:
        if get_admin_state():
            if delete_influencer_with_id(dataDict["influencerIdentifier"]):
                return "CORRECT", 200
        else:
            return "You have to be logged in as admin", 403
    except KeyError:
        return "Wrong params", 405
    return "You must be logged in as an admin", 403


@app.route("/api/delete_profile_image", methods=['POST'])
def delete_profile_image_from_galery():
    img_id = json.loads(request.data)["img_identifier"]
    if check_if_logged_in() and get_kind_of_user() == 1:
        try:
            os.remove("{}/{}/{}".format(UPLOAD_FOLDER, get_user_identifier(), img_id))
        except:
            return "INTERNAL SERVER ERROR", 500
        return "CORERCT", 200

    return "", 401


@app.route("/api/pin_influencer", methods=['POST'])
def pin_influencer_api():
    if pin_influencer(json.loads(request.data)["campaign_id"], json.loads(request.data)["influencer_identifier"],
                      json.loads(request.data)["remark"]):
        return "CORRECT"
    return "already pinned"


@app.route("/api/delete_public_campaign", methods=['POST'])
def delete_campaign_with_identifier():
    try:
        if get_kind_of_user() == 2:
            delete_public_campaign_with_identifier(json.loads(request.data)["campaign_identifier"],
                                                   get_user_identifier())
            return "CORRECT"
    except UserNotLoggedIn:
        pass
    return redirect("/")


@app.route("/api/save_search", methods=['POST'])
def store_the_search():
    try:
        if check_if_logged_in() and get_kind_of_user() == 2:
            if store_search(json.loads(request.data)["search"], json.loads(request.data)["title"],
                            get_user_identifier()):
                return "CORRECT"
        else:
            return "A company must be logged in"
    except UserNotLoggedIn:
        return "A company must be logged in"
    except KeyError:
        return "Manipulated Params"
    except:
        pass
    return "INTERNAL ERROR"


@app.route("/api/delete_query", methods=['POST'])
def delete_query():
    try:
        if get_kind_of_user() == 2:
            delete_stored_query(get_user_identifier(), json.loads(request.data)["timestamp"])
            return "CORRECT"
        else:
            return "Company must be logged in"
    except UserNotLoggedIn:
        return "INTERNAL ERROR"


@app.route("/api/request_pwd_reset_token", methods=['POST'])
def request_pwd_reset():
    import re

    if re.match(r"[^@]+@[^@]+\.[^@]+", json.loads(request.data)["mail"]):
        send_pwd_reset_token(json.loads(request.data)["mail"])

    return "", 200


@app.route("/<string:language_abbr>/campaigns", methods=['POST'])
def receive_new_campaign(language_abbr: str) -> any:
    params = request.form

    try:
        if params.get("add_campaign"):
            if add_campaign(params["campaign_name"], params["description"], get_user_identifier()):
                redirect("/" + language_abbr + "/campaigns")
        elif params.get("edit_campaign"):
            if edit_campaign(params["identifier"], params["campaign_name"], params["description"],
                             get_user_identifier()):
                redirect("/" + language_abbr + "/campaigns")
        else:
            return redirect("/" + language_abbr)
    except (KeyError, UserNotLoggedIn):
        return redirect("/" + language_abbr)

    return return_rendered_personal_campaigns(language_abbr)


@app.route("/<string:language_abbr>/pwd_reset", methods=['GET'])
def reset_pwd(language_abbr: str):
    print(request.args.get("token"))
    return render_template("usermanagement/restore_pwd.html", **get_required_params(language_abbr),
                           token=request.args.get("token"))


@app.route("/<string:language_abbr>/pwd_reset", methods=['POST'])
def reset_pwd_receiver(language_abbr: str):
    print(request.form.get("pwd"))
    set_new_password(request.form.get("pwd"), request.form.get("token"))
    return redirect("/" + str(language_abbr) + "/login")


@app.route("/robots.txt")
def get_crawl_info() -> any:
    return render_template("robots.txt")


def get_title_img(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


def get_subscription_package():
    try:
        if get_kind_of_user() == 2:
            subscription_packet = get_subscription_package_of_company_with_identifier(get_user_identifier())
        else:
            subscription_packet = "basic"
    except UserNotLoggedIn:
        subscription_packet = "basic"

    return subscription_packet


@app.route("/<language_abbr>/book/<string:package>")
def get_book_mask(language_abbr, package):
    amounts = ('239.00', '399.00')  # PRIME-Amounts
    amounts_vat = ('284.41', '474.81')
    s_pack = "PRIME"
    if package == "pro":
        s_pack = "PRO"
        amounts = ('119.00', '199.00')
        amounts_vat = ('141,61', '236.81')

    return render_template("company_preferences/views/book/checkout_view.html", **get_required_params(language_abbr),
                           amount=amounts, package=s_pack, amounts_vat=amounts_vat)


@app.route("/api/booked_package", methods=['POST'])
def book_request() -> any:
    try:
        if get_kind_of_user() == 2:

            change_subscription_package(
                get_user_identifier(),
                json.loads(request.data)["package"],
                int(json.loads(request.data)["months"]))

            token = genrate_invoice_token()

            create_invoice_db_entry(
                get_user_identifier(),
                json.loads(request.data)["package"],
                int(json.loads(request.data)["months"]),
                float(json.loads(request.data)["amount"]),
                token
            )

            send_booked_package_confirmation_mail(
                **get_book_confirmation_mailing_data_usind_the_uuid(token)
            )

            kwargs = get_book_confirmation_mailing_data_usind_the_uuid(token)
            kwargs.update(contact_email="cheers@blogbar.eu")

            print(kwargs)

            send_booked_package_confirmation_mail(
                **kwargs
            )
        else:
            return "Forbidden", 403

    except UserNotLoggedIn:
        pass
    return "CORRECT"


@app.route("/<string:language_abbr>/publiccampaigns", methods=['GET'])
def get_all_campaigns_view(language_abbr: str) -> any:
    try:
        if get_subscription_package() != "prime" and get_kind_of_user() == 2:
            return redirect("/" + get_required_params(language_abbr)["language_abbr"])
        if len(request.args) == 0:
            return render_template(
                "market_place/start_page.html",
                **get_required_params(language_abbr),
                campaigns=get_all_public_campaigns(),
                subscr_package=get_subscription_package(),
                marketplace_act="active"
            )
        search_results = get_all_public_campaigns_that_fit_with(request.args.getlist("topic"),
                                                                request.args.getlist("channels"))
        return render_template(
            "market_place/start_page.html",
            **get_required_params(language_abbr),
            **get_passed_params_back(request.args),
            campaigns=search_results,
            subscr_package=get_subscription_package(),
            marketplace_act="active"
        )
    except:
        return redirect("/" + get_required_params(language_abbr)["language_abbr"])


@app.route("/<string:language_abbr>/publiccampagins/<int:campaignidentifier>", methods=['GET'])
def get_specific_public_campaign_view(language_abbr: str, campaignidentifier: int) -> any:
    try:
        data = get_details_of_public_campaign_with_identifier(campaignidentifier)
        return render_template("market_place/details_of_campaign.html", **get_required_params(language_abbr),
                               marketplace_act="active", **data)
    except CampaignDoesNotExist:
        return redirect("/" + language_abbr + "/publiccampaign")


@app.route("/<string:language_abbr>/publiccampaigns/create", methods=['GET'])
def get_create_campaign_view(language_abbr: str) -> any:
    try:
        if get_kind_of_user() == 2 and get_subscription_package() == "prime":
            return render_template("market_place/company_prime/create_campaign.html",
                                   **get_required_params(language_abbr))
        return redirect("/" + language_abbr + "/publiccampaigns")
    except UserNotLoggedIn:
        return redirect("/" + language_abbr)


@app.route("/<string:language_abbr>/publiccampaigns/<int:public_campaign_identifier>/edit", methods=['GET'])
def edit_public_camapign_as_prime_user(language_abbr: str, public_campaign_identifier: int) -> any:
    try:
        if get_kind_of_user() == 2 and get_subscription_package() == "prime":
            return render_template(
                "market_place/company_prime/edit_campaign.html",
                **get_required_params(language_abbr),
                **get_details_of_public_campaign_with_identifier(
                    campaign_identifier=public_campaign_identifier,
                ),
                marketplace_act="active"
            )
        return redirect("/" + language_abbr + "/publiccampaigns")
    except UserNotLoggedIn:
        return redirect("/" + language_abbr)


@app.route("/<string:language_abbr>/publiccampaigns/overview", methods=['GET'])
def get_overview_of_campaigns(language_abbr: str) -> any:
    try:
        if get_kind_of_user() == 2 and get_subscription_package() == "prime":
            return render_template(
                "market_place/company_prime/mycampaigns.html",
                **get_required_params(language_abbr),
                campaigns=get_campaigns_of_company_with_identifier(get_user_identifier()),
                marketplace_act="active"
            )
        return redirect("/" + language_abbr + "/publiccampaigns")
    except UserNotLoggedIn:
        return redirect("/" + language_abbr)


@app.route("/<string:language_abbr>/publiccampaigns/create", methods=['POST'])
def receive_campaign_creation_request(language_abbr: str) -> any:
    try:
        if get_kind_of_user() == 2:
            if add_public_campaign(get_user_identifier(), request.form, request.files):
                return redirect("/" + language_abbr + "/publiccampaigns")
    except UserNotLoggedIn:
        return redirect("/" + language_abbr)
    return redirect("/" + language_abbr + "/publiccampaigns")


@app.route("/<string:language_abbr>/publiccampaigns/<int:public_campaign_identifier>/edit", methods=['POST'])
def receive_updated_public_campaign(language_abbr: str, public_campaign_identifier: int) -> any:
    try:
        if get_kind_of_user() == 2 and get_subscription_package() == "prime":
            update_campaign(public_campaign_identifier, get_user_identifier(), request.form, request.files)
            return redirect("/" + language_abbr + "/publiccampaigns")
        return redirect("/" + language_abbr + "/publiccampaigns")
    except UserNotLoggedIn:
        return redirect("/" + language_abbr)


@app.route("/download/campaigndetails/<int:campaign_identifier>")
def download_pdf(campaign_identifier):
    try:
        return send_file(
            "/root/webapplication/static/campaigns/details_campaign_reference_no_{0}.pdf".format(campaign_identifier),
            as_attachment=True)
    except FileNotFoundError:
        return "DOES NOT EXITST"


@app.route("/<string:language_abbr>/download/<string:filetype>", methods=['GET'])
def download_file(language_abbr: str, filetype: str) -> any:
    with open('downloadable_files.yaml', 'r') as f:
        config = yaml.safe_load(f.read())

        file = config.get(filetype)

        if file:
            return send_file(
                f"{PATH_PREFIX}/{file.get(language_abbr, config.get(filetype).get('default'))}",
                as_attachment=file.get("attachment")
            )

    return abort(404)


@app.route('/api/cookieDecision', methods=['POST'])
def receiveCookie():
    session['cookiesConfirmed'] = json.loads(request.data).get('decision')
    return '', 200


@app.route("/admin", methods=["GET"])
def return_admin_panel():
    if get_admin_state():
        suinfl_seven = get_signup_data_sevendays_influencer()
        sucomp_seven = get_signup_data_sevendays_company()

        results = []
        sums = []

        helper_list = list()

        if sucomp_seven is None:
            helper_list.append(None)
        else:
            helper_list.append(sucomp_seven.values())

        if suinfl_seven is None:
            helper_list.append(None)
        else:
            helper_list.append(suinfl_seven.values())

        # The following code requires one signup for each group a week
        for entries in helper_list:
            tempSum = 0
            if entries is not None:
                for entry in entries:
                    tempSum += int(entry)
            sums.append(tempSum)
            results.append(tempSum / (len(entries) if entries is not None else 1))
        return render_template("admin/logged_in/index.html", **get_required_params("de"), **get_kpis(),
                               averages=results, sums=sums)
    else:
        return render_template("admin/not_logged_in/login_invitation.html", **get_required_params("de"))


@app.route("/admin", methods=["POST"])
def receive_token():
    if request.form.get("token") == "BB+blogbar1906":
        session["admin"] = True
        return return_admin_panel()
    else:
        session["admin"] = False
        return render_template("admin/not_logged_in/login_invitation.html", **get_required_params("de"),
                               error="ungültiger_token")


@app.route("/admin/kpis", methods=["GET"])
def get_admin_view():
    if get_admin_state():
        suinfl_seven = get_signup_data_sevendays_influencer()
        sucomp_seven = get_signup_data_sevendays_company()
        suinfl_day = get_signup_data_today_influencer()
        sucomp_day = get_signup_data_today_company()

        dictionary = {
            "signUpsLastSevenDays": {
                "dates": get_dates(),
                "companies": list(sucomp_seven.values()) if sucomp_seven is not None else [0 for i in range(7)],
                "influencer": list(suinfl_seven.values()) if suinfl_seven is not None else [0 for i in range(7)],
            },
            "signUpToday": {
                "hours": sucomp_day.keys(),
                "companies": sucomp_day.values(),
                "influencer": suinfl_day.values()
            }
        }

        print(dictionary)

        return render_template("admin/logged_in/kpis/index.html", **get_required_params("de"), **get_kpis(),
                               **dictionary)
    return redirect("/admin")


@app.route("/admin/usermanagement", methods=['GET'])
def get_usermanagement_option_of_admin():
    if get_admin_state():
        return render_template("admin/logged_in/usermanagement/index.html", **get_required_params("de"))
    else:
        return redirect("/admin")


# Reported influencers:
@app.route("/admin/d", methods=['GET'])
def get_d_options_of_admin():
    if get_admin_state():
        return render_template("admin/logged_in/d/index.html", **get_required_params("de"),
                               reported_influencers=get_all_reported_profiles())
    else:
        return redirect("/admin")


###RECEIVE DASHBOARD FORM-POSTS
@app.route("/admin/post/influencer_action", methods=['POST'])
def receive_influencer_action_performed_by_admin():
    if get_admin_state():
        if request.form.get("influencerAction") == '1':
            delete_influencer_account_with_mail_address_from_database(request.form.get("mail"))
        elif request.form.get("influencerAction") == '3':
            delete_instagram_entry(request.form.get("mail"))
        elif request.form.get("influencerAction") == '4':
            delete_facebook_entry(request.form.get("mail"))
        elif request.form.get("influencerAction") == '5':
            delete_youtube_entry(request.form.get("mail"))
        elif request.form.get("influencerAction") == '6':
            delete_pinterest_entry(request.form.get("mail"))
        elif request.form.get("influencerAction") == '7':
            delete_personal_blog_entry(request.form.get("mail"))
        else:
            return redirect("/admin/usermanagement")
        return redirect("/admin/usermanagement")
    else:
        return redirect("/admin/usermanagement")


@app.route("/admin/post/company_action", methods=['POST'])
def receive_company_action_performed_by_admin():
    if get_admin_state():
        if request.form.get("companyAction") == '1':
            delete_company_profile(request.form.get("mail"))
        elif request.form.get("companyAction") == '3':
            book_package(request.form.get("mail"), 'basic')
        elif request.form.get("companyAction") == '4':
            book_package(request.form.get("mail"), 'pro', 6)
        elif request.form.get("companyAction") == '5':
            book_package(request.form.get("mail"), 'pro', 12)
        elif request.form.get("companyAction") == '6':
            book_package(request.form.get("mail"), 'prime', 6)
        elif request.form.get("companyAction") == '7':
            book_package(request.form.get("mail"), 'prime', 12)
        else:
            return redirect("/admin/usermanagement")
        return redirect("/admin/usermanagement")
    else:
        return redirect("/admin/usermanagement")


@app.route("/invoice/<string:token>", methods=['GET'])
def return_invoice_as_pdf(token: str) -> any:
    if not os.path.exists('/root/webapplication/static/invoices/invoice_{token}.pdf'.format(token=token)):
        pdfkit.from_string(render_template('/invoice_template.html',
                                           **get_data_of_invoice_with_uuid(
                                               token)),
                           '/root/webapplication/static/invoices/invoice_{token}.pdf'.format(token=token))
    return send_file('/root/webapplication/static/invoices/invoice_{token}.pdf'.format(token=token), as_attachment=True)


def render_all_invoices_of_company_with_identifier(company_identifier: int):
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""SELECT token FROM invoice_data WHERE company_identifier = %s""", (
        company_identifier,
    ))

    results = cursor.fetchall()

    for entries in results:
        token = entries[0]

        pdfkit.from_string(render_template('/invoice_template.html',
                                           **get_data_of_invoice_with_uuid(
                                               token)),
                           '/root/webapplication/static/invoices/invoice_{token}.pdf'.format(token=token))


#### Dashboard:
@app.route("/api/dashboard/signups", methods=["POST"])
def get_sign_ups() -> any:
    suinfl_seven = get_signup_data_sevendays_influencer()
    sucomp_seven = get_signup_data_sevendays_company()
    suinfl_day = get_signup_data_today_influencer()
    sucomp_day = get_signup_data_today_company()

    dictionary = {
        "signUpsLastSevenDays": {
            "dates": suinfl_seven.keys(),
            "companies": sucomp_seven.values(),
            "influencer": suinfl_seven.values()
        },
        "signUpToday": {
            "hours": sucomp_day.keys(),
            "companies": sucomp_day.values(),
            "influencer": suinfl_day.values()
        }
    }

    return json.dumps(dictionary)


@app.route("/utils/generate_pdf", methods=['GET'])
def generate_invoice():
    try:
        pdfkit.from_string(render_template('/invoice_template.html',
                                           **get_data_of_invoice_with_uuid(
                                               "xpk18777ele11786iud2252qqn204242txb189229lut170228")
                                           ),
                           'out.pdf'
                           )
        return "200"
    except KeyboardInterrupt:
        return "500"


@app.route("/<string:language_abbr>/imprint", methods=['GET'])
def get_imprint(language_abbr: str) -> any:
    return render_template("/miscellaneous/imprint.html", **get_required_params(language_abbr))


if __name__ == '__main__':
    app.run(port='5000', host='127.0.0.1', debug=True)
