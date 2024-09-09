import requests
from config import db_name
from DATA_BASE.database import database_movie
def send_video(token,chat_id,file_id,name):
    url = f"https://api.telegram.org/bot{token}/sendVideo"
    data = {
        "chat_id": chat_id,
        "video": file_id,
        "caption": name
    }
    response = requests.post(url, json=data)

def get_id(cod):
    db = database_movie(db_name)
    return db.get_movie(cod)

def yes_or_no(token,chat_id,file_id,name,keyboard):
    url = f"https://api.telegram.org/bot{token}/sendVideo"
    data = {
        "chat_id": chat_id,
        "video": file_id,
        "caption": name,
        "reply_markup": keyboard
    }
    response = requests.post(url, json=data)

