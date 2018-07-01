from PyQt5 import QtWidgets
import sys
import getpass

class TestClient(QtWidgets.QMainWindow):
    userName = ''

    def __init__(self):
        super().__init__()
        self.testInit()

    def testInit(self):
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("Начало теста")
        self.window.resize(280,200)

        self.clientName = QtWidgets.QLabel()
        self.testStatus = QtWidgets.QLabel()
        self.beginTestButton = QtWidgets.QPushButton()
        self.beginTestButton.clicked.connect(self.beginTest)

        '''
        укладка интерфейса в контейнер, вывод слоя на экран, надписи
        '''
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.clientName)
        self.vbox.addWidget(self.testStatus)
        self.vbox.addWidget(self.beginTestButton)

        self.window.setLayout(self.vbox)
        self.window.show()

        self.getUserInfo() #Получение имени пользователя
        self.beginTestButtonSetup() #деактивация, имя кнопки
        self.getTestStatus() #ожидание загрузки вопросов

    '''
    функции, собирающие информацию и получающие
    тест для прохождения
    '''

    def getUserInfo(self):
        self.userName = getpass.getuser()
        self.clientName.setText('<center>Ваше имя: ' + self.userName + '</center>')

    def beginTestButtonSetup(self):
        self.beginTestButton.setEnabled(False)
        self.beginTestButton.setText('Начать тест')

    def getTestStatus(self):
        #!!!!!!!!!!!!!раз в 10 секунд попытка загрузить вопросы
        self.beginTestButton.setEnabled(True) #активация кнопки  начала, после загрузки вопросов

    def beginTest(self):
        self.testStart() #переход к первому вопросу

    '''
    интерфейс самого теста
    '''

    def testStart(self):
        self.window.setWindowTitle("Тест")
        self.window.resize(400,600)

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	client = TestClient()
	sys.exit(app.exec_())
