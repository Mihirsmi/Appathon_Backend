from __init__ import *

def sendEmail(token,email):
    message ='Howdy citizens of Bits_Please!\nI am glad that you signed up for Bits_Please\nNow click on the link below and get yourself registered!\n'
    link = 'http://appathon2016.herokuapp.com/api/verifyEmail?token='+token+'\n'
    message += link
    message += 'Have a good day!\n'
    return requests.post(
    "https://api.mailgun.net/v3/sandboxab643396059243a895ca2ea5aba4688e.mailgun.org/messages",
    auth = ("api", "key-845ca68ca5b1dbab046af2929c501abc"),
    data = {
        "from":"Admin User admin@sandboxab643396059243a895ca2ea5aba4688e.mailgun.org",
        "to": email,
        "subject": "Email Verification for Bits_Please",
        "text": message
        }
    )
