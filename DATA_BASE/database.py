import sqlite3


# ----------------------------------------------- database for users-------------------------------------------------------------------------------#
class database_user:
    def __init__(self, DB_NAME):
        self.connection = sqlite3.connect(DB_NAME)
        self.cursor = self.connection.cursor()

    def add_new_user(self, tg_id, l_name, f_name, username):
        self.cursor.execute(f"INSERT INTO users (first_name,last_name,tg_id,username)"
                            f"VALUES (?,?,?,?);", (f_name, l_name, tg_id, username))
        self.connection.commit()

    def get_user(self, tg_id):
        user = self.cursor.execute(f"SELECT * FROM users WHERE tg_id={tg_id};")
        return user.fetchone()

    def update_admin(self, tg_id, new_admin_id):
        self.cursor.execute(f"UPDATE users SET admin_id=?"
                            f"Where tg_id=?;", (new_admin_id, tg_id))
        self.connection.commit()

    def get_all(self):
        user = self.cursor.execute(f"SELECT id FROM users;")
        return user.fetchall()

    def get_all_admins(self):  # new
        admins = self.cursor.execute(f"SELECT * FROM users WHERE admin_id != 0;")
        return admins.fetchall()

    def get_user_id(self):
        user_id = self.cursor.execute(f"SELECT tg_id FROM users;")
        return user_id.fetchall()

    def get_all_user(self):
        users = self.cursor.execute(f"SELECT * FROM users;")
        return users.fetchall()

    def __dell__(self):
        self.cursor.close()
        self.connection.close()


# ------------------------------------------------------ database for movies--------------------------------------------------------------------#


class database_movie:
    def __init__(self, DB_NAME):
        self.connection = sqlite3.connect(DB_NAME)
        self.cursor = self.connection.cursor()

    def add_new_movie(self, file_id, key, des=None):
        self.cursor.execute(f"INSERT INTO movies (file_id,about,key)"
                            f"VALUES (?,?,?);", (file_id, des, key))
        self.connection.commit()

    def get_movie(self, key):
        user = self.cursor.execute(f"SELECT * FROM movies WHERE key={key};")
        return user.fetchone()

    def key_s(self):
        keys = self.cursor.execute(f"SELECT key FROM movies;")
        return keys.fetchall()

    def get_janr(self, text):
        janr = self.cursor.execute(f"SELECT key FROM movies WHERE about LIKE '%{text}%'")
        return janr.fetchall()

    def get_movies(self, text):
        movies = self.cursor.execute(f"SELECT * FROM movies WHERE title LIKE '%{text}%'")
        return movies.fetchall()

    def get_movies_list(self):
        movies = self.cursor.execute(f"SELECT * FROM movies;")
        return movies.fetchall()

    def delete_movie(self, key):
        movie = self.cursor.execute(f"DELETE FROM movies WHERE key={key};")
        return movie.connection.commit()

    def __dell__(self):
        self.cursor.close()
        self.connection.close()


# -------------------------------------------------- database for channels--------------------------------#


class database_channel:
    def __init__(self, DB_NAME):
        self.connection = sqlite3.connect(DB_NAME)
        self.cursor = self.connection.cursor()

    def add_channel(self, channel_id, url, name):
        self.cursor.execute(f"INSERT INTO sub_channel(channel_id, url, name) VALUES (?,?, ?);", (channel_id, url, name))
        self.connection.commit()

    def all_channel(self):
        channels = self.cursor.execute(f"SELECT * FROM sub_channel;")
        return channels.fetchall()

    def del_channel(self, channel_id):
        self.cursor.execute(f"DELETE FROM sub_channel WHERE channel_id = {channel_id}")
        self.connection.commit()

    def get_channel(self, channel_id):
        channels = self.cursor.execute(f"SELECT * FROM sub_channel WHERE channel_id = {channel_id};")
        return channels.fetchone()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
