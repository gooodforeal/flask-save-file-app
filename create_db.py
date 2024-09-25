from flask import Flask, render_template, request, jsonify, make_response
from io import StringIO
import sqlite3
import csv
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Соединение с базой данных
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Создание таблицы (если ее еще нет)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        text TEXT NOT NULL,
        date DATE NOT NULL
    )
''')
cursor.execute('''
            INSERT INTO posts (title, text, date) VALUES ("new1", "new1-text", "2023-05-24")
        ''')
cursor.execute('''
            INSERT INTO posts (title, text, date) VALUES ("new2", "new2-text", "2023-01-13")
        ''')
cursor.execute('''
            INSERT INTO posts (title, text, date) VALUES ("new3", "new3-text", "2022-01-01")
        ''')
cursor.execute('''
            INSERT INTO posts (title, text, date) VALUES ("new4", "new4-text", "2021-12-12")
        ''')
cursor.execute('''
            INSERT INTO posts (title, text, date) VALUES ("new5", "new5-text", "2024-03-03")
        ''')
cursor.execute('''
            INSERT INTO posts (title, text, date) VALUES ("new6", "new6-text", "2024-06-06")
        ''')
cursor.execute('''
            INSERT INTO posts (title, text, date) VALUES ("new7", "new7-text", "2024-07-07")
        ''')
cursor.execute('''
            INSERT INTO posts (title, text, date) VALUES ("new8", "new8-text", "2023-09-09")
        ''')

conn.commit()