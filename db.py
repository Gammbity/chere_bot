import psycopg2
from psycopg2 import Error

# PostgreSQL ulanish parametrlari
db_name = "Chere"
db_user = "ChereAdmin"
db_password = "Qwerty123$"
db_host = "localhost"
db_port = "5432"

try:
    # PostgreSQL-ga ulanish
    connection = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )

    cursor = connection.cursor()
    print("PostgreSQL-ga muvaffaqiyatli ulandik")

except (Exception, Error) as error:
    print("PostgreSQL-ga ulanishda xatolik:", error)

# Yangi yozuvni qo'shish
cursor.execute("INSERT INTO users (id, name, age) VALUES (%s, %s, %s)", (1, 'John Doe', 30))
connection.commit()

# Ma'lumotlarni o'qish
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Ma'lumotni yangilash 
cursor.execute("UPDATE users SET age = %s WHERE id = %s", (31, 1))
connection.commit()

# Ma'lumotni o'chirish
cursor.execute("DELETE FROM users WHERE id = %s", (1,))
connection.commit()

# Ulanishni yopish
if connection:
    cursor.close()
    connection.close()
    print("PostgreSQL ulanishi yopildi")
