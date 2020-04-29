import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random

# from Core.Usermanagement import get_user_type_and_langage # ToDo: recursive import !!! Fix this Issue

from Core.dbconn import get_database_connection

footer = """
            <footer style="font-family: Calibri;"><br><br><br>
                <img src="https://blogbar.eu/static/img/Mailingfooterlogo.jpg" width="300px;"><br><br><br>
                <p>
                    BlogBar Digital Network UG (haftungsbeschränkt)<br>
                    Krausstr. 1<br>
                    63897 Miltenberg
                </p>
                <p>
                    <a href="www.blogbar.eu">www.blogbar.eu</a><br>
                    <a href="mailto:cheers@blogbar.eu">cheers@blogbar.eu</a><br>
                    Tel. 0176 8747 9127
                </p>
            
                <p>
                    Firmensitz: Miltenberg<br>
                    Registergericht: Amtsgericht Aschaffenburg HRB 15208<br>
                    Umsatzsteuer-Identifikationsnummer gem. § 27a UStG: DE325297281<br>
                    Geschäftsführer: Axel Sommer, Carolin Wolz<br>
                </p>
            </footer>
        """


def get_user_type_and_langage(mail: str) -> (int, str):
    """

    :param mail:
    :return: (int, str) ==> (kind, language_abbr)
    """
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""SELECT KIND, LANG, NAME FROM sign_up_view WHERE MAIL=%s;""", (
        mail,
    ))

    result = cursor.fetchall()[0]

    result = (result[0], result[1], result[2])

    cursor.close()
    dbconnection.close()

    return result


def get_random_string() -> str:
    alphabeth = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "q", "r", "s",
                 "t", "u", "u", "v", "w", "x", "y", "z"]
    string = ""
    for i in range(0, 3):
        string += alphabeth[random.randint(0, len(alphabeth) - 1)]
    return string


def generate_token_pn():
    token = ""
    for i in range(0, 15):
        token += get_random_string()
        for i in range(0, 2):
            token += str(random.randint(0, 255))
    print(token)
    return token


def generate_pwd_reset_token(mail_addr: str) -> str:
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    token = generate_token_pn()
    try:
        cursor.execute("""
        INSERT INTO pwd_reset_tokens(token, email) VALUES (%s, %s)""", (token, mail_addr))
        print(cursor.statement)
    except:
        cursor.execute("""
        UPDATE pwd_reset_tokens SET token = %s WHERE email = %s""", (token, mail_addr))
        print(cursor.statement)

    dbconnection.commit()

    cursor.close()
    dbconnection.close()

    return token


def send_double_opt_in_request(receiver_mail, first_name, kind: int, language: str):
    sender_email = "noreply@blogbar.eu"
    password = "BlogBar2103#"

    message = MIMEMultipart("alternative")
    message[
        "Subject"] = "BlogBar: E-Mail-Adresse bestätigen!" if language == "de" else "BlogBar: Confirm E-Mail-Address!"
    message["From"] = sender_email
    message["To"] = receiver_mail

    confirm_key = generate_token_pn()

    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""DELETE FROM confirm_keys WHERE email = %s""", (receiver_mail,))
    cursor.execute("""INSERT INTO confirm_keys(email, token) VALUES (%s, %s)""", (receiver_mail, confirm_key))

    print("INSERTED FOR: {mail}".format(
        mail=receiver_mail,
    ))

    dbconnection.commit()

    cursor.close()
    dbconnection.close()

    # Create the plain-text and HTML version of your message
    if kind == 2:
        if language == 'de':
            text = """\
            Hallo {first_name},
            
            vielen Dank für Ihre Registrierung bei BlogBar. Wir freuen uns, Sie bei der Suche nach passenden Influencer unterstützen zu können.
            Bevor es losgehen kann, bitte bestätigen Sie Ihre E-Mailadresse durch folgenden Link: https://blogbar.eu/de/confirm?key={key}
            Im Anschluss können Sie sich direkt einloggen und das passende Paket für Ihre Anforderungen buchen.
            Bitte beachten Sie: Sofern Sie den Link innerhalb von 3 Tagen nicht bestätigen, wird die Anmeldung zurückgesetzt und Ihre Daten gelöscht.
            Bei Fragen stehen wir gerne zur Verfügung. 
        
            Ihr Team von BlogBar""".format(first_name=first_name, key=confirm_key)
            html = """\
            <html>
              <body style="font-family: Calibri;">
                <p>Hallo {first_name},<br><br>
                   vielen Dank für Ihre Registrierung bei BlogBar. Wir freuen uns, Sie bei der Suche nach passenden Influencer unterstützen zu können.
                    Bevor es losgehen kann, bitte bestätigen Sie Ihre E-Mailadresse durch folgenden Link:<br>
                   <a href="https://blogbar.eu/de/confirm?key={key}">Jetzt bestätigen</a>
                   <br>
                   <br>
                   Bitte beachten Sie: Sofern Sie den Link innerhalb von 3 Tagen nicht bestätigen, wird die Anmeldung zurückgesetzt und Ihre Daten gelöscht.
            Bei Fragen stehen wir gerne zur Verfügung.
                    <br>
                   <br>
                   Wir freuen uns, dass du unserer Plattform beigetreten bist.<br><br>
                   Your team from BlogBar!
                </p>
                
              </body>
              {footer}
            </html>
            """.format(first_name=first_name,
                       key=confirm_key,
                       footer=footer)
        else:
            text = """\
                    Hello {first_name},

                    Thank you for registering at BlogBar. We are happy to assist you in your search for suitable influencers.
                    Before you can start, please confirm your e-mail address with the following link: https://blogbar.eu/de/confirm?key={key}
                    Then you are able to log in directly and book the right package for your requirements.

                    Please note: If you do not confirm the link within 3 days, the registration will be reset and your data deleted.
                    
                    If you have any questions, please do not hesitate to contact us.
                    
                    Your team from BlogBar""".format(first_name=first_name, key="4567898765456789098765678909876567890")
            html = """\
                    <html>
                      <body style="font-family: Calibri;">
                        <p>Hello {first_name},<br><br>
                           Thank you for registering at BlogBar. We are happy to assist you in your search for suitable influencers.
                    Before you can start, please confirm your e-mail address with the following link:<br>
                           <a href="https://blogbar.eu/de/confirm?key={key}">Confirm now!</a>
                           <br>
                           <br>
                           Then you are able to log in directly and book the right package for your requirements.
                            Please note: If you do not confirm the link within 3 days, the registration will be reset and your data deleted.
                            <br>
                            If you have any questions, please do not hesitate to contact us.
                           <br>
                           <br>
                           Your team from BlogBar!
                           {footer}
                        </p>
                      </body>
                    </html>
                    """.format(first_name=first_name,
                               key=confirm_key,
                               footer=footer)
    else:
        if language == 'de':
            text = """\
                    Hallo {first_name},
    
                    wir freuen uns sehr, dass du ab sofort Teil unserer Community bist.
                    Bevor es losgehen kann, bitte bestätige deine E-Mailadresse durch folgenden Link: https://blogbar.eu/de/confirm?key={key}
                    Im Anschluss kannst du dich direkt einloggen und deine Daten jederzeit anpassen.
                    Bitte beachten: Sofern du den Link innerhalb von 3 Tagen nicht bestätigst, wird die Anmeldung zurückgesetzt und deine Daten gelöscht.
                    Bei Fragen stehen wir gerne zur Verfügung. 
                    
                    Dein Team von BlogBar""".format(first_name=first_name, key="4567898765456789098765678909876567890")
            html = """\
                    <html>
                      <body style="font-family: Calibri;">
                        <p>Hallo {first_name},<br><br>
                           wir freuen uns sehr, dass du ab sofort Teil unserer Community bist.
                    Bevor es losgehen kann, bitte bestätige deine E-Mailadresse durch folgenden Link:<br>
                           <a href="https://blogbar.eu/de/confirm?key={key}">Bestätigen</a>
                           <br>
                           <br>
                           Im Anschluss kannst du dich direkt einloggen und deine Daten jederzeit anpassen.
                            Bitte beachten: Sofern du den Link innerhalb von 3 Tagen nicht bestätigst, wird die Anmeldung zurückgesetzt und deine Daten gelöscht.
                            Bei Fragen stehen wir gerne zur Verfügung. 
                            <br>
                           <br>
                           Wir freuen uns, dass du unserer Plattform beigetretn bist.<br><br>
                        </p>
                        <p>Dein Team von BlogBar</p>
                      </body>
                      {footer}
                    </html>
                    """.format(first_name=first_name,
                               key=confirm_key,
                               footer=footer)
        else:
            text = """\
                   Hello {first_name},

                   we are very happy that you are part of our community now. Before you can start, please confirm your e-mail address with the following link:https://blogbar.eu/de/confirm?key={key}
                   Afterwards you can log in directly and change your data every  time. 
                    Please note: If you do not confirm the link within 3 days, the registration will be reset and your data deleted. 
                    If you have any questions, please do not hesitate to contact us.

                   Your team from BlogBar""".format(first_name=first_name,
                                                    key="4567898765456789098765678909876567890")
            html = """\
                   <html>
                     <body style="font-family: Calibri;">
                       <p>Hello {first_name},<br><br>
                          we are very happy that you are part of our community now.
                        Before you can start, please confirm your e-mail address with the following link:
                        <br>
                          <a href="https://blogbar.eu/de/confirm?key={key}">Confirm by clicking this link</a>
                          <br>
                          <br>
                          Afterwards you can log in directly and change your data every time.
                            Please note: If you do not confirm the link within 3 days, the registration will be reset and your data deleted.
                            If you have any questions, please do not hesitate to contact us.
                       </p>
                       <br><br>
                        <p>Your Team from BlogBar</p>
                     </body>
                     {footer}
                   </html>
                   """.format(first_name=first_name, key=confirm_key, footer=footer)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.ionos.de", 465, context=context) as server:
        server.login(sender_email, password)
        try:
            server.sendmail(
                sender_email, receiver_mail, message.as_string()
            )
        except smtplib.SMTPRecipientsRefused:
            # EMail-Address not taken
            pass


def send_pwd_reset_token(receiver_mail):
    kind, language, name = get_user_type_and_langage(receiver_mail)

    sender_email = "noreply@blogbar.eu"
    password = "BlogBar2103#"

    message = MIMEMultipart("alternative")
    message["Subject"] = "BlogBar: Passwort zurücksetzen" if language == "de" else "BlogBar: Reset your Password"
    message["From"] = sender_email
    message["To"] = receiver_mail

    token = generate_pwd_reset_token(receiver_mail)

    if language == "de":
        if kind == 1:
            text = """
                        Hallo {name},
                        Mit folgendem Link kannst du dein Passwort zurücksetzen:
                        https://blogbar.eu/de/pwd_reset?token={key}
                        Viele Grüße,
                        Dein Team von BlogBar
                        """.format(key=token, name=name)

            html = """\
                       <html>
                         <body style="font-family: Calibri;">
                           <p>
                              Hallo {name},<br><br>
                              Mit folgendem Link kannst du dein Passwort zurücksetzen:<br>
                              <a href="https://blogbar.eu/de/pwd_reset?token={key}">Passwort zurücksetzten</a>
                           </p>
                           <p><br>Viele Grüße,<br><br>Dein Team von BlogBar</br></p>
                         </body>
                         {footer}
                       </html>
                       """.format(key=token, footer=footer, name=name)
        else:
            text = """
            Hallo Frau / Herr {name},
            Mit folgendem Link können Sie Ihr Passwort zurücksetzen:
            https://blogbar.eu/de/pwd_reset?token={key}
            Viele Grüße,
            Ihr Team von BlogBar
            """.format(key=token, name=name)

            html = """\
           <html>
             <body style="font-family: Calibri;">
               <p>
                  Hallo Frau / Herr {name},<br><br>
                  Mit folgendem Link können Sie Ihr Passwort zurücksetzen:<br>
                  <a href="https://blogbar.eu/de/pwd_reset?token={key}">Passwort zurücksetzten</a>
               </p>
               <p>Viele Grüße,<br><br>Ihr Team von BlogBar</p>
             </body>
             {footer}
           </html>
           """.format(key=token, footer=footer, name=name)

    else:
        if kind == 1:
            text = """
                  Hello {name},
                    With the following link you can reset your password:
                   https://blogbar.eu/de/pwd_reset?token={key}
                   Best regards,
                   Your team from BlogBar
                   """.format(key=token, name=name)

            html = """\
                  <html>
                    <body style="font-family: Calibri;">
                      <p>
                         Hello {name},<br><br>
                        With the following link you can reset your password:<br>
                         <a href="https://blogbar.eu/de/pwd_reset?token={key}">Reset password</a>
                      </p>
                      <p>Best regards, <br><br>Your team from BlogBar</p>
                    </body>
                    {footer}
                  </html>
                  """.format(key=token, footer=footer, name=name)

        else:
            text = """
                      Hello Mrs / Mr {name},
                        With the following link you can reset your password:
                       https://blogbar.eu/de/pwd_reset?token={key}
                       Best regards,
                       Your team from BlogBar
                       """.format(key=token, name=name)

            html = """\
                      <html>
                        <body style="font-family: Calibri;">
                          <p>
                             Hello Mrs / Mr {name},<br><br>
                            With the following link you can reset your password:<br>
                             <a href="https://blogbar.eu/de/pwd_reset?token={key}">Reset password</a>
                          </p>
                          <p>Best regards, <br><br>Your team from BlogBar</p>
                        </body>
                        {footer}
                      </html>
                      """.format(key=token, footer=footer, name=name)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.ionos.de", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_mail, message.as_string()
            )
    except:
        pass

    print(receiver_mail)


def send_log_in_alert(influencer_identifier: int):
    dbconnection = get_database_connection()
    cursor = dbconnection.cursor()

    cursor.execute("""SELECT * FROM influencer WHERE influencer_identifier = %s;""", (influencer_identifier,))

    data = cursor.fetchone()
    keys = cursor.column_names

    cursor.close()
    dbconnection.close()

    influencer = {}

    for index in range(0, len(keys)):
        influencer[keys[index]] = data[index]

    sender_email = "noreply@blogbar.eu"
    password = "BlogBar2103#"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Sicherheitshinweis: Neue Anmeldung in Deinem BlogBar-Account"
    message["From"] = sender_email
    message["To"] = influencer["email"]

    text = """\
        Hi {first_name},
        
        es wurde sich vor kurzen in Dein BlogBar-Konto eingeloggt.
        Falls Du es selbst warst, kannst du diese Mail ignorieren.
        
        Falls Du das Gefühl haben solltest, eine fremde Person ist im Besitz deiner Zugangsdaten, solltest du diese unter
        den Kontoeinstellungen sofort ändern.""".format(first_name=influencer["first_name"])
    html = """\
        <html>
          <body style="font-family: Calibri;">
            <p>Hi {first_name},<br>
            <br>
               es wurde sich vor kurzen in Dein BlogBar-Konto eingeloggt.<br>
                Falls Du es selbst warst, kannst du diese Mail ignorieren.
            </p>
            
            <p>Falls Du das Gefühl haben solltest, eine fremde Person ist im Besitz deiner Zugangsdaten, solltest du diese unter
        den Kontoeinstellungen sofort ändern: <a href="https://blogbar.eu/de/login"> Hier anmelden </a></p>
            
            <p>Du kannst dich bei Fragen zur weiteren Vorgehensweise gerne bei unserem Support-Team melden.<br><br>
            Dein Team von BlogBar!</p>
          </body>
          {footer}
        </html>
        """.format(first_name=influencer["first_name"], footer=footer)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.ionos.de", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, influencer["email"], message.as_string()
            )
    except:
        pass


def send_goodbye_message(mail, first_name, language: str):
    sender_email = "noreply@blogbar.eu"
    password = "BlogBar2103#"

    message = MIMEMultipart("alternative")
    message[
        "Subject"] = "Auf Wiedersehen: Deine Abmeldung war erfolgreich." if language == "de" else "Goodbye: Your Profile-Deletion-Request was successful"
    message["From"] = sender_email
    message["To"] = mail

    if language == 'de':
        text = """\
               Hi {first_name},

               du hast dich erfolgreich abgemeldet.
               Deine personenbezogenen Daten wurden vollständig und dauerhaft gelöscht.

               Schade, dass du gehst!

               hat dir ein Feature gefehlt? Teil uns gerne den Grund, der deine Abmeldung begründet hat mit: cheers@blogbar.eu

               Dein BlogBar-Team""".format(first_name=first_name)
        html = """\
               <html>
                 <body style="font-family: Calibri;">
                   Hi {first_name},<br><br>
                   <p>du hast dich erfolgreich abgemeldet.</p>
                   <p>Deine personenbezogenen Daten wurden <strong>vollständig und dauerhaft</strong> gelöscht.</p>

                   <p>Schade, dass du gehst!<br>

                   Hat dir ein Feature gefehlt? Teil uns gerne den Grund, der deine Abmeldung begründet hat mit: <a href="mailto:cheers@blogbar.eu">cheers@blogbar.eu</a></p>
                    <br>
                    Dein Team von BlogBar!
                 </body>
                 {footer}
               </html>
               """.format(first_name=first_name, footer=footer)
    else:
        print(language)
        text = """\
            Hello  {first_name},
            
            So sad that you want to unsubscribe from BlogBar. Of course we will comply with your request and confirm your unsubscription.
            Your data will be completely deleted immediately.
            
            We thank you for your trust and wish a lot of success in the future!
            
            Your team from BlogBar""".format(first_name=first_name)

        html = """\
            <html>
              <body style="font-family: Calibri;">
                Hello {first_name},<br><br>
            
                <p>So sad that you want to unsubscribe from BlogBar. Of course we will comply with your request and confirm your unsubscription.</p>
                <p>Your data will be completely deleted immediately.</p>
                
                <p>We thank you for your trust and wish a lot of success in the future!</p>
                <br>
                Your team from BlogBar!
              </body>
              {footer}
            </html>
            """.format(first_name=first_name, footer=footer)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.ionos.de", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, mail, message.as_string()
            )
    except:
        pass


def send_booked_package_confirmation_mail(company_name, contact_person, contact_email, booked_package, expire_date,
                                          token, booked_date, booked_package_duration_in_month,
                                          booked_package_total_amount,
                                          language_abbr: str):
    sender_email = "noreply@blogbar.eu"
    password = "BlogBar2103#"

    message = MIMEMultipart("alternative")
    if language_abbr == "de":
        message[
            "Subject"] = "Buchungsbestätigung: Die Buchung deines {months}-Monats-{level}-Premiumpaketes war erfolgreich".format(
            months=booked_package_duration_in_month,
            level=str(booked_package).upper()
        )
    else:
        message[
            "Subject"] = "Booking-Confirmation: The Booking of your {months}-Months-{level}-premium-package was successful".format(
            months=booked_package_duration_in_month,
            level=str(booked_package).upper()
        )
    message["From"] = sender_email
    message["To"] = contact_email
    # message['Cc'] = "cheers@blogbar.eu"

    if language_abbr == 'de':
        text = """\
                Hallo {contact_person},
    
                die Buchung Ihres {level}-Paketes war erfolgreich und wird dir für die nächsten {months} Monate
                erweiterte Funktionen ermöglichen.
                
                Dein Paket wird voraussichtlich am {expiration_date} auslaufen. Das Premiumpaket kann nach Ablaufen erneut 
                gebucht werden.
                
                Eine Rechnung kann unter folgendem Link heruntergeladen werden: 
                
                https://blogbar.eu/invoice/{token}
    
                Ihr BlogBar-Team""".format(contact_person=contact_person,
                                           level=str(booked_package).upper(),
                                           months=int(booked_package_duration_in_month),
                                           expiration_date=expire_date,
                                           token=token)
        html = """\
                <html>
                  <body style="font-family: Calibri;">
                    <p>Hallo {contact_person},</p>
    
                    <p>die Buchung Ihres {level}-Paketes war erfolgreich und wird dir für die nächsten {months} Monate
                    erweiterte Funktionen ermöglichen.</p>
                    
                    <p>Dein Paket wird voraussichtlich am {expiration_date} auslaufen. Das Premiumpaket kann nach Ablaufen erneut 
                    gebucht werden.<p>
                    
                    <p>Eine Rechnung kann unter folgendem Link heruntergeladen werden: <br>
                    <a href="https://blogbar.eu/invoice/{token}"> Rechnung hier herunterladen</a></p>
        
                    <p>Ihr BlogBar-Team</p>
                  </body>
                  {footer}
                </html>
                """.format(contact_person=contact_person,
                           level=str(booked_package).upper(),
                           months=int(booked_package_duration_in_month),
                           expiration_date=expire_date,
                           token=token, footer=footer)
    else:
        text = """\
                Hello {contact_person},

                Thank you for booking our premium package!
                You can download the invoice using this link:
                https://blogbar.eu/invoice/{token}

                Your package is activated. You can start directly.
                Click here for the login: https://blogbar.eu/en/login
                
                We wish you much success!

                If you have any questions, please do not hesitate to contact us.

                Your team from BlogBar""".format(contact_person=contact_person,
                                                 level=str(booked_package).upper(),
                                                 months=int(booked_package_duration_in_month),
                                                 expiration_date=expire_date,
                                                 token=token)
        html = """\
                <html>
                  <body style="font-family: Calibri;">
                    <p>Hello {contact_person},</p>

                    <p>Thank you for booking our premium package!</p>
                    
                    <p>You can download the invoice using this link:<br>
                    <a href="https://blogbar.eu/invoice/{token}"> Rechnung hier herunterladen</a></p>

                    <p>Your package is activated. You can start directly.<p>
                    <p> Click <a href="https://blogbar.eu/en/login">here</a> for the login.</p>

                    <p>We wish you much success!<br>
                    If you have any questions, please do not hesitate to contact us.
                    </p>

                    <p>Your team from BlogBar</p>
                  </body>
                  {footer}
                </html>
                """.format(contact_person=contact_person,
                           level=str(booked_package).upper(),
                           months=int(booked_package_duration_in_month),
                           expiration_date=expire_date,
                           token=token, footer=footer)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.ionos.de", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, contact_email, message.as_string()
            )
    except:
        # Log this in a logging script
        print("ERROR OCCURED BY SENDING MAIL")
