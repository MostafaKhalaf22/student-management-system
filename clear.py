import sqlite3
conn = sqlite3.connect('students.db')
cursor = conn.cursor()
cursor.execute('DELETE FROM grades')
conn.commit()
print('grades deleted')
conn.close()