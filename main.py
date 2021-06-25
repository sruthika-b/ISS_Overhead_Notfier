import requests
import smtplib
import time
from datetime import datetime
MY_LATITUDE = 12.922915
MY_LONGITUDE = 80.127457
my_email = "sample email"
password = "*********"
parameters = {
    "lat": MY_LATITUDE,
    "lng": MY_LONGITUDE,
    "formatted" : 0
}

def over_head():
    location_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    location_response.raise_for_status()
    loc_data = location_response.json()

    iss_latitude = float(loc_data["iss_position"]["latitude"])
    iss_longitude = float(loc_data["iss_position"]["longitude"])

    region = False
    #The ISS's location can be +5 or -5 degrees from your position
    if 7 <= iss_latitude <= 17 and 75 <= iss_longitude <= 85:
        return True
    return False

def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split('T')[1].split(':')[0])
    sunset = int(data["results"]["sunset"].split('T')[1].split(':')[0])

    time_now = datetime.now().hour

    if sunset <= time_now or time_now <= sunrise:
        return True
    return False

# If the ISS is close to my current position and it's currently dark,
# then send an email to notify me to took up

while True:
    if over_head() and is_night():
        # Initiate email
        conn = smtplib.SMTP("smtp.gmail.com")
        conn.starttls()
        conn.login(my_email,password)
        conn.sendmail(from_addr=my_email,
                  to_addrs="sruthikab003@gmail.com",
                  msg="Look Up for an ISS\n\nLook for an ISS in the sky right now")
    time.sleep(60)