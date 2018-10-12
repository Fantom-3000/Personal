import sqlite3 as lite
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem
import sys
from functools import partial

def read_users_data(sql):
    conn = lite.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    users_data = cursor.fetchall()
    cursor.close()
    return users_data

# Обработка нажатия кнопки "Отправить"
def enter_button_clk(table, users_list_box, stations_list_box, persons_list_box, schedule_list_box):
    user = users_list_box.currentText()
    station = stations_list_box.currentText()
    person = person_list_box.currentText()
    schedule = schedule_list_box.currentText()
    station_id = station_list.index(station) + 1 # Индекс станции
    person_id = person_index(person)
    schedule_id = schedule_list.index(schedule) * 2 + 1 # Индекс ячейки графика + в качестве n лица
    table.setItem(schedule_id + person_id, station_id, QTableWidgetItem(user))

def person_index(person):
    if person == 'Первого':
        person_id = 0
    elif person == 'Второго':
        person_id = 1
    return person_id

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    sql_users = '''SELECT * FROM users'''
    sql_stations = '''SELECT * FROM stations'''
    sql_persons = '''SELECT * FROM persons'''
    sql_schedule = '''SELECT * FROM schedules'''

    window = QtWidgets.QWidget()
    window.resize(1000, 400)

    box = QtWidgets.QVBoxLayout(window)
    h_box_1 = QtWidgets.QHBoxLayout()
    h_box_2 = QtWidgets.QHBoxLayout()

    table = QtWidgets.QTableWidget()
    table.setColumnCount(7)
    table.setRowCount(9)
    table.setFixedSize(750, 300)
    table.horizontalHeader().hide()
    table.verticalHeader().hide()

    users_list_box = QtWidgets.QComboBox()
    stations_list_box = QtWidgets.QComboBox()
    person_list_box = QtWidgets.QComboBox()
    schedule_list_box = QtWidgets.QComboBox()
    enter_button = QtWidgets.QPushButton('Отправить')

    users_login_list = QtWidgets.QListWidget()
    users_login_list.setFixedSize(200, 300)

    # Звполнение строк названиями станций из базы данных
    data = read_users_data(sql_stations)
    station_list = []
    for station_data in data:
        station_list.append(station_data[1])    
    stations_list_box.addItems(station_list)

    # Звполнение строк номерами графиков из базы данных
    data = read_users_data(sql_schedule)
    schedule_list = []
    for schedule_data in data:
        schedule_list.append(schedule_data[1])
    schedule_list_box.addItems(schedule_list)    

    # Заполнение строк фамилиями и инициалами из базы данных
    if users_list_box.currentIndexChanged != -1:
        data = read_users_data(sql_users)
        for user_data in data:
            users_list_box.addItem(user_data[1])

    # Звполнение строк в качестве лица из базы данных
    if person_list_box.currentIndexChanged != -1:
        data = read_users_data(sql_persons)
        for person_data in data:
            person_list_box.addItem(person_data[1])

    # Внесение в таблицу наименований столбцов и строк
    for col in range(1, 9, 2): # Столбцы - наименования станций
        table.setSpan(col, 0, 2, 1)
        table.setItem(col, 0, QTableWidgetItem(schedule_list[(col)//2]))

    for row in range(1, 7): # Строки - наименования графиков
        table.setItem(0, row, QTableWidgetItem(station_list[row-1]))    

    h_box_1.addWidget(users_login_list, QtCore.Qt.AlignLeft)
    h_box_1.addWidget(table, QtCore.Qt.AlignLeft)
    h_box_2.addWidget(users_list_box)
    h_box_2.addWidget(stations_list_box)
    h_box_2.addWidget(schedule_list_box)
    h_box_2.addWidget(person_list_box)
    h_box_2.addWidget(enter_button)

    box.addLayout(h_box_1)
    box.addLayout(h_box_2)

    # Обработчик кнопки "Отправить"
    enter_button.clicked.connect(partial(enter_button_clk, table, users_list_box, 
        stations_list_box, person_list_box, schedule_list_box))

    window.show()
    sys.exit(app.exec_())
