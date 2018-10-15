import sqlite3 as lite
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem
import sys
from functools import partial

def read_data(sql):
    conn = lite.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    users_data = cursor.fetchall()
    cursor.close()
    return users_data

# Обработка нажатия кнопки "Отправить"
def enter_button_clk(table_login_model, users_list_box, stations_list_box, persons_list_box, schedule_list_box, logins):
    user = users_list_box.currentText()
    # user = logins.data(QtGui.QStandardItem.text(1)) # Не работает
    station = stations_list_box.currentText()
    person = person_list_box.currentText()
    schedule = schedule_list_box.currentText()
    station_id = station_list.index(station) + 1 # Индекс станции
    person_id = person_list.index(person)
    schedule_id = schedule_list.index(schedule) * 2 + 1 # Индекс ячейки графика + в качестве n лица
    login = table_login_model.data(table_login_model.index(schedule_id + person_id, station_id))
    if not login:
        table_login_model.setItem(schedule_id + person_id, station_id, QtGui.QStandardItem(user))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    sql_users = '''SELECT * FROM users ORDER BY login'''
    sql_stations = '''SELECT * FROM stations'''
    sql_persons = '''SELECT * FROM persons'''
    sql_schedule = '''SELECT * FROM schedules'''

    window = QtWidgets.QWidget()
    window.resize(1000, 400)

    box = QtWidgets.QVBoxLayout(window)
    h_box_1 = QtWidgets.QHBoxLayout()
    h_box_2 = QtWidgets.QHBoxLayout()

    users_list_box = QtWidgets.QComboBox()
    stations_list_box = QtWidgets.QComboBox()
    person_list_box = QtWidgets.QComboBox()
    schedule_list_box = QtWidgets.QComboBox()
    enter_button = QtWidgets.QPushButton('Отправить')
    logins_list_box = QtWidgets.QListView()
    logins_list_box.setFixedSize(150, 300)

    login_table_view = QtWidgets.QTableView()
    table_login_model = QtGui.QStandardItemModel(9, 7)
    login_table_view.setModel(table_login_model)
    login_table_view.setFixedSize(750, 300)
    login_table_view.horizontalHeader().hide()
    login_table_view.verticalHeader().hide()

    # Звполнение строк названиями станций из базы данных
    data = read_data(sql_stations)
    station_list = []
    for station_data in data:
        station_list.append(station_data[1])
    stations = QtCore.QStringListModel(station_list)
    stations_list_box.setModel(stations)
    # stations_list_box.addItems(station_list)

    # Звполнение строк номерами графиков из базы данных
    data = read_data(sql_schedule)
    schedule_list = []
    for schedule_data in data:
        schedule_list.append(schedule_data[1])
    schedule_list_box.addItems(schedule_list)    

    # Заполнение строк фамилиями и инициалами из базы данных
    if users_list_box.currentIndexChanged != -1:
        login_list = []
        data = read_data(sql_users)
        for user_data in data:
            login_list.append(user_data[1])
        logins = QtCore.QStringListModel(login_list)
        logins_list_box.setModel(logins)
        users_list_box.setModel(logins)

    # Звполнение строк в качестве лица из базы данных
    if person_list_box.currentIndexChanged != -1:
        data = read_data(sql_persons)
        person_list = []
        for person_data in data:
            person_list.append(person_data[1])
        person_list_box.addItems(person_list)

    # Внесение в таблицу наименований столбцов и строк
    for col in range(1, 9, 2): # Столбцы - наименования станций
        login_table_view.setSpan(col, 0, 2, 1)
        table_login_model.setItem(col, 0, QtGui.QStandardItem(schedule_list[(col)//2]))

    for row in range(1, 7): # Строки - наименования графиков
        table_login_model.setItem(0, row, QtGui.QStandardItem(station_list[row-1]))

    h_box_1.addWidget(logins_list_box)
    h_box_1.addWidget(login_table_view)

    h_box_2.addWidget(users_list_box)
    h_box_2.addWidget(stations_list_box)
    h_box_2.addWidget(schedule_list_box)
    h_box_2.addWidget(person_list_box)
    h_box_2.addWidget(enter_button)

    box.addLayout(h_box_1)
    box.addLayout(h_box_2)

    # Обработчик нажатия кнопки "Отправить"
    enter_button.clicked.connect(partial(enter_button_clk, table_login_model, users_list_box, 
        stations_list_box, person_list_box, schedule_list_box, logins))

    window.show()
    sys.exit(app.exec_())
