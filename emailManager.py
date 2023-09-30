from redmail import gmail
from datetime import datetime
import pytz
import socket

gmail.username = "bst.einbruchschutz@gmail.com"
gmail.password = "ssnnpngxsrnjdsvi"


def sendGmail_svenVersion(*args, subject):
    gmail.send(
        subject=f"[Event-Server] {get_host_name()} von eAccess-Webclient",
        receivers=["ramzi.d@outlook.com"],
        html=f"""
             <h2>Guten Tag</h2>
             <p> </p>
             <p>Ein Server ist nicht mehr erreichbar! Nachfolgend die Informationen vom Server:</p>
             <p>PC-Name:     {get_host_name()}    </p>
             <p>PC-Adresse: {get_local_ip()} </p>
             <p>Der Server ist hat keine Verbindung seit: </p>
             <p>Datum:      {datum()}  </p>
             <p>Zeit:       {time()}  </p>
             <p>Bitte Verbindung kontrollieren und wiederherstellen.
             <br><h2>BST Einbruchschutz</h2></p>
         """,
    )


def sendGmail_ramziVersion(*args, subject, text_1, text_2=''):
    gmail.send(
        subject=subject,
        receivers=["ramzi.d@outlook.com"],
        html=f"""
             <h2>Guten Tag</h2>
             <p> {args}</p>
             <p><{text_1}/p>
             <p></p>
             <p>{text_2}</p>
             <p></p>
             <p>Datum:      {datum()}  </p>
             <p>Zeit:       {time()}  </p>
             <p>
             <br><h2>BST Einbruchschutz</h2></p>
         """,
    )


def datum():
    current_date = datetime.now()
    swiss_date_format = current_date.strftime("%d.%m.%Y")
    return swiss_date_format


def time():
    zurich_tz = pytz.timezone("Europe/Zurich")

    # Get the current time with the Zurich timezone
    current_time = datetime.now(zurich_tz)

    # Format the time in Swiss format
    swiss_time_format = current_time.strftime("%H:%M:%S")

    # Print the time in Swiss format with Zurich timezone
    return swiss_time_format


def get_local_ip():
    try:
        # Get the hostname of the machine
        hostname = socket.gethostname()

        # Get the IP address associated with the hostname
        local_ip = socket.gethostbyname(hostname)

        return local_ip
    except socket.gaierror as e:
        return f"there is Error: {e} please control ur script"


def get_host_name():
    try:
        # Get the hostname of the machine
        hostname = socket.gethostname()
        return hostname
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"there is Error: {e} please control ur script"
