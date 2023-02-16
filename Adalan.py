from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QMovie, QIcon, QPixmap
from PyQt6.uic import loadUi
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
import random
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Adalan.ui", self)
        #self.setFixedSize(281, 251)
        self.setMaximumWidth(self.width())
        self.setMaximumHeight(self.height())
        # Global variables
        self.slider_max = 100
        self.slider_min = 0
        self.timer_delay = 5000
        self.start = False
        self.count = 0
        self.total_questions = 10
        self.operator_list = []
        self.operator_dict = {"Addition": "+", "Subtraction": "-", "Multiplication": "X", "Division": "/"}
        self.total_correct = 0
        self.total_wrong = 0
        self.movie = None
        self.passed_gif = None
        self.failed_gif = None
        self.answer_response_time = []
        self.question_index = []

        # Icon
        self.setWindowIcon(QIcon('adalan_icon.png'))

        # Initialization the UI components
        self.chk_add.setChecked(True)
        self.operator_list.append(self.chk_add.text())
        self.txt_errors.appendPlainText("Wrong answers\n")

        # Time initialization
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_time)
        self.dial_delay.setValue(5)
        self.lbl_delay.setText(str(self.dial_delay.value()) + " seconds")

        # Operator selection
        self.chk_add.stateChanged.connect(lambda : self.op_state(self.chk_add))
        self.chk_sub.stateChanged.connect(lambda : self.op_state(self.chk_sub))
        self.chk_mul.stateChanged.connect(lambda : self.op_state(self.chk_mul))
        self.chk_div.stateChanged.connect(lambda : self.op_state(self.chk_div))

        # hide inputs
        self.hide_controls()
        self.brn_show_result.hide()

        # Input number validation
        self.inp_1.setValidator(QIntValidator(0, 100000))
        self.inp_2.setValidator(QIntValidator(0, 100000))
        self.inp_result.setValidator(QDoubleValidator(-1000000000, 1000000000, 0))

        # Set the slider value
        self.int_range.setMinimum(self.slider_min)
        self.int_range.setMaximum(self.slider_max)
        self.slider_position = int(self.slider_max / 2)
        self.int_range.setValue(self.slider_position)
        self.lbl_upper_limt.setText(str(self.int_range.value()))
        self.lbl_lower_limit.setText(str(self.slider_min))

        # Total Questions slider
        self.inp_total_question.setMinimum(1)
        self.inp_total_question.setMaximum(100)
        self.inp_total_question.setValue(10)
        self.lbl_total_ques_lower.setText(str(1))
        self.lbl_total_ques_upper.setText("100")
        self.lbl_ques_cnt.setText("10")

        # Test start button
        self.btn_start.setChecked(True)  # set the initial status to True

        # Slots
        self.inp_result.returnPressed.connect(self.validate_result)
        self.int_range.valueChanged.connect(self.set_range)
        self.btn_start.clicked.connect(self.set_test_status_btn)
        self.dial_delay.valueChanged.connect(self.set_dial_text)
        self.inp_total_question.valueChanged.connect(self.update_total_questions)
        self.menu_howto.triggered.connect(self.how_to)
        self.menu_about.triggered.connect(self.about_adalan)
        self.menu_req.triggered.connect(self.menu_requirements)

        # Default options for ui
        self.disable_user_input()  # disable user inputs
        self.update_gifs()

    def menu_requirements(self):
        message = "Windows 10 OS\n" \
                  "Python 3.8+\n" \
                  "and a smiling face :)"
        QMessageBox.about(self, "Requirements", message)


    def how_to(self):
        message = "To use adalan follow the steps\n\n" \
                  "1. Set the numbers range to fix the min and max range.\n" \
                  "This is used to randomly pick numbers between the min max value. The default value is 50\n" \
                  "2. Set the total questions for the test. Default value is 10 and you can choose up to 100 questions\n" \
                  "3. Set the delay by rotating the knob. This is the time in which you need to answer the question" \
                  "4. Click the start button to start the test\n" \
                  "5. Once you click the start button the timer will start decrementing and you need to answer before the" \
                  "time reaches 0s.The answer is validated and you know the results with the funny jif :) \n\n" \
                  "Tip: You can use the enter key to validate the answer or after 0 seconds it will auto eveluate your results." \
                  "\n\n isn't it FUNNY ......"
        QMessageBox.about(self, "Using Adalan Application", message)

    def about_adalan(self):
        message = "Adalan is an application developed by Prabhu Kalaimani.\n" \
                  "It is a fun application to learn mathematics. \nIt helps childrens to" \
                  "shrapen their basic mathematics skills. \nThis application is tested by Shraven Prabu\n" \
                  "This application is built and tested on windows platform.\n\nFor any queries improvements please e-mail\n" \
                  "prabhu_tigers@yahoo.com"

        QMessageBox.about(self, "About Adalan", message)

    def update_gifs(self):
        self.passed_gif = ([file for file in os.listdir('gifs/correct_gif') if file.endswith('.gif')])
        self.failed_gif = ([file for file in os.listdir('gifs/wrong_gif') if file.endswith('.gif')])

    def display_image(self, status):
        if status:
            gif_file = "gifs/correct_gif/" + random.choice(self.passed_gif)
            self.movie = QMovie(gif_file)
        else:
            gif_file = "gifs/wrong_gif/" + random.choice(self.failed_gif)
            self.movie = QMovie(gif_file)

        self.lbl_disp.setMovie(self.movie)
        self.movie.start()

    def stop_image(self):
        self.lbl_disp.clear()

    def set_dial_text(self):
        wait_time = self.dial_delay.value()
        self.lbl_delay.setText(str( wait_time) + " seconds")

    def op_state(self, chkbox):
        op_name = chkbox.text()
        if op_name not in self.operator_list and chkbox.isChecked():
            self.operator_list.append(op_name)
        if op_name in self.operator_list and not chkbox.isChecked():
            self.operator_list.remove(op_name)
        # print("List = ", self.operator_list)

    def set_test_status_btn(self):
        self.start_testing()

    def update_total_questions(self, val):
        self.total_questions = val
        self.lbl_ques_cnt.setText(str(val))

    def set_range(self, val):
        """
        This method will set the label while the vertical scroller position is changed
        :param val: vertical scroller position
        :return: None
        """
        self.lbl_upper_limt.setText(str(val))
        self.slider_position = val

    def get_random(self, start=1, end=100):
        """
        this method will return a random number between start and end value
        :param start: stating of the random number
        :param end:  ending range of the random-number
        :return random_num: random number between start and end
        """
        random_num = random.randint(start, end)
        return random_num

    def show_controls(self):
        self.inp_1.show()
        self.inp_2.show()
        self.lbl_equal.show()
        self.inp_result.show()
        self.lbl_ans_hint.show()
        self.lbl_operator.show()

    def hide_controls(self):
        self.inp_1.hide()
        self.inp_2.hide()
        self.lbl_equal.hide()
        self.inp_result.hide()
        self.lbl_ans_hint.hide()
        self.lbl_operator.hide()

    def start_testing(self):
        if len(self.operator_list) == 0:
            # print("Throw error to select at least one operator")
            QMessageBox.critical(self, "No operator is chosen !!!", "Chose at least one operator")
        else:
            self.lbl_ans_status.hide()
            self.lock_ui()
            self.show_controls()
            self.timer.start(1000)
            self.stop_image()
            self.enable_user_input()
            self.count = self.dial_delay.value()
            self.lbl_timer.setText(str(self.count))
            self.start = True
            # print("Test in progress...")

            x = self.get_random(self.slider_min, self.slider_position)
            y = self.get_random(self.slider_min, self.slider_position)
            operator = self.operator_dict[random.choice(self.operator_list)]

            # Handle divide by division

            if operator == "/":
                if x == 0 and y == 0:
                    x = 1
                    y = 1
                res = 1
                if y == 0:
                    tmp_val = x
                    x = y
                    y = tmp_val
                res = x * y
                x = res

            # print(x, operator, y)
            self.inp_1.setText(str(x))
            self.lbl_operator.setText(operator)
            self.inp_2.setText(str(y))

    def disable_user_input(self):
        self.btn_start.setEnabled(True)
        self.btn_start.setStyleSheet("background-color : green")
        self.inp_result.setEnabled(False)
        self.btn_start.setFocus()

    def enable_user_input(self):
        self.inp_result.setEnabled(True)
        self.btn_start.setEnabled(False)
        self.btn_start.setStyleSheet("background-color : orange")
        self.btn_start.hide()
        self.btn_start.setText(" ")
        self.inp_result.setFocus()

    def validate_result(self):

        x = int(self.inp_1.text())
        y = int(self.inp_2.text())
        operator = self.lbl_operator.text()

        if self.inp_result.text() == "":
            result = 0
        else:
            result = int(self.inp_result.text())

        # update the status
        tmp_cnt = self.inp_total_question.value() - self.total_questions + 1
        per_complete = int((tmp_cnt / self.inp_total_question.value()) * 100)
        completion_txt = f"{tmp_cnt}/{self.inp_total_question.value()}  {per_complete} % Completed "
        self.lbl_completion_status.setText(completion_txt)

        # Fill up the response time
        time = self.dial_delay.value() - int(self.lbl_timer.text())
        self.answer_response_time.append(time)
        self.question_index.append(tmp_cnt)
        # print("question ", tmp_cnt)
        # print("response time ", str(time))


        # First clear x and y
        self.inp_1.clear()
        self.inp_2.clear()
        self.inp_result.clear()
        self.lbl_operator.clear()

        result_status = False
        correct_ans = 0
        # Evaluate statement
        if operator == "+":
            correct_ans = x + y
            result_status = (result == correct_ans)
        elif operator == "-":
            correct_ans = x - y
            result_status = (result == correct_ans)
        elif operator == "X":
            correct_ans = x * y
            result_status = (result == correct_ans)
        elif operator == "/":
            correct_ans = round(x / y)
            result_status = (result == correct_ans)

        # print(f"{result_status} {x} {operator} {y} = {result}")
        if result_status:
            self.total_correct += 1
            self.display_image(result_status)
            self.lbl_ans_status.setStyleSheet("background-color : green")
            self.lbl_ans_status.setText("Correct Answer !!!")
        else:
            self.total_wrong += 1
            self.txt_errors.appendPlainText(f"Q-{self.total_questions}: {x} {operator} {y} = {result} Ans: {correct_ans}")
            self.display_image(result_status)
            self.lbl_ans_status.setStyleSheet("background-color : red")
            self.lbl_ans_status.setText("Wrong Answer !!!")

        self.total_questions -= 1
        self.lbl_ques_cnt.setText(str(self.total_questions))
        self.lbl_passed_cnt.setText(str(self.total_correct))
        self.lbl_failed_cnt.setText(str(self.total_wrong))
        self.inp_result.setText("")
        self.start = False
        self.count = self.dial_delay.value()
        self.disable_user_input()
        self.btn_start.show()
        self.lbl_ans_status.show()

        if self.total_questions == 0:
            self.reset_ui()
            dialog = ShowResults(patent=self)
            dialog.exec()
            self.total_correct = 0
            self.total_wrong = 0
            self.lbl_ans_status.hide()
            self.lbl_completion_status.clear()
            self.lbl_disp.clear()
            self.lbl_timer.setText('0')
            self.txt_errors.clear()
            self.txt_errors.appendPlainText("Wrong answers\n")
        else:
            self.btn_start.setText("Next Question")
            self.hide_controls()

    def reset_ui(self):
        self.btn_start.setText("Start Test")
        self.inp_total_question.setEnabled(True)
        self.dial_delay.setEnabled(True)
        self.int_range.setEnabled(True)
        self.total_questions = self.inp_total_question.value()
        self.lbl_ques_cnt.setText(str(self.total_questions))
        self.lbl_passed_cnt.setText("0")
        self.lbl_failed_cnt.setText("0")

    def lock_ui(self):
        self.inp_total_question.setEnabled(False)
        self.dial_delay.setEnabled(False)
        self.int_range.setEnabled(False)

    def show_time(self):
        # checking if flag is true
        if self.start:
            # incrementing the counter
            self.count -= 1

            # timer is completed
            if self.count == 0:
                # making flag false
                self.start = False
                # setting text to the label
                self.lbl_timer.setText("0")
                self.validate_result()

        if self.start:
            # getting text from count
            text = str(self.count)
            # showing text
            self.lbl_timer.setText(text)


class ShowResults(QDialog):
    """
    This class is for the plots
    """
    def __init__(self, patent=None):
        super().__init__(patent)
        self.parent = patent
        loadUi("Results.ui", self)
        self.setMaximumWidth(self.width())
        self.setMaximumHeight(self.height())

        # Bar chart - Pass Vs Failed chart
        self.pass_fail_graph.setTitle(title="Pass Vs Failed")
        total_questions = self.parent.total_questions
        total_corrects = self.parent.total_correct
        total_wrongs = self.parent.total_wrong
        # Calculate the pass percentage
        pass_percentage = round((total_corrects / total_questions) * 100)
        self.setWindowIcon(QIcon('adalan_icon.png'))
        pixmap = QPixmap('adalan_icon.png')
        self.ada_icon.setPixmap(pixmap)
        self.ada_icon.setScaledContents(True)

        status_list = ['Failed', 'Passed']
        ticks = []
        xval = list(range(1, len(status_list) + 1))

        bargraph = pg.BarGraphItem(x=[1], height=[total_wrongs], width=0.8, brush='red')
        self.pass_fail_graph.addItem(bargraph)
        bargraph = pg.BarGraphItem(x=[2], height=[total_corrects], width=0.8, brush='green')
        self.pass_fail_graph.addItem(bargraph)

        for i, item in enumerate(status_list):
            ticks.append((xval[i], item))
        ticks = [ticks]
        ax = self.pass_fail_graph.getAxis('bottom')
        ax.setTicks(ticks)

        self.lbl_total.setText(str(total_questions))
        self.lbl_correct.setText(str(total_corrects))
        self.lbl_wrong.setText(str(total_wrongs))
        # self.lbl_quick.setText("1")
        self.lbl_pass_percentage.setText(str(pass_percentage)+"%")

        # Plotting response graph
        time_list = self.parent.answer_response_time
        ques_index = self.parent.question_index
        self.lbl_summary.setText(f"Out of {total_questions} questions you have answered {total_corrects} correctly and {total_wrongs} incorrectly.\n"
                                 f"Your pass percentage is {pass_percentage} %.\n")

        self.response_time_graph.setTitle(title="Response Time")
        self.response_time_graph.plot(ques_index, time_list)
        ques_index = []
        time_list = []



app = QApplication([])
win = MainWindow()
win.show()
app.exec()
