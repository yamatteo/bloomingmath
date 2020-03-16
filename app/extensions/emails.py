# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
# from os import getenv
#
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
#
# SENDGRID_API_KEY = getenv("SENDGRID_API_KEY", "")
# print("SENDGRID KEY:", SENDGRID_API_KEY)
# message = Mail(
#     from_email='from_email@example.com',
#     to_emails='bloomingmath@zoho.com',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')
# try:
#     sg = SendGridAPIClient(SENDGRID_API_KEY)
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e.message)


# def send_password_reset_email(token: str = "", to_email: str = ""):
#     message = Mail(
#         from_email="bloomingmath@zoho.com",
#         to_emails=to_email,
#         subject="Bloomingmath password reset",
#         html_content="<p>Gentile utente, è stata richiesta una nuova password per il profilo collegato a questo \
#         indirizzo email. Se non hai richiesto la nuova password o se non hai nemmeno un profilo su Bloomingmath: ci \
#         scusiamo per il disagio, cancella questa mail e dimenticati di noi. Se vuoi impostare la nuova password, segui \
#         il link <a href='https://bloomingmath.herokuapp.com/users/password_reset/{token}'>\
#         https://bloomingmath.herokuapp.com/users/password_reset/{token}</a>.</p><p>A presto.</p>"
#     )
#     print(message)
#     try:
#         sg = SendGridAPIClient(SENDGRID_API_KEY)
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print(e.message)

def send_password_reset_email(token: str, to_email: str):
    import smtplib
    import ssl
    from email.message import EmailMessage

    msg = EmailMessage()
    msg.set_content(f"""\
Buongiorno Eternauta.

È arrivata al nostro server una richiesta per reimpostare la tua password. Per poterlo fare con la certezza che \
l'autore della richiesta sia proprio tu, per favore copia e incolla il codice seguente nella richiesta.

{token}

Se non hai richiesto di reimpostare la password o se non hai un profilo in Bloomingmath, cancella e dimentica \
questa mail.

Cordiali saluti.""")
    msg['Subject'] = f'Richiesta di reimpostare la password'
    msg['From'] = "bloomingmath@zoho.com"
    msg['To'] = to_email

    port = 465  # For SSL
    password = "hangetsu87"

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.zoho.com", port, context=context) as server:
        server.login("bloomingmath@zoho.com", password)
        server.send_message(msg)
