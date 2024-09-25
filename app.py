from flask import Flask, render_template, request, jsonify, make_response
from io import StringIO
import sqlite3
import csv
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)


conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        text TEXT NOT NULL,
        date DATE NOT NULL
    )
''')

conn.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        format = request.form['format']

        # Получение данных из базы данных
        cursor.execute('''
            SELECT title, text, date
            FROM posts
            WHERE date BETWEEN ? AND ?
        ''', (start_date, end_date))
        data = cursor.fetchall()

        # Преобразование данных в выбранный формат
        if format == 'csv':
            response = make_response(generate_csv(data))
            response.headers["Content-Disposition"] = "attachment; filename=data.csv"
            response.headers["Content-Type"] = "text/csv"
        elif format == 'json':
            response = jsonify(data)
            response.headers["Content-Type"] = "application/json"
        elif format == 'xml':
            response = make_response(generate_xml(data))
            response.headers["Content-Disposition"] = "attachment; filename=data.xml"
            response.headers["Content-Type"] = "text/xml"
        else:
            response = "Неверный формат"
        return response
    else:
        return render_template('index.html')


def generate_csv(data):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['title', 'text', 'date'])
    for row in data:
        writer.writerow(row)
    return output.getvalue()


def generate_xml(data):
    root = ET.Element('data')
    for row in data:
        post = ET.SubElement(root, 'post')
        ET.SubElement(post, 'title').text = row[0]
        ET.SubElement(post, 'text').text = row[1]
        ET.SubElement(post, 'date').text = row[2]
    return ET.tostring(root, encoding='utf-8')


if __name__ == '__main__':
    app.run(debug=True)
