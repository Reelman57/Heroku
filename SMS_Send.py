from itertools import count
import pandas as pd
import os
from datetime import datetime, timedelta
from twilio.rest import Client
import time
import pytz
import re
import sys

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
messaging_sid= os.environ['TWILIO_MSGNG_SID']
twilio_number = "+12086034040"
Client = Client(account_sid, auth_token)

sent_texts = set()
x=0
arg1 = sys.argv[1] if len(sys.argv) > 1 else ""
arg2 = sys.argv[2] if len(sys.argv) > 2 else "+15099902828"

with open('DO_NOT_SEND.txt', 'r') as file:
    sent_texts = set(line.strip() for line in file)

def get_send_time():
    timezone = pytz.timezone('America/Los_Angeles')
    now_utc = datetime.now(timezone)
    send_at = now_utc + timedelta(minutes=15)
    return send_at

def send_text(text_nbr, message):
    if text_nbr not in sent_texts and not pd.isna(text_nbr):
        try:
            message = Client.messages.create(
                body=message,
                from_=twilio_number,
                to=text_nbr
            )
            sent_texts.add(text_nbr)  # Add the actual phone number to the set
            return message  # Return the message object
        except Exception as e:
            print(f"Error sending SMS to {text_nbr}: {e}")
            return None  # Return None to indicate failure
    else:
        return None 

def get_message(row):
    message = f"Hello {row['First_Name']},\n"

    if arg1:
        message += arg1 + "\n"
    return message

data_path = "Westmond_Master.csv"

df = pd.read_csv(data_path)
df_filtered = df[(df['Age'] > 17)]
df_sorted = df_filtered.sort_values(by='Last_Name', ascending=True)

for index,row in df_sorted.iterrows():

    print(row["Last_Name"], row["First_Name"], row["Phone Number"])

    if row["Last_Name"] == "Reese" and row["First_Name"] == "Dale":

        subject, message = get_message(row)
        if arg1:
            send_text(row['Phone Number'], message)
       
        x+=1
        time.sleep(.1)

message = Client.messages.create(
body=f'Message sent to {x} individuals.',
from_=twilio_number,
to = arg2
)
