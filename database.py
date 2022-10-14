import sqlite3
from utils.dispatcher import database_path

conn = sqlite3.connect(database_path)
cur = conn.cursor()

async def create_default_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INT, chat_id INT)""")
    conn.commit()

async def create_bot_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS bot(user_id INT, nick TEXT, balance INT, skin_color TEXT, chats TEXT)""")
    conn.commit()

async def select_user_in_bot_db(user_id):
    user_in_table = cur.execute(f"SELECT user_id FROM bot WHERE user_id=?", (user_id, ))
    user_in_table = user_in_table.fetchone()
    return user_in_table

async def insert_into_bot_db(user_id, nick, skin_color, chat_id):
    balance = 0
    cur.execute("INSERT INTO bot VALUES (?, ?, ?, ?, ?)", (user_id, nick, balance, skin_color, chat_id))
    conn.commit()

async def update_balance_bot(user_id, balance):
    cur.execute("UPDATE bot SET balance=? WHERE user_id=?", (balance, user_id))
    conn.commit()

async def update_nickname_bot_db(user_id, nick):
    cur.execute("UPDATE bot SET nick=? WHERE user_id=?", (nick, user_id))
    conn.commit()

async def update_skin_color_bot_db(user_id, skin_color):
    cur.execute("UPDATE bot SET skin_color=? WHERE user_id=?", (skin_color, user_id))
    conn.commit()

async def return_user_from_bot_db(user_id):
    returned_user = cur.execute(f"SELECT * FROM bot WHERE user_id=?", (user_id, ))
    returned_user = returned_user.fetchall()
    return returned_user

async def create_reputation_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS reputation (user_id INT, chat_id INT, rep INT, unrep INT)""")
    conn.commit()

async def check_user_in_rep(user_id, chat_id):
    returnedd_user = cur.execute("SELECT user_id FROM reputation WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    returnedd_user = returnedd_user.fetchone()
    return returnedd_user

async def select_reputation(user_id, chat_id):
    returned_user = cur.execute("SELECT * FROM reputation WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    returned_user = returned_user.fetchall()
    return returned_user

async def insert_reputation_table(user_id, chat_id, rep, unrep):
    cur.execute("INSERT INTO reputation VALUES (?, ?, ?, ?)", (user_id, chat_id, rep, unrep))
    conn.commit()

async def update_reputation_table(user_id, chat_id, rep, unrep):
    cur.execute("UPDATE reputation SET rep=?, unrep=? WHERE user_id=? AND chat_id=?", (rep, unrep, user_id, chat_id))
    conn.commit()

async def create_last_time_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS last_rep (user_id INT, chat_id INT, last_time TEXT)""")
    conn.commit()

async def select_last_time(user_id, chat_id):
    before = cur.execute("SELECT last_time FROM last_rep WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    before = before.fetchone()
    return before

async def insert_into_last_time(user_id, chat_id, last_time):
    cur.execute("INSERT INTO last_rep VALUES (?, ?, ?)", (user_id, chat_id, last_time))
    conn.commit()

async def update_last_time(user_id, chat_id, last_time):
    cur.execute("UPDATE last_rep SET last_time=? WHERE user_id=? AND chat_id=?", (last_time, user_id, chat_id))
    conn.commit()

async def create_skins_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS skins (skin_name TEXT, skin_id TEXT)""")
    conn.commit()

async def select_skin(skin_id):
    returned_skin = cur.execute("SELECT skin_name FROM skins WHERE skin_id=?", (skin_id, ))
    returned_skin = returned_skin.fetchone()
    return returned_skin

async def create_inventory_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS inventory (user_id INT, skins TEXT)""")
    conn.commit()

async def select_inventory_user(user_id):
    returned_inventory = cur.execute("SELECT skins FROM inventory WHERE user_id=?", (user_id, ))
    returned_inventory = returned_inventory.fetchone()
    return returned_inventory

async def insert_into_inventory(user_id, skins):
    cur.execute("INSERT INTO inventory VALUES (?, ?)", (user_id, skins))
    conn.commit()

async def update_inventory(user_id, skins):
    cur.execute("UPDATE inventory SET skins=? WHERE user_id=?", (skins, user_id))
    conn.commit()

async def create_promo_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS promocodes (promo TEXT, type TEXT, gift_id TEXT, uses INT)""")
    conn.commit()

async def select_promo_user(promo):
    returned_promo = cur.execute("SELECT gift_id FROM promocodes WHERE promo=?", (promo, ))
    returned_promo = returned_promo.fetchone()
    return returned_promo

async def select_all_promo(promo):
    returned_all = cur.execute("SELECT * FROM promocodes WHERE promo=?", (promo, ))
    returned_all = returned_all.fetchall()
    return returned_all

async def update_promo(promo, uses):
    cur.execute("UPDATE promocodes SET uses=? WHERE promo=?", (uses, promo))
    conn.commit()

async def create_jobs_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS jobs (user_id INT UNIQUE, job TEXT, job_name TEXT)""")
    conn.commit()

async def create_welder_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS welder_job (user_id INT UNIQUE, uses INT)""")
    conn.commit()

async def create_taxi_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS taxi_job (user_id INT UNIQUE, uses INT)""")
    conn.commit()

async def select_user_from_jobs(user_id):
    returned_user = cur.execute("SELECT job FROM jobs WHERE user_id=?", (user_id, ))
    returned_user = returned_user.fetchone()
    return returned_user

async def select_name_from_jobs(user_id):
    returned_name_job = cur.execute("SELECT job_name FROM jobs WHERE user_id=?", (user_id, ))
    returned_name_job = returned_name_job.fetchone()
    return returned_name_job

async def select_welder_user(user_id):
    welder_user = cur.execute("SELECT user_id FROM welder_job WHERE user_id=?", (user_id, ))
    welder_user = welder_user.fetchone()
    return welder_user

async def replace_into_jobs(user_id, job, job_name):
    cur.execute("REPLACE INTO jobs VALUES (?, ?, ?)", (user_id, job, job_name))
    conn.commit()

async def replace_into_welder(user_id, uses):
    cur.execute("REPLACE INTO welder_job VALUES (?, ?)", (user_id, uses))
    conn.commit()

async def replace_into_taxi(user_id, uses):
    cur.execute("REPLACE INTO taxi_job VALUES (?, ?)", (user_id, uses))
    conn.commit()

async def select_welder_uses(user_id):
    welder_uses = cur.execute("SELECT uses FROM welder_job WHERE user_id=?", (user_id, ))
    welder_uses = welder_uses.fetchone()
    return welder_uses

async def create_warning_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS time_ban (user_id INT UNIQUE, bool BOOL)""")
    conn.commit()

async def select_warning_table(user_id):
    returned_warning = cur.execute("SELECT bool FROM time_ban WHERE user_id=?", (user_id, ))
    returned_warning = returned_warning.fetchone()

    try:
        returned_warning = returned_warning[0]
        return returned_warning

    except:
        return True

async def replace_warning(user_id, sost):
    cur.execute("REPLACE INTO time_ban VALUES (?, ?)", (user_id, sost))
    conn.commit()

async def select_taxi_user(user_id):
    taxi_user = cur.execute("SELECT user_id FROM taxi_job WHERE user_id=?", (user_id, ))
    taxi_user = taxi_user.fetchone()
    return taxi_user

async def select_taxi_uses(user_id):
    taxi_uses = cur.execute("SELECT uses FROM taxi_job WHERE user_id=?", (user_id, ))
    taxi_uses = taxi_uses.fetchone()
    return taxi_uses

async def delete_user_from_jobs(user_id):
    cur.execute("DELETE from jobs WHERE user_id=?", (user_id, ))
    conn.commit()
