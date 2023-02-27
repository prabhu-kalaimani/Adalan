#########################################################################
#
#   Designed and developed by Prabhu Kalaimani
#   prabhu_tigers@yahoo.com
#
##########################################################################

from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QStatusBar
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QMovie, QIcon, QPixmap
from PyQt6.uic import loadUi
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
import random
import os
import math
# pyinstaller --windowed --icon=adalan_icon.ico --add-data="*.ui;."  --add-data="gifs/;gifs/"  Adalan.py


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Adalan.ui", self)
        self.setMaximumWidth(self.width())
        self.setMaximumHeight(self.height())
        self.adalan_version = "2.0"
        # Global variables
        self.slider_max = 100
        self.slider_min = 0
        self.timer_delay = 5000
        self.start = False
        self.count = 0
        self.total_questions = 10
        self.operator_list = []
        self.operator_dict = {"Addition": "+", "Subtraction": "-", "Multiplication": "X",
                              "Division": "/", "Square":"x2", "Cube":"x3", "SquareRoot": "sqrt"}
        self.total_correct = 0
        self.total_wrong = 0
        self.movie = None
        self.passed_gif = None
        self.failed_gif = None
        self.answer_response_time = []
        self.question_index = []
        # To display vertically
        self.vertical_display = False

        # vertical display
        self.vertical_display = False
        self.lbl_inp1.hide()
        self.lbl_inp2.hide()
        self.lbl_operator_1.hide()
        self.inp_power_y1.hide()

        # Icon
        self.setWindowIcon(QIcon('adalan_icon.png'))

        self.lbl_score_board.setStyleSheet("border-image : url(gifs/scoreboard.jpg);background-position: center;")


        # Status barlbl_score_board
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        msg = f"Welcome to Adalan {self.adalan_version}. Press Start Test button to start the test. You can use the enter keyboard for entering answers and moving to the next question..."
        self.status_message(msg)

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
        self.chk_square.stateChanged.connect(lambda : self.op_state(self.chk_square))
        self.chk_cbrt.stateChanged.connect(lambda : self.op_state(self.chk_cbrt))
        self.chk_sqrt.stateChanged.connect(lambda : self.op_state(self.chk_sqrt))

        # Vertical display button
        # self.chk_vertical.stateChanged.connect(lambda : self.vertical_change(self.chk_vertical))

        # hide inputs
        self.inp_power_y.hide()
        self.hide_controls()

        # Input number validation
        self.inp_result.setValidator(QDoubleValidator(-1000000000, 1000000000, 2))

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

        self.inp_1.textChanged.connect(self.lbl_inp1.setText)
        self.inp_2.textChanged.connect(self.lbl_inp2.setText)
        self.lbl_operator.textChanged.connect(self.lbl_operator_1.setText)
        self.inp_power_y.textChanged.connect(self.inp_power_y1.setText)

        # Default options for ui
        self.disable_user_input()  # disable user inputs
        self.update_gifs()

    def status_message(self, msg):
        self.statusBar.clearMessage()
        self.statusBar.showMessage(msg)

    def menu_requirements(self):
        """
        Requirements menu
        """
        message = "Windows 10 OS\n" \
                  "Python 3.8+\n" \
                  "and a smiling face :)"
        QMessageBox.about(self, "Requirements", message)

    def how_to(self):
        """
        how to dialog
        """
        message = f"To use Adalan {self.adalan_version} follow the steps\n\n" \
                  "1. Set the numbers range to fix the min and max range.\n" \
                  "This is used to randomly pick numbers between the min max value. The default value is 50\n" \
                  "2. Set the total questions for the test. Default value is 10 and you can choose up to 100 questions\n" \
                  "3. Set the delay by rotating the knob. This is the time in which you need to answer the question" \
                  "4. Click the start button to start the test\n" \
                  "5. Once you click the start button the timer will start decrementing and you need to answer before the" \
                  "time reaches 0s.The answer is validated and you know the results with the funny jif :) \n\n" \
                  "Tip: You can use the enter key to validate the answer or after 0 seconds it will auto eveluate your results." \
                  "\n\n isn't it FUNNY ......"
        QMessageBox.about(self, f"Using Adalan Application {self.adalan_version}", message)

    def about_adalan(self):
        """
        Aoubt adalan dialog
        """
        message = f"Adalan {self.adalan_version} is an application developed by Prabhu Kalaimani.\n" \
                  "It is a fun application to learn mathematics. \nIt helps childrens to" \
                  "shrapen their basic mathematics skills. \nThis application is tested by Shraven Prabu\n" \
                  "This application is built and tested on windows platform.\n\nFor any queries improvements please e-mail\n" \
                  "prabhu_tigers@yahoo.com"

        QMessageBox.about(self, f"About Adalan {self.adalan_version}", message)

    def update_gifs(self):
        """
        Update gifs
        """
        self.passed_gif = ([file for file in os.listdir('gifs/correct_gif') if file.endswith('.gif')])
        self.failed_gif = ([file for file in os.listdir('gifs/wrong_gif') if file.endswith('.gif')])

    def display_image(self, status):
        """
        Displaying images
        """
        if status:
            gif_file = "gifs/correct_gif/" + random.choice(self.passed_gif)
            self.movie = QMovie(gif_file)
        else:
            gif_file = "gifs/wrong_gif/" + random.choice(self.failed_gif)
            self.movie = QMovie(gif_file)

        self.lbl_disp.setMovie(self.movie)
        self.lbl_disp.setScaledContents(True)
        self.movie.start()

    def stop_image(self):
        """
        Method which stops the image
        """
        self.lbl_disp.clear()

    def set_dial_text(self):
        """
        Handles seconds dial
        """
        wait_time = self.dial_delay.value()
        self.lbl_delay.setText(str( wait_time) + " seconds")

    # def vertical_change(self, chkbox):
    #     if chkbox.isChecked():
    #         self.vertical_display = True
    #     else:
    #         self.vertical_display = False

    def op_state(self, chkbox):
        """
        Handles operator check box
        """
        op_name = chkbox.text()
        if op_name not in self.operator_list and chkbox.isChecked():
            self.operator_list.append(op_name)
        if op_name in self.operator_list and not chkbox.isChecked():
            self.operator_list.remove(op_name)

    def set_test_status_btn(self):
        """
        Starts the test
        """
        self.start_testing()

    def update_total_questions(self, val):
        """
        Total questions
        """
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

    def show_controls(self, operator, vertical_control):
        """
        Displays controls
        """
        if vertical_control:
            # print("Vertical ui is on")
            self.inp_1.hide()
            self.inp_2.hide()
            self.inp_power_y.hide()
            self.lbl_operator.hide()

            if operator == "x2" or operator == "x3":
                self.lbl_inp1.hide()
                self.lbl_operator_1.hide()
                self.lbl_inp2.show()
                self.inp_power_y1.show()
            elif operator == "sqrt":
                self.lbl_operator.hide()
                self.lbl_inp1.hide()
                self.lbl_inp1.hide()
                self.lbl_operator_1.hide()
                self.inp_power_y.hide()
                self.lbl_inp2.show()
                self.inp_power_y1.hide()
            else:
                self.lbl_inp1.show()
                self.lbl_operator_1.show()
                self.lbl_inp2.show()
                self.inp_power_y1.hide()
        else:
            # print("Vertical ui is off")
            if operator == "x2" or operator == "x3":
                self.inp_1.hide()
                self.lbl_operator.hide()
                self.inp_2.show()
                self.inp_power_y.show()
                self.lbl_operator_1.hide()
                self.inp_power_y1.hide()
                self.lbl_inp1.hide()
                self.lbl_inp2.hide()
            elif operator == "sqrt":
                self.inp_1.hide()
                self.lbl_operator.hide()
                self.inp_2.show()
                self.inp_power_y.hide()
                self.lbl_operator_1.hide()
                self.inp_power_y1.hide()
                self.lbl_inp1.hide()
                self.lbl_inp2.hide()
            else:
                self.inp_1.show()
                self.inp_2.show()
                self.lbl_operator.show()
                self.inp_power_y.hide()
                self.lbl_inp1.hide()
                self.lbl_inp2.hide()
                self.lbl_operator_1.hide()

        # Default ui's
        self.inp_result.show()
        self.lbl_equal.show()

    def hide_controls(self, operator=None):
        """
        Hides controls
        """
        # print("Vertical ui is on")
        self.inp_1.hide()
        self.inp_2.hide()
        self.lbl_operator.hide()
        self.lbl_inp1.hide()
        self.lbl_inp2.hide()
        self.lbl_operator_1.hide()
        # Default ui's
        self.inp_result.hide()
        self.lbl_equal.hide()
        self.inp_power_y.hide()
        self.inp_power_y1.hide()

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

    def start_testing(self):
        """
        Method to start the test
        """
        if len(self.operator_list) == 0:
            # print("Throw error to select at least one operator")
            QMessageBox.critical(self, "No operator is chosen !!!", "Chose at least one operator")
        else:
            self.lbl_ans_status.hide()
            self.lock_ui()
            # local vertical display
            self.chk_vertical.setEnabled(False)
            # self.show_controls()
            self.timer.start(1000)
            self.stop_image()
            self.enable_user_input()
            self.count = self.dial_delay.value()
            self.lbl_timer.setText(str(self.count))
            self.start = True
            # print("Test in progress...")

            # Generate x and y parameters
            x = self.get_random(self.slider_min, self.slider_position)
            y = self.get_random(self.slider_min, self.slider_position)
            operator = self.operator_dict[random.choice(self.operator_list)]

            # Based on the operator show and hide controls
            self.show_controls(operator=operator, vertical_control=self.chk_vertical.isChecked())

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

            if operator == "x2":
                # print("Executing square")
                self.inp_1.setText(str(x))
                self.inp_2.setText(str(y))
                self.lbl_operator.setText("x2")
                self.inp_power_y.setText("2")
            elif operator == "x3":
                # print("Executing cube")
                self.inp_1.setText(str(x))
                self.inp_2.setText(str(y))
                self.lbl_operator.setText("x3")
                self.inp_power_y.setText("3")
            elif operator == "sqrt":
                self.lbl_operator.setText("sqrt")
                self.inp_1.setText(str(x))
                self.inp_2.setText(f"√{x}")
                self.inp_power_y.setText(str(x))
            else:
                self.inp_1.setText(str(x))
                self.lbl_operator.setText(operator)
                self.inp_2.setText(str(y))

    def validate_result(self):
        operator = self.lbl_operator.text()

        if self.inp_result.text() == "":
            result = 0
        else:
            if operator == "sqrt":
                result = float(self.inp_result.text())
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


        if operator == "x2" or operator == "x3":
            x = int(self.inp_1.text())
            y = int(self.inp_2.text())
        elif operator == "sqrt":
            x = int(self.inp_power_y.text())
            y = int(self.inp_power_y.text())
        else:
            x = int(self.inp_1.text())
            y = int(self.inp_2.text())

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
        elif operator == "x2":
            correct_ans = y * y
            result_status = (result == correct_ans)
        elif operator == "x3":
            correct_ans = y * y * y
            result_status = (result == correct_ans)
        elif operator == "sqrt":
            correct_ans = round(math.sqrt(x), 2)
            result_status = (result == correct_ans)

        # print(f"{result_status} {x} {operator} {y} = {result}")
        if result_status:
            self.total_correct += 1
            self.display_image(result_status)
            self.lbl_ans_status.setStyleSheet("background-color : green")
            self.lbl_ans_status.setText("Correct Answer !!!")
        else:
            self.total_wrong += 1
            if operator == "x2":
                tmp = f"{y} x {y}"
            if operator == "x3":
                tmp = f"{y} x {y} x {y}"

            if operator == "x2" or operator == "x3":
                self.txt_errors.appendPlainText(f"(Q-{self.total_questions}) {tmp} = {correct_ans}  You entered: {result}\n-------------------------------------")
            elif operator == "sqrt":
                self.txt_errors.appendPlainText(f"(Q-{self.total_questions}) √{x} = {correct_ans}  You entered: {result}\n-------------------------------------")
            else:
                self.txt_errors.appendPlainText(f"(Q-{self.total_questions}) {x} {operator} {y} = {correct_ans}  You entered: {result}\n-------------------------------------")

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
            self.inp_power_y.clear()
            self.hide_controls(operator=operator)
            self.txt_errors.appendPlainText("Wrong answers\n")
        else:
            self.btn_start.setText("Next Question")
            self.hide_controls(operator=operator)
        # local vertical display
        self.chk_vertical.setEnabled(True)

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
        self.parent.answer_response_time = []
        self.parent.question_index = []


app = QApplication([])
win = MainWindow()
win.show()
app.exec()
