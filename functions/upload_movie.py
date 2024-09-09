import requests
from config import db_name
from DATA_BASE.database import database_movie
db = database_movie(db_name)
async def upload(file_id,key,des = None,):
    db.add_new_movie(file_id=file_id,key=key,des=des)
