import psycopg2
import os

try:
	conn = psycopg2.connect(os.environ['DATABASE_URL'])
	print "Conectado a la base de datos"
except:
	print "Conexión a la base de datos falló"


# Diccionario de usuario
def result_to_user(row):
	user = {}
	user['id'] = row[0]
	user['chat'] = row[1]
	user['link'] = row[2]
	user['previous_data'] = row[3]

# Devuelve una lista de diccionarios de usuarios
def get_users():
	cur = conn.cursor()
	cur.execute("SELECT * from users")
	rows = cur.fetchall()
	users = []
	for r in rows:
		users.append(result_to_user(r))
	return users


# Devuelve un solo usuario segun id_chat
def get_single_user(id_chat):
	cur = conn.cursor()
	query = "SELECT * from users WHERE chat=%s;"
	cur.execute(query, (str(id_chat),))
	rows = cur.fetchone()
	return result_to_user(r)


# Devuelve un solo usuario segun id_chat
def insert_user(id_chat, grades, link):
	query = "INSERT INTO users(chat,previous_data,link) VALUES (%s, '%s', '%s');"
	cur = conn.cursor()
	cur.execute(query, (str(id_chat), grades, link,))
	conn.commit()


# Borra un usuario segun id_chat
def delete_user(id_chat):
	query = "DELETE FROM users WHERE chat=%s;"
	cur = conn.cursor()
	cur.execute(query, (str(id_chat), ))
	conn.commit()


# Actualiza un usuario segun id_chat
def update_user(id_chat, grades, link):
	query = "UPDATE users SET previous_data='%s', link='%s' WHERE chat=%s;"
	cur = conn.cursor()
	cur.execute(query, (grades, link, str(id_chat), ))
	conn.commit()