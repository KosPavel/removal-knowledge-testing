from PyQt5 import QtWidgets
import sys
import getpass

class TestClient(QtWidgets.QMainWindow):
    userName = ''
    questionList = []
    answerList = []
    nowQuestion = 0 #0 соответствует первому вопросу
    clientAnswer = []
    rightAnswer = []

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

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.clientName)
        self.vbox.addWidget(self.testStatus)
        self.vbox.addWidget(self.beginTestButton)

        self.window.setLayout(self.vbox)
        self.window.show()

        self.getUserInfo() #Получение имени пользователя
        self.beginTestButtonSetup() #деактивация, имя кнопки
        self.getTest() #ожидание загрузки вопросов

    def getUserInfo(self):
        self.userName = getpass.getuser()
        self.clientName.setText('<center>Ваше имя: ' + self.userName + '</center>')

    def beginTestButtonSetup(self):
        self.beginTestButton.setEnabled(False)
        self.beginTestButton.setText('Начать тест')

    def getTest(self):
        #!!!!!!!!!!!!!раз в 10 секунд попытка загрузить вопросы, пока просто откроем файл
        #и запишем вопросы и ответы в два списка
        testFile = open('test.txt', 'r')
        #далее заполнение списков вопросов, ответов и правильных ответов
        lines = 0
        for line in testFile:
            if (lines % 5 == 0):
                self.questionList.append(line)
            else:
                if line[0] == '!': #метка правильного ответа = !
                    self.rightAnswer.append('1')
                    self.answerList.append(line[1:])
                    self.clientAnswer.append('') #пользователь ещё не ответил, поэтому пробел
                else:
                    self.rightAnswer.append('0')
                    self.answerList.append(line)
                    self.clientAnswer.append('') #пользователь ещё не ответил, поэтому пробел
            lines += 1
        self.testStatus.setText('<center>Тест подготовлен, можно начать</center>')
        self.beginTestButton.setEnabled(True) #активация кнопки  начала, после загрузки вопросов

    def beginTest(self):
        self.window.hide()
        self.testStart() #переход к тесту

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
        self.answerBtn1.clicked.connect(self.makeAnswer)
        self.answerBtn2.clicked.connect(self.makeAnswer)
        self.answerBtn3.clicked.connect(self.makeAnswer)
        self.answerBtn4.clicked.connect(self.makeAnswer)

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

    def switchQuestion(self): #переход к след/пред вопросу
        sender = self.sender()
        if sender == self.previousQuestion:
            self.nowQuestion -= 1
            self.currentQuestion()
            if self.nowQuestion == 0:
                self.currentQuestion()
                self.previousQuestion.setEnabled(False)
                self.nextQuestion.setEnabled(True)
            else:
                self.currentQuestion()
                self.nextQuestion.setEnabled(True)
        else:
            self.nowQuestion += 1
            self.currentQuestion()
            if self.nowQuestion == len(self.questionList) - 1:
                self.currentQuestion()
                self.previousQuestion.setEnabled(True)
                self.nextQuestion.setEnabled(False)
            else:
                self.currentQuestion()
                self.previousQuestion.setEnabled(True)

    def currentQuestion(self): #вывод текущего вопроса и подгрузка ответа, если был
        self.questionNumber.setText('<center> Вопрос № ' + str(self.nowQuestion+1) + '</center>')
        self.questionView.setText(self.questionList[self.nowQuestion])
        self.answerBtn1.setText(self.answerList[self.nowQuestion + self.nowQuestion * 3])
        if self.clientAnswer[self.nowQuestion + self.nowQuestion * 3] == '1':
            self.answerBtn1.setEnabled(False)
            self.answerBtn2.setEnabled(True)
            self.answerBtn3.setEnabled(True)
            self.answerBtn4.setEnabled(True)
        elif self.clientAnswer[self.nowQuestion + self.nowQuestion * 3] == '':
            self.answerBtn1.setEnabled(True)
        self.answerBtn2.setText(self.answerList[self.nowQuestion + self.nowQuestion * 3 + 1])
        if self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 1] == '1':
            self.answerBtn1.setEnabled(True)
            self.answerBtn2.setEnabled(False)
            self.answerBtn3.setEnabled(True)
            self.answerBtn4.setEnabled(True)
        elif self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 1] == '':
            self.answerBtn2.setEnabled(True)
        self.answerBtn3.setText(self.answerList[self.nowQuestion + self.nowQuestion * 3 + 2])
        if self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 2] == '1':
            self.answerBtn1.setEnabled(True)
            self.answerBtn2.setEnabled(True)
            self.answerBtn3.setEnabled(False)
            self.answerBtn4.setEnabled(True)
        elif self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 2] == '':
            self.answerBtn3.setEnabled(True)
        self.answerBtn4.setText(self.answerList[self.nowQuestion + self.nowQuestion * 3 + 3])
        if self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 3] == '1':
            self.answerBtn1.setEnabled(True)
            self.answerBtn2.setEnabled(True)
            self.answerBtn3.setEnabled(True)
            self.answerBtn4.setEnabled(False)
        elif self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 3] == '':
            self.answerBtn4.setEnabled(True)

    def makeAnswer(self): # внесение ответа пользователя в массив, корректировка массива и кнопок
        sender = self.sender()
        if sender == self.answerBtn1:
            self.answerBtn1.setEnabled(False)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3] = '1'
            self.answerBtn2.setEnabled(True)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 1] = ''
            self.answerBtn3.setEnabled(True)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 2] = ''
            self.answerBtn4.setEnabled(True)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 3] = ''
        elif sender == self.answerBtn2:
            self.answerBtn2.setEnabled(False)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 1] = '1'
            self.answerBtn1.setEnabled(True)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3] = ''
            self.answerBtn3.setEnabled(True)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 2] = ''
            self.answerBtn4.setEnabled(True)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 3] = ''
        elif sender == self.answerBtn3:
            self.answerBtn3.setEnabled(False)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 2] = '1'
            self.answerBtn1.setEnabled(True)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3] = ''
            self.answerBtn2.setEnabled(True)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 1] = ''
            self.answerBtn4.setEnabled(True)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 3] = ''
        elif sender == self.answerBtn4:
            self.answerBtn4.setEnabled(False)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 3] = '1'
            self.answerBtn1.setEnabled(True)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3] = ''
            self.answerBtn2.setEnabled(True)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 1] = ''
            self.answerBtn3.setEnabled(True)
            self.clientAnswer[self.nowQuestion + self.nowQuestion * 3 + 2] = ''

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	client = TestClient()
	sys.exit(app.exec_())
