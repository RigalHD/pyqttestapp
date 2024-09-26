import sys
from dotenv import load_dotenv
from os import getenv
from sqlalchemy.orm import Session
from sqlalchemy import select, inspect, MetaData, create_engine, Engine
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt6.QtWidgets import QMainWindow, QLabel

from qtttdb import Users, Base


class FirstForm(QMainWindow):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine: Engine = engine
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Главная форма')
        self.btn = QPushButton('Другая форма', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(100, 100)
        self.btn.clicked.connect(self.open_second_form)

    def open_second_form(self):
        self.second_form = SecondForm(self, "Данные для второй формы")
        self.second_form.show()


class SecondForm(QWidget):
    def __init__(self, engine: Engine, *args):
        super().__init__()
        self.engine: Engine = engine
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Вторая форма')
        self.lbl = QLabel(args[-1], self)
        self.lbl.adjustSize()


class AuthForm(QWidget):
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine: Engine = engine
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Вход или регистрация')
        
        self.authorisation_label = QLabel("Авторизация", self)
        self.authorisation_label.adjustSize()
        self.authorisation_label.move(125, 50)
        
        self.error_label = QLabel("", self)
        self.error_label.adjustSize()
        self.error_label.move(100, 75)
        
        self.login_btn = QPushButton('Вход', self)
        self.login_btn.resize(self.login_btn.sizeHint())
        self.login_btn.move(160, 230)
        self.login_btn.clicked.connect(self.login_user)
        
        self.reg_btn = QPushButton('Рег', self)
        self.reg_btn.resize(self.reg_btn.sizeHint())
        self.reg_btn.move(60, 230)
        self.reg_btn.clicked.connect(self.register_user)
        
        self.name_input = QLineEdit(self)
        self.name_input.move(100, 150)
        
        self.password_input = QLineEdit(self)
        self.password_input.move(100, 200)

    def register_user(self):
        with Session(engine) as session:
            # Base.metadata.drop_all(engine)
            # Base.metadata.create_all(engine)
            with session.begin():
                if not self.name_input.text() or not self.password_input.text():
                    self.error_label.setText("Нельзя оставлять поля пустыми")
                    self.error_label.adjustSize()
                elif self.name_input.text() in session.scalars(select(Users.name)):
                    self.error_label.setText("Такое имя уже есть")
                    self.error_label.adjustSize()
                else:
                    user = Users(
                        name=self.name_input.text(), 
                        password=self.password_input.text()
                        )
                    session.merge(user)
                    self.main_form = FirstForm(engine=self.engine)
                    self.main_form.show()
                    self.close()
    
    def login_user(self):
        with Session(engine) as session:
            user = session.scalar(
                select(
                    Users
                    ).where(
                        Users.name==self.name_input.text(),
                        Users.password==self.password_input.text()
                    )
                )
            if user:
                self.main_form = FirstForm(engine=self.engine)
                self.main_form.show()
                self.close()
            else:
                self.error_label.setText("Неверный логин или пароль")


if __name__ == '__main__':
    engine: Engine = create_engine(
        getenv("SQLALCHEMY_URL"),
        echo=True
    )
    app = QApplication(sys.argv)
    reg = AuthForm(engine=engine)
    reg.show()
    sys.exit(app.exec())
    