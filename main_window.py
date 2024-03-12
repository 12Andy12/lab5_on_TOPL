from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtWidgets, QtGui
import json
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Machine:
    states: []
    alphabet: []
    alphabet_y: []
    rules: [[]]
    state: str
    stack: str
    stack_y: str
    end: []
    alphabet_stack: []


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.setWindowTitle("Легенда ТЯПа")
        self.tableStyle = "QTableWidget{\ngridline-color: #666666}"
        self.headerStyle = "::section:pressed {background-color: #323232;\nborder: none;}\n::section {background-color: #323232;\nborder: none;}"
        self.tableWidget.horizontalHeader().setStyleSheet(self.headerStyle)
        self.tableWidget.setStyleSheet(self.tableStyle)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setColumnCount(5)
        headers = ['', '', '', '', '']
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 60)
        self.tableWidget.setColumnWidth(3, 200)

        self.file = "test.json"

        result = self.input(self.file)
        self.loadTable(result.rules)
        self.btn_check.clicked.connect(lambda: self.check(result))

    def check(self, mashine):
        mashine = self.input(self.file)
        word = self.word.text()
        word = word + "ε"
        chain = word

        for char in word:

            if (char not in mashine.alphabet and char != "ε"):
                self.println(
                    f"char not in mashine.alphabet для ({mashine.state}, {char}, {mashine.stack[0]}) => цепочка не принадлежит языку")
                return

            is_ok = False
            good_rule = []
            number = 0
            super_number = -1
            for rule in mashine.rules:
                number += 1
                if mashine.state == rule[0] and char == rule[1] and mashine.stack[0] == rule[2]:
                    if is_ok == True:
                        self.println(
                            f"Найдено больше одного правила для ({mashine.state}, {char}, {mashine.stack[0]}) => цепочка не принадлежит языку")
                        return
                    good_rule = rule
                    is_ok = True
                    super_number = number

            if is_ok == False:
                self.println(
                    f"Не найдено правило для ({mashine.state}, {char}, {mashine.stack[0]}) => цепочка не принадлежит языку")
                return

            self.println(f"({mashine.state}, {chain}, {mashine.stack}) переход по правилу {super_number} ({good_rule[3]}, {good_rule[4]}, {good_rule[5]}), y = '{mashine.stack_y}'")

            for c in good_rule[4]:
                if (c not in mashine.alphabet_stack and good_rule[4] != 'ε'):
                    self.println(
                        f"{good_rule[4]} not in mashine.alphabet_stack для ({mashine.state}, {char}, {mashine.stack[0]}) => цепочка не принадлежит языку")
                    return

            for c in good_rule[5]:
                if (c not in mashine.alphabet_y and good_rule[5] != 'ε'):
                    self.println(
                        f"{good_rule[5]} not in mashine.alphabet_y для ({mashine.state}, {char}, {mashine.stack[0]}) = ({good_rule[3]}, {good_rule[4]}, {good_rule[5]}) => цепочка не принадлежит языку")
                    return

            if good_rule[4] == "ε" and len(mashine.stack) > 1:
                mashine.stack = mashine.stack[1:]
            else:
                mashine.stack = good_rule[4] + mashine.stack[1:]

            if good_rule[5] != "ε":
                mashine.stack_y += good_rule[5]

            mashine.state = good_rule[3]

            chain = chain[1:]
            # print(f"Тек - ({mashine.state}, {char}, {mashine.stack})")
            if mashine.stack == "ε" and (mashine.state in mashine.end):
                self.println(f"({mashine.state}, 'eps', {mashine.stack})")
                self.println(f"Цепочка принадлежит данному языку, y = {mashine.stack_y}")
                return

        char = "ε"
        while  mashine.stack != "ε" or (mashine.state not in mashine.end):
            if (char not in mashine.alphabet and char != "ε"):
                self.println(
                    f"char not in mashine.alphabet для ({mashine.state}, {char}, {mashine.stack[0]}) => цепочка не принадлежит языку")
                return

            is_ok = False
            good_rule = []
            number = 0
            super_number = -1
            for rule in mashine.rules:
                number += 1
                if mashine.state == rule[0] and char == rule[1] and mashine.stack[0] == rule[2]:
                    if is_ok == True:
                        self.println(
                            f"Найдено больше одного правила для ({mashine.state}, {char}, {mashine.stack[0]}) => цепочка не принадлежит языку")
                        return
                    good_rule = rule
                    is_ok = True
                    super_number = number

            if is_ok == False:
                self.println(
                    f"Не найдено правило для ({mashine.state}, {char}, {mashine.stack[0]}) => цепочка не принадлежит языку")
                return

            self.println(f"({mashine.state}, {chain}, {mashine.stack}) переход по правилу {super_number} ({good_rule[3]}, {good_rule[4]}, {good_rule[5]}), y = '{mashine.stack_y}'")

            for c in good_rule[4]:
                if (c not in mashine.alphabet_stack and good_rule[4] != 'ε'):
                    self.println(
                        f"{good_rule[4]} not in mashine.alphabet_stack для ({mashine.state}, {char}, {mashine.stack[0]}) => цепочка не принадлежит языку")
                    return

            for c in good_rule[5]:
                if (c not in mashine.alphabet_y and good_rule[5] != 'ε'):
                    self.println(
                        f"{good_rule[5]} not in mashine.alphabet_y для ({mashine.state}, {char}, {mashine.stack[0]}) = ({good_rule[3]}, {good_rule[4]}, {good_rule[5]}) => цепочка не принадлежит языку")
                    return

            if good_rule[4] == "ε" and len(mashine.stack) > 1:
                mashine.stack = mashine.stack[1:]
            else:
                mashine.stack = good_rule[4] + mashine.stack[1:]

            if good_rule[5] != "ε":
                mashine.stack_y += good_rule[5]

            mashine.state = good_rule[3]

            chain = chain[1:]
            # print(f"Тек - ({mashine.state}, {char}, {mashine.stack})")
            if mashine.stack == "ε" and (mashine.state in mashine.end):
                self.println(f"({mashine.state}, 'eps', {mashine.stack})")
                self.println(f"Цепочка принадлежит данному языку, y = {mashine.stack_y}")
                return



    def loadTable(self, rules):
        i = 1
        self.tableWidget.setRowCount(0)
        for rule in rules:
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0,
                                     QtWidgets.QTableWidgetItem(str(i) + "."))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1,
                                     QtWidgets.QTableWidgetItem(f"δ({str(rule[0])}, {str(rule[1])}, {str(rule[2])})"))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2,
                                     QtWidgets.QTableWidgetItem(f" -> "))
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3,
                                     QtWidgets.QTableWidgetItem(f"({str(rule[3])}, {str(rule[4])}, {str(rule[5])})"))
            self.tableWidget.item(self.tableWidget.rowCount() - 1, 1).setTextAlignment(
                QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.tableWidget.item(self.tableWidget.rowCount() - 1, 2).setTextAlignment(
                QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.tableWidget.item(self.tableWidget.rowCount() - 1, 3).setTextAlignment(
                QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            i += 1

    def input(self, file):
        try:
            with open(file, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            self.println("Файл с данными не найден")
            exit(-1)
        states = data["states"]
        alphabet = data["alphabet"]
        alphabet_y = data["alphabet_y"]
        in_stack = data["in_stack"]
        rules = data["rules"]

        for rule in range(len(rules)):
            for i in range(len(rules[rule])):
                if rules[rule][i] == "EPS":
                    rules[rule][i] = "ε"

        start = data["start"]
        stack = data["start_stack"]
        stack_y = data["start_y"]
        end = data["end"]
        self.println(rules)
        print(rules)
        text = f"P({states}, {alphabet}, {in_stack}, {alphabet_y}, δ, {start}, {stack}, {end})"
        self.P.setText(text)
        self.println(text)
        machine = Machine(states, alphabet, alphabet_y, rules, start, stack, stack_y, end, in_stack)
        return machine

    def println(self, text):
        current_datetime = datetime.now()
        text = str(text).replace("ε", "'eps'")
        text = str(text).replace("δ", "'b'")
        self.log.setText(str(current_datetime) + ": " + text + "\n" + self.log.text())
        logFile = open("log.txt", "a")
        logFile.write(f"{str(current_datetime)} : {str(text)}\n")
        logFile.close()
