import random
import smtplib
from array import array
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime, timedelta
from time import sleep

import re

import pycurl
from io import BytesIO

crl = pycurl.Curl()
b_obj = BytesIO()
crl.setopt(crl.URL, 'https://www.mein-laborergebnis.de/ergebnis/b3476a18-df20-41bf-b69a-c24d36b1c245')

crl.setopt(crl.WRITEDATA, b_obj)

crl.perform()

crl.close()

get_body = b_obj.getvalue()

text = get_body.decode('utf8')

x = re.findall("<div class=\"display-4 mb-4 ErgebnisText\">\n\s*(.*)\n.*</div>", text)

print(x[0])
