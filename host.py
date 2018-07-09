from PyQt5 import QtWidgets, QtGui
import sys

class TestHost(QtWidgets.QWidget):
    fullTest = []
    questionNumber = 0

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
        self.beginCreation.clicked.connect(self.createTest)

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
        self.fullTestListCreation()

        self.createTestWindow = QtWidgets.QWidget()
        self.createTestWindow.setWindowTitle("Создание теста")
        self.createTestWindow.resize(400,400)

        self.questionNumber = QtWidgets.QLabel()
        self.enterQuestion = QtWidgets.QTextEdit("Введите вопрос")
        self.answer1 = QtWidgets.QTextEdit()
        self.answer2 = QtWidgets.QTextEdit()
        self.answer3 = QtWidgets.QTextEdit()
        self.answer4 = QtWidgets.QTextEdit()
        self.rightAnswer1 = QtWidgets.QCheckBox()
        self.rightAnswer2 = QtWidgets.QCheckBox()
        self.rightAnswer3 = QtWidgets.QCheckBox()
        self.rightAnswer4 = QtWidgets.QCheckBox()
        self.previousQuestion = QtWidgets.QPushButton('Предыдущий вопрос')
        self.previousQuestion.clicked.connect(self.switchQuestion)
        self.previousQuestion.setEnabled(False)
        self.nextQuestion = QtWidgets.QPushButton('Следующий вопрос')
        self.nextQuestion.clicked.connect(self.switchQuestion)
        self.finishTestCreation = QtWidgets.QPushButton('Завершить создание')
        self.finishTestCreation.clicked.connect(self.switchQuestion)

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
        self.vbox.addWidget(self.questionNumber)
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
        if (self.questionNumber == 0) or (self.questionNumber == ''):
            pass
        else:
            for i in range(int(self.questionNumber) * 5):
                self.fullTest.append('')
            self.howManyQuestions.hide()
            print(self.fullTest)

    def switchQuestion(self):
        pass

    def finishCreation(self):
        pass

    def loadTest(self):
        pass

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	client = TestHost()
	sys.exit(app.exec_())
