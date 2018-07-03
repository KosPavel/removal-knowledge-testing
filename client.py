from PyQt5 import QtWidgets
import sys
import getpass

class TestClient(QtWidgets.QMainWindow):
    userName = ''
    questionList = []
    answerList = []
    nowQuestion = 0 #0 соответствует первому вопросу
    clientAnswer = []

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
        testFile = open('test.txt', 'r')
        lines = 0
        for line in testFile:
            if (lines % 5 == 0):
                self.questionList.append(line)
            else:
                self.answerList.append(line)
            lines += 1
        #!!!!!!!!!!!!!раз в 10 секунд попытка загрузить вопросы, пока просто откроем файл
        #и запишем вопросы и ответы в два списка
        self.testStatus.setText('<center>Тест подготовлен, можно начать</center>')
        self.beginTestButton.setEnabled(True) #активация кнопки  начала, после загрузки вопросов

    def beginTest(self):
        self.window.hide()
        self.testStart() #переход к тесту

    '''
    интерфейс самого теста
    '''

    def testStart(self):

        self.testWindow = QtWidgets.QWidget()
        self.testWindow.setWindowTitle("Тест")
        self.testWindow.resize(400,400)

        self.questionView = QtWidgets.QTextBrowser()

        self.timer = QtWidgets.QLabel()
        self.questionNumber = QtWidgets.QLabel()
        self.hboxtop = QtWidgets.QHBoxLayout()
        self.hboxtop.addWidget(self.questionNumber)
        self.hboxtop.addWidget(self.timer)

        self.answerBtn1 = QtWidgets.QPushButton()
        self.answerBtn2 = QtWidgets.QPushButton()
        self.answerBtn3 = QtWidgets.QPushButton()
        self.answerBtn4 = QtWidgets.QPushButton()

        self.previousQuestion = QtWidgets.QPushButton('Предыдущий вопрос')
        self.nextQuestion = QtWidgets.QPushButton('Следующий вопрос')
        self.previousQuestion.setEnabled(False)
        self.previousQuestion.clicked.connect(self.switchQuestion)
        self.nextQuestion.clicked.connect(self.switchQuestion)
        self.finishTest = QtWidgets.QPushButton('Завершить тест')

        self.hboxbot = QtWidgets.QHBoxLayout()
        self.hboxbot.addWidget(self.previousQuestion)
        self.hboxbot.addWidget(self.finishTest)
        self.hboxbot.addWidget(self.nextQuestion)

        self.testVbox = QtWidgets.QVBoxLayout()
        self.testVbox.addStretch(1)
        self.testVbox.addLayout(self.hboxtop)
        self.testVbox.addWidget(self.questionView)
        self.testVbox.addWidget(self.answerBtn1)
        self.testVbox.addWidget(self.answerBtn2)
        self.testVbox.addWidget(self.answerBtn3)
        self.testVbox.addWidget(self.answerBtn4)
        self.testVbox.addLayout(self.hboxbot)

        self.testWindow.setLayout(self.testVbox)
        self.currentQuestion()
        self.testWindow.show()

    def switchQuestion(self):
        sender = self.sender()
        if sender == self.previousQuestion:
            if self.nowQuestion == 0:
                pass
            else:
                self.nowQuestion -= 1
                self.previousQuestion.setEnabled(True)
                self.currentQuestion()
                if self.nowQuestion == 0:
                    self.previousQuestion.setEnabled(False)
                    self.nextQuestion.setEnabled(True)
        else:
            if self.nowQuestion == len(self.questionList) - 1:
                pass
            else:
                self.nowQuestion += 1
                self.nextQuestion.setEnabled(True)
                self.currentQuestion()
                if self.nowQuestion == len(self.questionList) - 1:
                    self.nextQuestion.setEnabled(False)
                    self.previousQuestion.setEnabled(True)

    def currentQuestion(self):
        self.questionView.setText(self.questionList[self.nowQuestion])
        self.answerBtn1.setText(self.answerList[self.nowQuestion + self.nowQuestion * 3])
        self.answerBtn2.setText(self.answerList[self.nowQuestion + self.nowQuestion * 3 + 1])
        self.answerBtn3.setText(self.answerList[self.nowQuestion + self.nowQuestion * 3 + 2])
        self.answerBtn4.setText(self.answerList[self.nowQuestion + self.nowQuestion * 3 + 3])

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	client = TestClient()
	sys.exit(app.exec_())
