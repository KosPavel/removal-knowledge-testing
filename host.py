from PyQt5 import QtWidgets, QtGui
import sys

class TestHost(QtWidgets.QWidget):
    fullTest = []
    questionNumber = 0 #всего вопросов
    nowQuestion = 0 #сейчас первый вопрос

    def __init__(self):
        super().__init__()
        self.testInit()

    def testInit(self):
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("Инициализация")
        self.window.resize(280,200)

        self.loadTestButton = QtWidgets.QPushButton('Загрузить тест')
        self.loadTestButton.clicked.connect(self.loadTest)
        self.createTestButton = QtWidgets.QPushButton('Создать тест')
        self.createTestButton.clicked.connect(self.howManyQuestions)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.loadTestButton)
        self.vbox.addWidget(self.createTestButton)

        self.window.setLayout(self.vbox)
        self.window.show()

    def howManyQuestions(self): #ввод количества вопросов в тесте
        self.howManyQuestions = QtWidgets.QWidget()
        self.howManyQuestions.setWindowTitle("Инициализация")
        self.howManyQuestions.resize(280,200)

        self.infoEnterNumber = QtWidgets.QLabel('Введите количество вопросов в тесте')
        self.enterNumber = QtWidgets.QLineEdit()
        self.beginCreation = QtWidgets.QPushButton('Начать создание теста')
        self.beginCreation.clicked.connect(self.fullTestListCreation)

        self.validateQuestionNumber = QtGui.QIntValidator() #проверка ввода числа
        self.enterNumber.setValidator(self.validateQuestionNumber)

        self.vertBox = QtWidgets.QVBoxLayout()
        self.vertBox.addWidget(self.infoEnterNumber)
        self.vertBox.addWidget(self.enterNumber)
        self.vertBox.addWidget(self.beginCreation)
        self.howManyQuestions.setLayout(self.vertBox)
        self.window.hide()
        self.howManyQuestions.show()

    def createTest(self):
        self.createTestWindow = QtWidgets.QWidget()
        self.createTestWindow.setWindowTitle("Создание теста")
        self.createTestWindow.resize(400,400)

        self.questionNumberLabel = QtWidgets.QLabel()
        self.questionNumberLabel.setText('<center>Вопрос № ' + str(self.nowQuestion + 1) + '</center>')
        self.enterQuestion = QtWidgets.QTextEdit("Введите вопрос")
        self.answer1 = QtWidgets.QTextEdit('Введите ответ, отметьте правильность')
        self.answer2 = QtWidgets.QTextEdit('Введите ответ, отметьте правильность')
        self.answer3 = QtWidgets.QTextEdit('Введите ответ, отметьте правильность')
        self.answer4 = QtWidgets.QTextEdit('Введите ответ, отметьте правильность')
        self.rightAnswer1 = QtWidgets.QCheckBox()
        self.rightAnswer2 = QtWidgets.QCheckBox()
        self.rightAnswer3 = QtWidgets.QCheckBox()
        self.rightAnswer4 = QtWidgets.QCheckBox()

        self.buttonGroup = QtWidgets.QButtonGroup() # exclusive checkboxes
        self.buttonGroup.addButton(self.rightAnswer1)
        self.buttonGroup.addButton(self.rightAnswer2)
        self.buttonGroup.addButton(self.rightAnswer3)
        self.buttonGroup.addButton(self.rightAnswer4)

        self.previousQuestion = QtWidgets.QPushButton('Предыдущий вопрос')
        self.previousQuestion.clicked.connect(self.switchQuestion)
        self.previousQuestion.setEnabled(False)
        self.nextQuestion = QtWidgets.QPushButton('Следующий вопрос')
        self.nextQuestion.clicked.connect(self.switchQuestion)
        self.finishTestCreation = QtWidgets.QPushButton('Завершить создание')
        self.finishTestCreation.clicked.connect(self.finishCreation)

        self.hbox0 = QtWidgets.QHBoxLayout()
        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox2 = QtWidgets.QHBoxLayout()
        self.hbox3 = QtWidgets.QHBoxLayout()
        self.hbox4 = QtWidgets.QHBoxLayout()
        self.hbox0.addWidget(self.answer1)
        self.hbox0.addWidget(self.rightAnswer1)
        self.hbox1.addWidget(self.answer2)
        self.hbox1.addWidget(self.rightAnswer2)
        self.hbox2.addWidget(self.answer3)
        self.hbox2.addWidget(self.rightAnswer3)
        self.hbox3.addWidget(self.answer4)
        self.hbox3.addWidget(self.rightAnswer4)
        self.hbox4.addWidget(self.previousQuestion)
        self.hbox4.addWidget(self.finishTestCreation)
        self.hbox4.addWidget(self.nextQuestion)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.questionNumberLabel)
        self.vbox.addWidget(self.enterQuestion)
        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox4)

        self.createTestWindow.setLayout(self.vbox)
        self.createTestWindow.show()

    def fullTestListCreation(self): #заполнение пробелами списка fullTest, количество пробелов = вопросы + ответы
        self.questionNumber = self.enterNumber.text()
        if (self.questionNumber == '0') or (self.questionNumber == ''):
            pass
        else:
            for i in range(int(self.questionNumber) * 5):
                if (i % 5) == 0:
                    self.fullTest.append('Введите вопрос')
                else:
                    self.fullTest.append('Введите ответ, отметьте правильность')
            self.howManyQuestions.hide()
            self.createTest()

    def switchQuestion(self):
        sender = self.sender()
        if sender == self.previousQuestion:
            self.fillQuestion()
            self.nowQuestion -= 1
            self.questionNumberLabel.setText('<center>Вопрос № ' + str(self.nowQuestion + 1) + '</center>')
            self.currentQuestion()
            if self.nowQuestion == 0:
                self.previousQuestion.setEnabled(False)
                self.nextQuestion.setEnabled(True)
            else:
                self.nextQuestion.setEnabled(True)
        else:
            self.fillQuestion()
            self.nowQuestion += 1
            self.questionNumberLabel.setText('<center>Вопрос № ' + str(self.nowQuestion + 1) + '</center>')
            self.currentQuestion()
            if self.nowQuestion == int(self.questionNumber) - 1:
                self.previousQuestion.setEnabled(True)
                self.nextQuestion.setEnabled(False)
            else:
                self.previousQuestion.setEnabled(True)

    def fillQuestion(self): #записать вопрос и ответы в список
        question = self.enterQuestion.toPlainText()
        enteredAnswer1 = self.answer1.toPlainText()
        enteredAnswer2 = self.answer2.toPlainText()
        enteredAnswer3 = self.answer3.toPlainText()
        enteredAnswer4 = self.answer4.toPlainText()
        fullTestPosition = self.nowQuestion * 5
        self.fullTest[fullTestPosition] = question
        if self.rightAnswer1.isChecked() == True:
            self.fullTest[fullTestPosition + 1] = '!' + enteredAnswer1
        else:
            self.fullTest[fullTestPosition + 1] = enteredAnswer1
        if self.rightAnswer2.isChecked() == True:
            self.fullTest[fullTestPosition + 2] = '!' + enteredAnswer2
        else:
            self.fullTest[fullTestPosition + 2] = enteredAnswer2
        if self.rightAnswer3.isChecked() == True:
            self.fullTest[fullTestPosition + 3] = '!' + enteredAnswer3
        else:
            self.fullTest[fullTestPosition + 3] = enteredAnswer3
        if self.rightAnswer4.isChecked() == True:
            self.fullTest[fullTestPosition + 4] = '!' + enteredAnswer4
        else:
            self.fullTest[fullTestPosition + 4] = enteredAnswer4

    def currentQuestion(self): #показать вопрос, если уже был заполнен
        fullTestPosition = self.nowQuestion * 5
        question = self.fullTest[fullTestPosition]
        enteredAnswer1 = self.fullTest[fullTestPosition + 1]
        enteredAnswer2 = self.fullTest[fullTestPosition + 2]
        enteredAnswer3 = self.fullTest[fullTestPosition + 3]
        enteredAnswer4 = self.fullTest[fullTestPosition + 4]
        self.enterQuestion.setText(question)
        if enteredAnswer1[0] == '!':
            self.answer1.setText(enteredAnswer1[1:])
            self.rightAnswer1.setChecked(True)
        else:
            self.answer1.setText(enteredAnswer1)
        if enteredAnswer2[0] == '!':
            self.answer2.setText(enteredAnswer2[1:])
            self.rightAnswer2.setChecked(True)
        else:
            self.answer2.setText(enteredAnswer2)
        if enteredAnswer3[0] == '!':
            self.answer3.setText(enteredAnswer3[1:])
            self.rightAnswer3.setChecked(True)
        else:
            self.answer3.setText(enteredAnswer3)
        if enteredAnswer4[0] == '!':
            self.answer4.setText(enteredAnswer4[1:])
            self.rightAnswer4.setChecked(True)
        else:
            self.answer4.setText(enteredAnswer4)

    def finishCreation(self):
        self.fillQuestion()
        if self.checkTest() == False:
            self.questionNumberLabel.setText('<center><b>Где-то не отмечен правильный ответ!</b><center>')
        else:
            fileTest = open('Test.txt', 'w')
            for line in range(len(self.fullTest)):
                fileTest.write(self.fullTest[line] + '\n')
            fileTest.close()

    # def warningWindow(self, warnText): #окно-предупреждение об ошибке НЕ РАБОТАЕТ
    #     warningWindow = QtWidgets.QWidget()
    #     warningWindow.setWindowTitle("Achtung!")
    #     warningWindow.resize(100,100)
    #     warningLabel = QtWidgets.QLabel()
    #     warningLabel.setText(warnText)
    #     vbox = QtWidgets.QVBoxLayout()
    #     vbox.addWidget(warningLabel)
    #     warningWindow.setLayout(vbox)
    #     warningWindow.show()

    def checkTest(self):
        totalRightAnswers = 0
        for i in range(len(self.fullTest)):
            if self.fullTest[i][0] == '!':
                totalRightAnswers += 1
        if totalRightAnswers == int(self.questionNumber):
            result = True
        else:
            result = False
        print(self.questionNumber)
        print(self.fullTest)
        print(totalRightAnswers)
        return result

    def loadTest(self):
        pass

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	client = TestHost()
	sys.exit(app.exec_())
