import datetime as dt
import smtplib
import random
import pandas
import messagebox

# TODO 1: Update the birthdays.csv
# TODO 2: Check if today matches a birthday in the birthdays.csv
# TODO 3: If step 2 is true, pick a random letter and replace [NAME] with the person's actual name from birthdays.csv
# TODO 4: Send the letter generated in step 3 to that person's email address.

PLACEHOLDER = "[NAME]"

today = dt.datetime.now()
data = pandas.read_csv("birthdays.csv").to_dict(orient="records")

sender = "some@some.com"
password = "yourpassword"  # app password specifically

for person in data:
    # find out if today's day and month correspond to someone's birthdate (#TODO2)
    if person["day"] == today.day and person["month"] == today.month:
        receiver = person["email"]

        messagebox.showinfo(title="Found Someone",
                            message=f"Found: {person['name']} - Birthday: {today.date()}")

        is_yes = messagebox.askyesno(title="Wish Happy Birthday",
                                     message=f"Would you like to wish Happy Birthday to {person['name']}'s email:\n"
                                             f"{receiver}?")

        if is_yes:  # if user click on yes -> continue to sending email to wish birthday
            # read and replace the placeholder name from a randomized letter
            with open(f"letter_{random.randint(1, 3)}.txt") as letter:
                letter_content = letter.read()  # read the content of the letter
                new_letter = letter_content.replace(PLACEHOLDER, person['name'])

            # connect, login to yahoo account and send the email
            try:
                with smtplib.SMTP("smtp.mail.yahoo.com", 587) as connection:  # access yahoo mail server with port 587
                    connection.starttls()  # make connection secure and encrypt all email
                    connection.login(user=sender, password=password)
                    connection.sendmail(
                        from_addr=sender,
                        to_addrs=receiver,
                        msg=f"Subject:Happy {person['name']}'s {today.year - person['year']} Birthday\n\n"
                            f"{new_letter}"
                    )
                    # show a pop-up to indicate that sending was successful
                    messagebox.showinfo(title="Sent Success",
                                        message=f"Your email has been sent successfully to: {receiver}")
            except TimeoutError:  # if the email server blocked this or somehow takes too long to answer
                messagebox.showwarning(title="SEND UNSUCCESSFUL",
                                       message=f"Your email was NOT sent successfully to: {receiver}")