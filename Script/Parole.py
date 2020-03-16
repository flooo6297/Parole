import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime, timedelta

smtp_url = ""
smtp_port = 0
mail_address = ""
mail_password = ""
debug_level = 0


def load_data_from_file(path):
    raw_data = open(path, encoding="ISO-8859-1")
    data_list = [line.rstrip('\n') for line in raw_data]
    return data_list


def get_host_names():
    host_list = load_data_from_file("/etc/DailyPassword/host.txt")
    if len(host_list) > 0:
        return host_list[0]
    else:
        return ""


def get_random_line(word_list):
    random_line = word_list[random.randrange(0, len(word_list) - 1)]
    filtered_line = filter_comments_from_line(random_line)
    while len(filtered_line) < 1:
        random_line = word_list[random.randrange(0, len(word_list) - 1)]
        filtered_line = filter_comments_from_line(random_line)
    return filtered_line


def filter_comments_from_line(line):
    to_return = ""
    for c in line:
        if c != "#":
            to_return += c
        else:
            break
    to_return = to_return.strip()
    return to_return


def get_current_date():
    date = datetime.now()
    return str(date.day) + "." + str(date.month) + "." + str(date.year)


def send_email(address, parole, date_string, host):
    msg = MIMEMultipart()
    message = "Dies ist der automatisierte Parolen-Newsletter für die Wohnung von " + host \
              + "<br><br><br> Die heutige Parole lautet: <br><br>" \
              + "<a href= \"https://www.google.com/search?q=" + parole + "\">" + parole + "</a> "
    msg['Subject'] = "Taegliche Parole vom " + date_string
    msg['From'] = mail_address
    msg['To'] = str(address)
    msg.attach(MIMEText(message, 'html'))

    # Send the message via SMTP server.
    s = smtplib.SMTP_SSL(smtp_url, smtp_port)
    s.set_debuglevel(debug_level)
    print(s.login(mail_address, mail_password))
    s.send_message(msg)
    s.quit()
