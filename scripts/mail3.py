import smtplib

gmail_user = 'quentin.chambefortgmail.com'
gmail_password = 'R0g3r666!'

sent_from = gmail_user
to = ['quentin.chambefort@gmail.com', 'quentin.chambefort@gmail.com']
subject = 'OMG Super Important Message'
body = 'teeeest'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print 'Email sent!'
except Exception as e:
    print 'Something went wrong...'
    print(e)
