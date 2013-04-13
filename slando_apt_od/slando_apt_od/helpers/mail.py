import smtplib
from email.mime.text import MIMEText

addressFrom = 'gagaga1024@gmail.com'
username = 'gagaga1024'
password = 'Z$d86~#$br=T;[.Y4@{X'


def SendMail(to, subject, text):

    message = MIMEText(messageText, 'html')
    message['Subject'] = subject
    message['From'] = addressFrom
    message['To'] = to

    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.ehlo()
    server.login(username, password)
    server.sendmail(addressFrom, addressTo, message.as_string())
    server.quit()


if __name__ == '__main__':
    addressTo = 'loafshock@gmail.com'
    subject = 'Mailer test'
    messageText = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
    "http://www.w3.org/TR/html4/strict.dtd">
    <HTML>
        <HEAD>
            <TITLE>My first HTML document</TITLE>
        </HEAD>
        <BODY>
            <P>Hello world!</P>
        </BODY>
    </HTML>
    """
    SendMail(addressTo, subject, messageText)
