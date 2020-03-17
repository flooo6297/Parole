import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime, timedelta
from threading import Timer
from time import sleep

from libs import epd2in7b
from PIL import Image, ImageDraw, ImageFont

smtp_url = ""
smtp_port = 0
mail_address = ""
mail_password = ""
debug_level = 0

font_24 = ImageFont.truetype('/opt/Parole/Fonts/Font.ttc', 24)

epd = epd2in7b.EPD()
epd.init()
epd.Clear()


def load_data_from_file(path):
    raw_data = open(path, encoding="ISO-8859-1")
    data_list = [line.rstrip('\n') for line in raw_data]
    return data_list


def get_host_names():
    host_list = load_data_from_file("/etc/Parole/host.txt")
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


def load_config():
    global smtp_url
    global smtp_port
    global mail_address
    global mail_password
    global debug_level
    config_data = load_data_from_file("/etc/Parole/dailyPassword.conf")
    for entry in config_data:
        config_line = filter_comments_from_line(entry)
        if len(config_line) > 0:
            split_config = config_line.split("=")
            if len(split_config) > 1:
                for i in range(1, len(split_config)):
                    if split_config[0] == "smtp_url":
                        smtp_url += split_config[i]
                    if split_config[0] == "smtp_port":
                        smtp_port += int(split_config[i])
                    if split_config[0] == "mail_address":
                        mail_address += split_config[i]
                    if split_config[0] == "mail_password":
                        mail_password += split_config[i]
                    if split_config[0] == "debug_level":
                        debug_level += int(split_config[i])
    return ""


def send_newsletters():
    load_config()
    host = get_host_names()
    current_date_string = get_current_date()
    parole_for_today = get_random_line(load_data_from_file("/etc/Parole/WordDatabase/de_DE_frami.txt"))

    email_addresses = load_data_from_file("/etc/Parole/addresses.txt")

    for entry in email_addresses:
        address = filter_comments_from_line(entry)
        if len(address) > 2:
            send_email(address, parole_for_today, current_date_string, host)
    display_parole_on_screen(parole_for_today)
    sleep(2)
    start_timer(True)


def start_timer(start_now=False):
    x = datetime.today()
    # y = x.replace(day=x.day, hour=0, minute=0, second=1, microsecond=0) + timedelta(days=1)
    # y = x + timedelta(seconds=10)

    y = x.replace(day=x.day, hour=0, minute=0, second=1, microsecond=0)

    if x < y:
        y = x.replace(day=x.day, hour=0, minute=0, second=1, microsecond=0) + timedelta(days=1)

    if start_now:
        y = x + timedelta(seconds=1)

    delta_t = y - x

    secs = delta_t.total_seconds()

    t = Timer(secs, send_newsletters)
    t.start()


def display_parole_on_screen(parole):
    black_image = Image.new('1', (epd.height, epd.width), 255)
    draw_black = ImageDraw.Draw(black_image)
    draw_black.text((2, 0), parole, font=font_24, fill=0)

    red_image = Image.new('1', (epd.height, epd.width), 255)
    draw_red = ImageDraw.Draw(red_image)

    epd.display(epd.getbuffer(black_image), epd.getbuffer(red_image))
    # epd.sleep()


start_timer(True)
