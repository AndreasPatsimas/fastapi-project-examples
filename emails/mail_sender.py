import smtplib

smtp_obj = smtplib.SMTP(host="smtp.gmail.com", port=587)
smtp_obj.ehlo()  # creates the server
smtp_obj.starttls()

email = "andreas.patsim3@gmail.com"
password = "****"
smtp_obj.login(email, password)

from_address = email
to_address = "sotirinio@hotmail.com"
subject = "tzogos"
message = "refarisma"
msg = "Subject: " + subject + '/n' + message

smtp_obj.sendmail(from_address, to_address, msg)