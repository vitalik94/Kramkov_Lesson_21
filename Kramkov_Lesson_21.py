# ДЗ на четверг (Ivanov_Lesson_21.py)
# 1. Создать таблицу в Базе Данных с тремя колонками(id, 2 - text, 3 - text).
# Заполнить её с помощью INSERT данными (3 записи).
# Удалить с помощью DELETE 2 запись. Обновить значения 3-ей записи на: hello world с помощью UPDATE
# *Записать данные с таблицы в текстовый файл в три колонки. Первая – id, вторая и третья с данными

import sqlite3

conn = sqlite3.connect('notes_data.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS notes(
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    note TEXT,
                                                    record TEXT
                                                    )''')

list_notes = [('ручка', 'карандаш'), ('телефон', 'стелс'), ('подземелье', 'драконы'), ('автомобиль', 'бмв'),
              ('машина', 'стиральная'), ('ягоды', 'груши'), ('магазин', 'базар')]
cursor.executemany('''INSERT INTO notes (note, record) VALUES(?,?)''', list_notes)
conn.commit()
cursor.execute('''SELECT * FROM notes''')
k = cursor.fetchall()
cursor.execute(f'''DELETE FROM notes WHERE id = {k[1][0]}''')
cursor.execute(f'''UPDATE notes SET note = 'hello world', record = 'hello world' WHERE id = {k[2][0]}''')
conn.commit()


with open('records.txt', 'a', encoding='utf-8') as f:
    for i in k:
        f.write(f'{str(i[0]):5}{i[1]:15}{i[2]:25}\n')


with open('records.txt', 'r', encoding='utf-8') as f:
    print(f.read())

# 2. В БД из первого задания удалить первую ПОЛОВИНУ записей, а вторую обновить на любые значения.
# В Ручную удалять нельзя!
# Если строк нечетное количество, то округляем в меньшую сторону!

if len(k) > 1:
    cursor.execute(f'''DELETE FROM notes WHERE id < {k[len(k) // 2][0]}''')
    cursor.execute('''UPDATE notes SET note = 'новые', record = 'записи' ''')
conn.commit()


# 3. Создать 2 таблицы в Базе Данных
# Одна будет хранить текстовые данные(1 колонка)
# Другая числовые(1 колонка)
# Есть список, состоящий из чисел и слов.
#  my_list = [‘Home’, ‘Work’, 29, 9, 2022]
# Если элемент списка слово, записать его в соответствующую таблицу,
# затем посчитать длину слова и записать её в числовую таблицу
# Если элемент списка число: проверить, если число чётное записать его в таблицу чисел, если нечётное,
# то записать во вторую таблицу слово: «нечётное»
# Если число записей во второй таблице больше 5, то удалить первую запись в первой таблице.
# Если меньше, то обновить первую запись в первой таблице на «hello»

cursor.execute('''CREATE TABLE IF NOT EXISTS texts1_data(
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    texts TEXT
                                                    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS nums2_data(
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    nums INTEGER
                                                    )''')

my_list = ['Home', 'Work', 29, 9, 'lesson', 2022, 'text', 10]
# my_list = ['Home', 'Work', 29, 9, 'lesson']

for i in my_list:

    if type(i) == str:
        cursor.execute('''INSERT INTO texts1_data(texts) VALUES(?)''', (i,))
        cursor.execute('''INSERT INTO nums2_data(nums) VALUES(?)''', (len(i),))
    elif type(i) == int:
        if i % 2 == 0:
            cursor.execute('''INSERT INTO nums2_data(nums) VALUES(?)''', (i,))
        else:
            cursor.execute('''INSERT INTO texts1_data(texts) VALUES('нечётное')''')

cursor.execute('''SELECT * FROM nums2_data''')
table_nums2 = cursor.fetchall()
cursor.execute('''SELECT * FROM texts1_data''')
table_texts1 = cursor.fetchall()

if len(table_nums2) >= 5:
    cursor.execute(f'''DELETE FROM texts1_data WHERE id = {table_texts1[0][0]}''')
else:
    cursor.execute(f'''UPDATE texts1_data SET texts = 'hello' WHERE id = {table_texts1[0][0]}''')

conn.commit()
conn.close()
