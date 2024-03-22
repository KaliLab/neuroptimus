import sys
from traceHandler import sizeError
try:
    import matplotlib
    matplotlib.use("Qt5Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
except RuntimeError as re:
    print(re)
    sys.exit()
import os
from copy import copy
import Core
import numpy
import os.path
from functools import partial
import re
import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QToolTip, QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog , QTableWidgetItem , QSizePolicy , QVBoxLayout, QGroupBox
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread, pyqtSignal
import warnings
warnings.simplefilter("ignore", UserWarning)

class FittingThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        try:
            # Call the runsim method
            self.parent().runsim()

            # Emit the finished signal
            self.finished.emit()
        except Exception as e:
            # Emit the error signal with the error message
            self.error.emit(str(e))


def popup(message):
    """
    Implements modal message dialog from the PyQT package.

    :param message: the string displayed in the window 
    """
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(message)
    msg.setInformativeText("")
    msg.setWindowTitle("Warning")
    msg.exec()





class Ui_Neuroptimus(QMainWindow):
    def __init__(self,*args):
        super().__init__(*args)


    def setupUi(self, Neuroptimus):
        """
        Implements the widgets from the PyQT package.
        """
        

       
        

        Neuroptimus.setObjectName("Neuroptimus")
        Neuroptimus.resize(800, 589)
        Neuroptimus.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # setting the minimum to be suitable to the device screen, by getting the screen size and setting the minimum to be 50% of it
        WINDOW2SCREEN_RATIO = 0.5
        # screen = QtWidgets.QDesktopWidget().screenGeometry()
        # Neuroptimus.setMinimumSize(QtCore.QSize(screen.width() * WINDOW2SCREEN_RATIO, screen.height() * WINDOW2SCREEN_RATIO))
        




        self.centralwidget = QtWidgets.QWidget(Neuroptimus)
        self.centralwidget.setObjectName("centralwidget")
        Neuroptimus.setCentralWidget(self.centralwidget)

        self.laybox = QtWidgets.QVBoxLayout(self.centralwidget)
        self.laybox.setContentsMargins(0, 0, 0, 0)
        self.laybox.setSpacing(0)

        self.tabwidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabwidget.setObjectName("tabwidget")
        self.tabwidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.laybox.addWidget(self.tabwidget)

        # filetab 1
        self.filetab = QtWidgets.QWidget()
        self.filetab.setObjectName("filetab")

        self.intvalidator = QIntValidator()
        self.doublevalidator = QDoubleValidator()

        self.size_ctrl = QtWidgets.QLineEdit(self.filetab)
        self.size_ctrl.setObjectName("size_ctrl")
        self.size_ctrl.setValidator(self.intvalidator)

        self.length_ctrl = QtWidgets.QLineEdit(self.filetab)
        self.length_ctrl.setObjectName("length_ctrl")
        self.length_ctrl.setValidator(self.doublevalidator)

        self.freq_ctrl = QtWidgets.QLineEdit(self.filetab)
        self.freq_ctrl.setObjectName("freq_ctrl")
        self.freq_ctrl.setValidator(self.doublevalidator)

        self.label_3 = QtWidgets.QLabel(self.filetab)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.filetab)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.filetab)
        self.label_5.setObjectName("label_5")

        self.label_7 = QtWidgets.QLabel(self.filetab)
        self.label_7.setObjectName("label_7")

        self.pushButton_3 = QtWidgets.QPushButton(self.filetab)
        self.pushButton_3.setObjectName("pushButton_3")

        self.label_2 = QtWidgets.QLabel(self.filetab)
        self.label_2.setObjectName("label_2")

        self.base_dir_controll = QtWidgets.QPushButton(self.filetab)
        self.base_dir_controll.setObjectName("base_dir_controll")

        self.label_6 = QtWidgets.QLabel(self.filetab)
        self.label_6.setObjectName("label_6")

        self.lineEdit_folder = QtWidgets.QLineEdit(self.filetab)
        self.lineEdit_folder.setObjectName("lineEdit_2")

        self.type_selector = QtWidgets.QComboBox(self.filetab)
        self.type_selector.setObjectName("type_selector")
        self.type_selector.addItem("")
        self.type_selector.addItem("")
        self.type_selector.addItem("")
        self.type_selector.addItem("")

        self.input_file_controll = QtWidgets.QPushButton(self.filetab)
        self.input_file_controll.setObjectName("pushButton")

        self.time_checker = QtWidgets.QCheckBox(self.filetab)
        self.time_checker.setObjectName("time_checker")

        self.dropdown = QtWidgets.QComboBox(self.filetab)
        self.dropdown.setObjectName("dropdown")
        self.dropdown.addItem("uV")
        self.dropdown.addItem("mV")
        self.dropdown.addItem("V")

        self.lineEdit_file = QtWidgets.QLineEdit(self.filetab)
        self.lineEdit_file.setObjectName("lineEdit")

        self.model = QStandardItemModel(0, 1)

        self.widget = QtWidgets.QWidget(self.filetab)
        self.widget.setObjectName("widget")

        self.input_tree = QtWidgets.QScrollArea(self.filetab)
        self.input_tree.setObjectName("input_tree")

        self.input_label = QtWidgets.QLabel(self.filetab)
        self.input_label.setObjectName("input_label")

        # Use a QGridLayout to arrange the widgets in a grid
        self.layout = QtWidgets.QGridLayout(self.filetab)
        #create new widget Qlabel name it  input_type_label at 0 ,0 
        self.input_type_label = QtWidgets.QLabel(self.filetab)
        self.input_type_label.setObjectName("input_type_label")
        self.input_type_label.setText("Input Type")


        self.layout.addWidget(self.input_type_label, 0, 0, 1, 1)
        self.layout.addWidget(self.type_selector, 0, 1, 1, 1)


        self.layout.addWidget(self.label_2, 1, 0, 1, 1)
        self.layout.addWidget(self.lineEdit_file, 1, 1, 1, 1)
        self.layout.addWidget(self.input_file_controll, 1, 2, 1, 1)
        self.layout.addWidget(self.time_checker, 1, 3, 1, 1)

        self.layout.addWidget(self.label_3, 2, 0, 1, 1) #Base Directory
        self.layout.addWidget(self.lineEdit_folder, 2, 1, 1, 2)
        self.layout.addWidget(self.base_dir_controll, 2, 3, 1, 1)



        self.layout.addWidget(self.label_5, 3, 0, 1, 1) #n of traces label
        self.layout.addWidget(self.size_ctrl, 3, 1, 1, 1) #n of traces input
        self.layout.addWidget(self.label_7, 3, 2, 1, 1,QtCore.Qt.AlignHCenter ) #units label, align center
        
        self.layout.addWidget(self.dropdown, 3, 3, 1, 1) #units dropdown



        self.layout.addWidget(self.label_4, 4, 0, 1, 1)
        self.layout.addWidget(self.length_ctrl, 4, 1, 1, 1)
        self.layout.addWidget(self.label_6, 4, 2, 1, 1)
        self.layout.addWidget(self.freq_ctrl, 4, 3, 1, 1)


        self.layout.addWidget(self.pushButton_3, 5, 0, 1, 2)
        
        self.layout.addWidget(self.input_tree, 6, 0, 1, 2)
        self.layout.addWidget(self.widget, 6, 2, 1, 2)

        #make all buttons in this tab the same size
        for widget in self.filetab.findChildren(QtWidgets.QPushButton):
            widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.filetab.setLayout(self.layout)

        self.tabwidget.addTab(self.filetab, "File Tab")

        # #model tab 
        self.tabwidget.addTab(self.filetab, "")
        self.modeltab = QtWidgets.QWidget()
        self.modeltab.setObjectName("modeltab")
        self.load_mods_checkbox = QtWidgets.QCheckBox(self.modeltab)
        self.load_mods_checkbox.setGeometry(QtCore.QRect(10, 130, 20, 20))
        self.label_23 = QtWidgets.QLabel(self.modeltab)
        self.label_23.setGeometry(QtCore.QRect(30, 130, 240, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.modeltab)
        self.label_24.setGeometry(QtCore.QRect(10, 80, 180, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.pushButton_12 = QtWidgets.QPushButton(self.modeltab)
        self.pushButton_12.setGeometry(QtCore.QRect(150, 50, 140, 22))
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_13 = QtWidgets.QPushButton(self.modeltab)
        self.pushButton_13.setGeometry(QtCore.QRect(330, 100, 80, 22))
        self.pushButton_13.setObjectName("pushButton_13")
        self.lineEdit_file2 = QtWidgets.QLineEdit(self.modeltab)
        self.lineEdit_file2.setGeometry(QtCore.QRect(10, 100, 221, 22))
        self.lineEdit_file2.setObjectName("lineEdit_file2")
        self.modellist = QtWidgets.QTableWidget(self.modeltab)
        self.modellist.setGeometry(QtCore.QRect(10, 200, 441, 261))
        self.modellist.setObjectName("modellist")
        self.modellist.setToolTip("<p>Select the desired parameters then click the Set button</p>")
        self.pushButton_14 = QtWidgets.QPushButton(self.modeltab)
        self.pushButton_14.setGeometry(QtCore.QRect(240, 150, 80, 22))
        self.pushButton_14.setObjectName("pushButton_14")
        self.pushButton_15 = QtWidgets.QPushButton(self.modeltab)
        self.pushButton_15.setGeometry(QtCore.QRect(240, 100, 80, 22))
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_16 = QtWidgets.QPushButton(self.modeltab)
        self.pushButton_16.setGeometry(QtCore.QRect(460, 200, 111, 22))
        self.pushButton_16.setObjectName("pushButton_16")
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        self.label_26 = QtWidgets.QLabel(self.modeltab)
        self.label_26.setGeometry(QtCore.QRect(10, 80, 300, 16))
        font.setWeight(50)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.modeltab)
        self.label_27.setGeometry(QtCore.QRect(10, 130, 300, 16))
        font.setWeight(50)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_26")
        font.setWeight(75)
        self.dd_type = QtWidgets.QComboBox(self.modeltab)
        self.dd_type.setGeometry(QtCore.QRect(10, 50, 121, 23))
        self.dd_type.setObjectName("dd_type")
        self.dd_type.addItem("Neuron")
        self.dd_type.addItem("External (Python)")
        self.dd_type.addItem("External")
        self.dd_type.currentIndexChanged.connect(self.sim_plat)
        self.dd_type.setToolTip("Simulator type")
        self.lineEdit_folder2 = QtWidgets.QLineEdit(self.modeltab)
        self.lineEdit_folder2.setGeometry(QtCore.QRect(10, 150, 221, 22))
        self.lineEdit_folder2.setObjectName("lineEdit_folder2")
        self.sim_path = QtWidgets.QLineEdit(self.modeltab)
        self.sim_path.setGeometry(QtCore.QRect(10, 100, 301, 22))
        self.sim_path.setObjectName("sim_path")
        self.sim_path.hide()
        self.sim_param = QtWidgets.QLineEdit(self.modeltab)
        self.sim_param.setGeometry(QtCore.QRect(10, 150, 50, 22))
        self.sim_param.setObjectName("sim_param")
        self.sim_param.hide()
        self.setter = QtWidgets.QPushButton(self.modeltab)
        self.setter.setGeometry(QtCore.QRect(460, 250, 80, 22))
        self.setter.setObjectName("setter")
        self.remover = QtWidgets.QPushButton(self.modeltab)
        self.remover.setGeometry(QtCore.QRect(460, 280, 80, 22))
        self.remover.setObjectName("remover")
        self.remover.setEnabled(False)



       

        self.layout = QtWidgets.QGridLayout(self.modeltab)
        
        self.layout.addWidget(self.dd_type, 0, 0, 1, 3) #simulator

        self.layout.addWidget(self.label_24, 1, 0, 1, 1) #label Model file

        self.layout.addWidget(self.lineEdit_file2, 1, 1, 1, 2)
        self.layout.addWidget(self.pushButton_15, 1, 3, 1, 1) #first browse non hidden 
        self.layout.addWidget(self.pushButton_13, 1, 4, 1, 1) #load



       
       
        hbox = QtWidgets.QHBoxLayout()

        # Add the checkbox and label to the layout
        hbox.addWidget(self.load_mods_checkbox, 0, QtCore.Qt.AlignLeft)
        hbox.addWidget(self.label_23, 1, QtCore.Qt.AlignLeft)
        # Set the horizontal stretch factor of the checkbox to 0 and the label to 1
        hbox.setStretch(0, 0)
        hbox.setStretch(1, 1)
        self.layout.addLayout(hbox, 2, 0, 1, 2)



        self.layout.addWidget(self.lineEdit_folder2, 2, 2, 1, 2)
        self.layout.addWidget(self.pushButton_14, 2, 4, 1, 1)

        
        
        self.layout.addWidget(self.modellist, 3, 0, 10, 3)
        self.layout.addWidget(self.pushButton_16, 3, 3, 2, 2) #define function
        self.layout.addWidget(self.sim_param, 5, 2, 1, 1)
        self.layout.addWidget(self.setter, 14, 0, 1, 1)
        self.layout.addWidget(self.remover, 14, 1, 1, 1)

        self.modeltab.setLayout(self.layout)

        self.tabwidget.addTab(self.modeltab, "Model Tab")
        
        for widget in self.modeltab.findChildren(QtWidgets.QPushButton):
            widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)




        #sim tab 3
        self.tabwidget.addTab(self.modeltab, "")
        self.simtab = QtWidgets.QWidget()
        self.simtab.setObjectName("simtab")
        self.param_to_record = QtWidgets.QComboBox((self.simtab))
        self.param_to_record.setGeometry(QtCore.QRect(220, 100, 121, 23))
        self.param_to_record.setObjectName("parameter to record")
        self.label_44 = QtWidgets.QLabel(self.simtab)
        self.label_44.setGeometry(QtCore.QRect(10, 220, 111, 16))
        font.setWeight(50)
        self.label_44.setFont(font)
        self.label_44.setObjectName("label_44")
        self.label_66 = QtWidgets.QLabel(self.simtab)
        self.label_66.setGeometry(QtCore.QRect(420, 80, 200, 16))
        self.label_66.setFont(font)
        self.label_66.setObjectName("label_66")
        self.label_67 = QtWidgets.QLabel(self.simtab)
        self.label_67.setGeometry(QtCore.QRect(420, 130, 200, 16))
        self.label_67.setFont(font)
        self.label_67.setObjectName("label_67")
        self.label_45 = QtWidgets.QLabel(self.simtab)
        self.label_45.setGeometry(QtCore.QRect(10, 320, 200, 16))
        self.label_45.setFont(font)
        self.label_45.setObjectName("label_45")
        self.lineEdit_pos = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_pos.setGeometry(QtCore.QRect(220, 200, 113, 22))
        self.lineEdit_pos.setObjectName("position")
        self.lineEdit_pos.setValidator(self.doublevalidator)
        self.section_stim = QtWidgets.QComboBox(self.simtab)
        self.section_stim.setGeometry(QtCore.QRect(10, 340, 121, 23))
        self.section_stim.setObjectName("section stim")
        self.label_46 = QtWidgets.QLabel(self.simtab)
        self.label_46.setGeometry(QtCore.QRect(10, 270, 200, 16))
        self.label_46.setFont(font)
        self.label_46.setObjectName("label_46")
        self.stimprot = QtWidgets.QComboBox(self.simtab)
        self.stimprot.setGeometry(QtCore.QRect(10, 100, 121, 23))
        self.stimprot.setObjectName("stimprot")
        self.stimulus_type = QtWidgets.QComboBox(self.simtab)
        self.stimulus_type.setGeometry(QtCore.QRect(10, 150, 121, 23))
        self.stimulus_type.setObjectName("stimulus type")
        self.label_71 = QtWidgets.QLabel(self.simtab)
        self.label_71.setGeometry(QtCore.QRect(10, 370, 300, 16))
        self.label_71.setFont(font)
        self.label_71.setObjectName("label_71")
        self.lineEdit_posins = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_posins.setGeometry(QtCore.QRect(10, 390, 113, 22))
        self.lineEdit_posins.setObjectName("posinside")
        self.lineEdit_posins.setValidator(self.doublevalidator)
        self.lineEdit_duration = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_duration.setGeometry(QtCore.QRect(10, 290, 113, 22))
        self.lineEdit_duration.setObjectName("duration")
        self.lineEdit_duration.setValidator(self.doublevalidator)
        font.setWeight(75)
        self.base_dir_controll9 = QtWidgets.QPushButton(self.simtab)
        self.base_dir_controll9.setGeometry(QtCore.QRect(10, 180, 115, 22))
        self.base_dir_controll9.setObjectName("base_dir_controll9")
        self.label_48 = QtWidgets.QLabel(self.simtab)
        self.label_48.setGeometry(QtCore.QRect(220, 130, 200, 16))
        font.setWeight(50)
        self.label_48.setFont(font)
        self.label_48.setObjectName("label_48")
        self.lineEdit_tstop = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_tstop.setGeometry(QtCore.QRect(420, 150, 113, 22))
        self.lineEdit_tstop.setObjectName("tstop")
        self.lineEdit_tstop.setValidator(self.doublevalidator)
        self.label_49 = QtWidgets.QLabel(self.simtab)
        self.label_49.setGeometry(QtCore.QRect(10, 130, 200, 16))
        self.label_49.setFont(font)
        self.label_49.setObjectName("label_49")
        self.label_68 = QtWidgets.QLabel(self.simtab)
        self.label_68.setGeometry(QtCore.QRect(420, 180, 200, 16))
        self.label_68.setFont(font)
        self.label_68.setObjectName("label_68")
        font.setWeight(75)
        self.lineEdit_delay = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_delay.setGeometry(QtCore.QRect(10, 240, 113, 22))
        self.lineEdit_delay.setObjectName("Delay")
        self.lineEdit_delay.setValidator(self.doublevalidator)
        self.label_51 = QtWidgets.QLabel(self.simtab)
        self.label_51.setGeometry(QtCore.QRect(220, 180, 200, 16))
        font.setWeight(50)
        self.label_51.setFont(font)
        self.label_51.setObjectName("label_51")
        self.label_52 = QtWidgets.QLabel(self.simtab)
        self.label_52.setGeometry(QtCore.QRect(220, 80, 200, 16))
        self.label_52.setFont(font)
        self.label_52.setObjectName("label_52")
        self.lineEdit_dt = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_dt.setGeometry(QtCore.QRect(420, 200, 113, 22))
        self.lineEdit_dt.setObjectName("lineEdit_dt")
        self.lineEdit_dt.setValidator(self.doublevalidator)
        self.section_rec = QtWidgets.QComboBox(self.simtab)
        self.section_rec.setGeometry(QtCore.QRect(220, 150, 121, 23))
        self.section_rec.setObjectName("section")
        self.lineEdit_initv = QtWidgets.QLineEdit(self.simtab)
        self.lineEdit_initv.setGeometry(QtCore.QRect(420, 100, 113, 22))
        self.lineEdit_initv.setObjectName("initv")
        self.lineEdit_initv.setValidator(self.doublevalidator)
        self.label_55 = QtWidgets.QLabel(self.simtab)
        self.label_55.setGeometry(QtCore.QRect(10, 80, 200, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_55.setFont(font)
        self.label_55.setObjectName("label_55")
        
       


        # Create a new QGridLayout layout
        grid = QtWidgets.QGridLayout(self.simtab)

        # Create a group box for the stimulus protocol widgets
        stim_group = QtWidgets.QGroupBox("Stimulus Mode")
        stim_layout = QtWidgets.QVBoxLayout()
        stim_layout.addWidget(self.label_55) #stim protocol
        stim_layout.addWidget(self.stimprot)
        stim_layout.addWidget(self.label_49) #stim type
        stim_layout.addWidget(self.stimulus_type) 
        stim_layout.addWidget(self.base_dir_controll9) #amplitude(s) push button
        stim_group.setLayout(stim_layout)

        # Add the stimulus protocol group box to the grid layout
        grid.addWidget(stim_group, 0, 0, 5, 1)

       
        # Create a group box for the delay and duration widgets
        time_group = QtWidgets.QGroupBox("Stimulation Time Settings")
        time_layout = QtWidgets.QVBoxLayout()
        time_layout.addWidget(self.label_44)
        time_layout.addWidget(self.lineEdit_delay)
        time_layout.addWidget(self.label_46)
        time_layout.addWidget(self.lineEdit_duration)
        time_group.setLayout(time_layout)

        # Add the time group box to the grid layout
        grid.addWidget(time_group, 5, 0, 4, 1)

        # Create a group box for the section and position widgets
        pos_group = QtWidgets.QGroupBox("Stimulus Position Configuration")
        pos_layout = QtWidgets.QVBoxLayout()
        pos_layout.addWidget(self.label_45)
        pos_layout.addWidget(self.section_stim)
        pos_layout.addWidget(self.label_71)
        pos_layout.addWidget(self.lineEdit_posins)
        pos_group.setLayout(pos_layout)

        # Add the position group box to the grid layout
        grid.addWidget(pos_group, 9, 0, 4, 1)

        # Create a group box for the recording widgets
        rec_group = QtWidgets.QGroupBox("Recording Settings")
        rec_layout = QtWidgets.QVBoxLayout()
        rec_layout.addWidget(self.label_52)
        rec_layout.addWidget(self.param_to_record)
        rec_layout.addWidget(self.label_48)
        rec_layout.addWidget(self.section_rec)
        rec_layout.addWidget(self.label_51)
        rec_layout.addWidget(self.lineEdit_pos)
        rec_group.setLayout(rec_layout)

        # Add the recording group box to the grid layout
        grid.addWidget(rec_group, 0, 1, 6, 1)

        # Create a group box for the initv, tstop, and time step widgets
        sim_group = QtWidgets.QGroupBox("Simulation Settings")
        sim_layout = QtWidgets.QVBoxLayout()
        sim_layout.addWidget(self.label_66)
        sim_layout.addWidget(self.lineEdit_initv)
        sim_layout.addWidget(self.label_67)
        sim_layout.addWidget(self.lineEdit_tstop)
        sim_layout.addWidget(self.label_68)
        sim_layout.addWidget(self.lineEdit_dt)
        sim_group.setLayout(sim_layout)

        # Add the simulation group box to the grid layout
        grid.addWidget(sim_group, 0, 2, 6, 1)

       

        for widget in self.simtab.findChildren(QtWidgets.QPushButton):
            widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        #setting groupbox titles only to bold centered
        for widget in self.simtab.findChildren(QtWidgets.QGroupBox):
            widget.setAlignment(QtCore.Qt.AlignCenter)
            widget.setStyleSheet("QGroupBox {font-weight: bold;}")
            


        # Set the layout of the widget to the new QGridLayout
        self.simtab.setLayout(grid)
            
        #fit tab 4
        self.tabwidget.addTab(self.simtab, "")
        self.fittab = QtWidgets.QWidget()
        self.fittab.setObjectName("fittab")
        self.label_56 = QtWidgets.QLabel(self.fittab)
        self.label_56.setGeometry(QtCore.QRect(10, 50, 270, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(11)
        font.setWeight(50)
        self.label_56.setFont(font)
        self.label_56.setObjectName("label_56")
        self.fitlist = QtWidgets.QTableWidget(self.fittab)
        # self.fitlist.setGeometry(QtCore.QRect(10, 80, 301, 401))
        self.fitlist.setObjectName("fitlist")
        self.spike_tresh = QtWidgets.QLineEdit(self.fittab)
        self.spike_tresh.setGeometry(QtCore.QRect(370,110, 113, 22))
        self.spike_tresh.setObjectName("spike_tresh")
        self.spike_window = QtWidgets.QLineEdit(self.fittab)
        self.spike_window.setGeometry(QtCore.QRect(370, 210, 113, 22))
        self.spike_window.setObjectName("spike_window")
        self.label_69 = QtWidgets.QLabel(self.fittab)
        self.label_69.setGeometry(QtCore.QRect(330, 90, 300, 16))
        self.spike_tresh.setText("0.0")
        self.spike_window.setText("1.0")
        self.label_69.setFont(font)
        self.label_69.setObjectName("label_69")
        self.label_70 = QtWidgets.QLabel(self.fittab)
        self.label_70.setGeometry(QtCore.QRect(330, 190, 300, 16))
        self.label_70.setFont(font)
        self.label_70.setObjectName("label_70")
        self.pushButton_normalize = QtWidgets.QPushButton(self.fittab)
        self.pushButton_normalize.setGeometry(QtCore.QRect(220, 50, 80, 22))
        self.pushButton_normalize.setObjectName("pushButton_normalize")
        self.pushButton_normalize.setText("Normalize")
        font.setPointSize(13)
        QToolTip.setFont(font)
        """self.fittab_help_icon = QtWidgets.QLabel("?",self.fittab)
        self.fittab_help_icon.setGeometry(350, 260, 30, 30)
        self.fittab_help_icon.setStyleSheet("border: 3px solid grey; border-radius: 15px; background-color: #1E90FF; color: white;")
        self.fittab_help_icon.setFont(font)
        self.fittab_help_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.fittab_help = QtWidgets.QLabel("",self.fittab)
        self.fittab_help.setGeometry(350, 260, 30, 30)"""
        self.pushButton_normalize.setToolTip("<p>Rescale the active fitness weights sum to 1</p>")
        self.fitlist.setToolTip("<p>Fitness functions with 0 weights considered inactive</p>")


        # Create a new QGridLayout
        grid = QtWidgets.QGridLayout(self.fittab)

        grid.addWidget(self.pushButton_normalize, 0, 1)
        grid.addWidget(self.fitlist, 1, 0, 10, 2)
        #make the table widget stretch to fill the available space
        grid.setColumnStretch(0, 1)
        grid.setRowStretch(0, 1)



        # Create a new QGroupBox for the spike detection parameters
        spike_group_box = QtWidgets.QGroupBox("Spike Detection Parameters")
        #make the group panel flat
       

        #set the font to be bold for the group box title
        spike_group_box.setStyleSheet("QGroupBox { font-weight: bold; }")


        # Create a new QGridLayout for the spike detection group box
        spike_group_layout = QtWidgets.QVBoxLayout(spike_group_box)

        # Add the widgets to the spike detection group box
        spike_group_layout.addWidget(self.label_69)
        spike_group_layout.addWidget(self.spike_tresh)
        spike_group_layout.addWidget(self.label_70)
        spike_group_layout.addWidget(self.spike_window)


       
        grid.addWidget(spike_group_box, 1, 5, 4, 2)


        # Set the layout of the spike detection group box
        spike_group_box.setLayout(spike_group_layout)


        self.fittab.setLayout(grid)




        #run tab 5
        self.tabwidget.addTab(self.fittab, "")
        self.runtab = QtWidgets.QWidget()
        self.runtab.setObjectName("runtab")
        self.pushButton_30 = QtWidgets.QPushButton(self.runtab)
        self.pushButton_30.setGeometry(QtCore.QRect(630, 460, 80, 22))
        self.pushButton_30.setObjectName("pushButton_30")
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        # self.pushButton_31 = QtWidgets.QPushButton(self.runtab)
        # self.pushButton_31.setGeometry(QtCore.QRect(110, 460, 111, 22))
        # self.pushButton_31.setObjectName("pushButton_31")
        self.pushButton_33 = QtWidgets.QPushButton(self.runtab)
        self.pushButton_33.setGeometry(QtCore.QRect(500, 460, 111, 22))
        self.pushButton_33.setObjectName("pushButton_33")
        self.pushButton_32 = QtWidgets.QPushButton(self.runtab)
        self.pushButton_32.setGeometry(QtCore.QRect(10, 460, 111, 22))
        self.pushButton_32.setObjectName("pushButton_32")
        self.label_59 = QtWidgets.QLabel(self.runtab)
        self.label_59.setGeometry(QtCore.QRect(10, 70, 200, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_59.setFont(font)
        self.label_59.setObjectName("label_59")

        self.pushButton_Inspyred = QtWidgets.QPushButton(self.runtab)
        self.pushButton_Inspyred.setGeometry(QtCore.QRect(128, 90, 83, 32))
        self.pushButton_Inspyred.setObjectName("Inspyred")
        self.pushButton_Pygmo = QtWidgets.QPushButton(self.runtab)
        self.pushButton_Pygmo.setGeometry(QtCore.QRect(210, 90, 83, 32))
        self.pushButton_Pygmo.setObjectName("Pygmo")
        self.pushButton_Bluepyopt = QtWidgets.QPushButton(self.runtab)
        self.pushButton_Bluepyopt.setGeometry(QtCore.QRect(288, 90, 93, 32))
        self.pushButton_Bluepyopt.setObjectName("Bluepyopt")
        self.pushButton_Scipy = QtWidgets.QPushButton(self.runtab)
        self.pushButton_Scipy.setGeometry(QtCore.QRect(380, 90, 71, 32))
        self.pushButton_Scipy.setObjectName("Scipy")
        self.pushButton_Recom = QtWidgets.QPushButton(self.runtab)
        self.pushButton_Recom.setGeometry(QtCore.QRect(10, 90, 120, 32))
        self.pushButton_Recom.setObjectName("Recommended")

        self.algolist = QtWidgets.QTableWidget(self.runtab)
        self.algolist.setGeometry(QtCore.QRect(10, 120, 441, 321))
        self.algolist.setObjectName("algolist")
        self.algorithm_parameter_list = QtWidgets.QTableWidget(self.runtab)
        self.algorithm_parameter_list.setGeometry(QtCore.QRect(470, 90, 241, 351))
        self.algorithm_parameter_list.setObjectName("algorithm_parameter_list")
        self.label_60 = QtWidgets.QLabel(self.runtab)
        self.label_60.setGeometry(QtCore.QRect(470, 70, 200, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_60.setFont(font)
        self.label_60.setObjectName("label_60")
        self.tabwidget.addTab(self.runtab, "")
        self.results_tab = QtWidgets.QWidget()
        self.results_tab.setObjectName("results_tab")

        grid = QtWidgets.QGridLayout(self.runtab)

        grid.addWidget(self.label_59, 0, 0, 1, 2) #Algorithm label

        # group the push buttons in a tight horizontal group
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.pushButton_Recom)
        button_layout.addWidget(self.pushButton_Inspyred)
        button_layout.addWidget(self.pushButton_Pygmo)
        button_layout.addWidget(self.pushButton_Bluepyopt)
        button_layout.addWidget(self.pushButton_Scipy)

        #setting all the labels in the run tab to bold
        for widget in self.runtab.findChildren(QtWidgets.QLabel):
            font = QtGui.QFont()
            font.setFamily("Ubuntu")
            font.setPointSize(10)
            font.setBold(True)
            widget.setFont(font)



        

        #making the buttons layout very tight
        button_layout.setSpacing(0)
        button_layout.setContentsMargins(0, 0, 0, 0)
    
        grid.addLayout(button_layout, 1, 0, 1, 2)
        
        #make the table widget stretch to fill the available space
        self.algolist.horizontalHeader().setStretchLastSection(True)

        grid.addWidget(self.algolist, 2, 0, 1, 4)

        grid.addWidget(self.label_60,0,2,1,1) #Parameters label
        grid.addWidget(self.algorithm_parameter_list,1,2,2,4)
        self.algorithm_parameter_list.horizontalHeader().setStretchLastSection(True)

        grid.addWidget(self.pushButton_32, 3, 0, 1, 1) #Boundaries
        grid.addWidget(self.pushButton_33, 3, 2, 1, 1) #Evaluate
        grid.addWidget(self.pushButton_30, 3, 3, 1, 1) #Run

        self.pushButton_32.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.pushButton_33.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.pushButton_30.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)


        

        self.runtab.setLayout(grid)


        #plot tab 6
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(75)
        self.label_72 = QtWidgets.QLabel(self.results_tab)
        self.label_72.setGeometry(QtCore.QRect(10, 10, 200, 16))

        self.label_72.setFont(font)
        self.label_72.setObjectName("label_72")
        self.tabwidget.addTab(self.results_tab, "")
        self.plot_widget = QtWidgets.QWidget(self.results_tab)
        self.plot_widget.setGeometry(QtCore.QRect(180, 10, 800, 600))
        self.plot_widget.setObjectName("plot_widget")
        self.pushButton_34 = QtWidgets.QPushButton(self.results_tab)
        self.pushButton_34.setGeometry(QtCore.QRect(30, 400, 121, 22))
        self.pushButton_34.setObjectName("pushButton_34")

        


        self.results_tab_grid = QtWidgets.QGridLayout(self.results_tab)

        grid.addWidget(self.label_72, 0, 0, 1, 1)
        self.label_72.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.results_tab_grid.addWidget(self.pushButton_34, 2, 0, 1, 2)

        self.results_tab_grid.addWidget(self.plot_widget, 0, 4, 4, 3)
        # self.plot_widget.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)

      
        #making pushButton 34 not to stretch and be fixed
        for widget in self.results_tab.findChildren(QtWidgets.QPushButton):
            widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)


       
        self.results_tab.setLayout(self.results_tab_grid)

       




        
        #stat tab 7
        self.stat_tab = QtWidgets.QWidget()
        self.stat_tab.setObjectName("stat_tab")
        self.tabwidget.addTab(self.stat_tab, "")
        self.pushButton_35 = QtWidgets.QPushButton(self.stat_tab)
        self.pushButton_35.setGeometry(QtCore.QRect(30, 400, 111, 22))
        self.pushButton_35.setObjectName("pushButton_34")
        self.pushButton_36 = QtWidgets.QPushButton(self.stat_tab)  
        self.pushButton_36.setGeometry(QtCore.QRect(150, 400, 111, 22))
        self.pushButton_36.setObjectName("pushButton_34")
        self.pushButton_37 = QtWidgets.QPushButton(self.stat_tab)
        self.pushButton_37.setGeometry(QtCore.QRect(300, 400, 111, 22))
        self.pushButton_37.setObjectName("pushButton_34")
        self.label_74 = QtWidgets.QLabel(self.stat_tab)
        self.label_74.setGeometry(QtCore.QRect(10, 50, 200, 16))
        self.label_74.setFont(font)
        self.label_74.setObjectName("label_74")
        self.errorlist = QtWidgets.QTableWidget(self.stat_tab)
        self.errorlist.setGeometry(QtCore.QRect(300, 200, 350, 180))
        self.errorlist.setObjectName("errorlist")
        self.fitstat = QtWidgets.QLabel(self.stat_tab)
        self.fitstat.setGeometry(QtCore.QRect(300, 50,200, 24))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.fitstat.setFont(font)
        self.fitstat.setObjectName("label")
        self.fitstat.setText(QtCore.QCoreApplication.translate("Neuroptimus", 'Fitness statistics'))


        #grid layout
        self.statLayout = QtWidgets.QGridLayout(self.stat_tab)
        # self.statLayout.addWidget(self.label_74, 0, 0, 1, 2)
        # self.statLayout.addWidget(self.pushButton_35, 2, 0, 1, 2)
        # self.statLayout.addWidget(self.fitstat, 0, 1, 1, 1)
        # self.statLayout.addWidget(self.errorlist, 1, 1, 1, 2) 
        # self.statLayout.addWidget(self.pushButton_37, 2, 1, 1, 1)
        
        #making pushButtons 37,35 not to stretch and be fixed
        self.pushButton_37.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.pushButton_35.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        #making all coloumns of the errorlist table widget stretch to fill the available space
        self.errorlist.horizontalHeader().setStretchLastSection(True)




        self.stat_tab.setLayout(self.statLayout)







        Neuroptimus.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Neuroptimus)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 771, 19))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        Neuroptimus.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Neuroptimus)
        self.statusbar.setObjectName("statusbar")
        Neuroptimus.setStatusBar(self.statusbar)
        self.actionunlock = QtWidgets.QAction(Neuroptimus)
        self.actionunlock.setObjectName("actionunlock")
        self.actionexit = QtWidgets.QAction(Neuroptimus)
        self.actionexit.setObjectName("actionexit")
        self.menuMenu.addAction(self.actionunlock)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menuMenu.addAction(self.actionexit)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.retranslateUi(Neuroptimus)
        QtCore.QMetaObject.connectSlotsByName(Neuroptimus)
        self.tabwidget.setCurrentIndex(0)





    def retranslateUi(self, Neuroptimus):
        """
        Set PyQT widgets behaviors and implements functions.
        """
        _translate = QtCore.QCoreApplication.translate
        Neuroptimus.setWindowTitle(_translate("Neuroptimus", "Neuroptimus"))
        #self.tabwidget.currentChanged.connect(self.onChange)
        #modeltab 2 disappearing
        self.actionunlock.triggered.connect(self.unlocktabs)
        self.actionexit.triggered.connect(QApplication.quit)

        self.tabwidget.setTabText(self.tabwidget.indexOf(self.filetab), _translate("Neuroptimus", "Target data"))
        self.label_23.setText(_translate("Neuroptimus", "Load mod files from:"))
        self.label_24.setText(_translate("Neuroptimus", "Model file"))
        self.lineEdit_folder2.setEnabled(False)
        self.pushButton_14.setEnabled(False)
        self.load_mods_checkbox.clicked.connect(self.disable_mod_path)
        self.pushButton_13.setText(_translate("Neuroptimus", "Load"))
        self.pushButton_13.clicked.connect(self.Load2)
        self.pushButton_12.setText(_translate("Neuroptimus", "Load python file"))
        self.pushButton_12.clicked.connect(self.Loadpython)
        self.pushButton_12.hide()
        self.pushButton_14.setText(_translate("Neuroptimus", "Browse...")) 
        self.pushButton_14.clicked.connect(self.openFolderNameDialog2)
        self.pushButton_15.setText(_translate("Neuroptimus", "Browse..."))
        self.pushButton_15.clicked.connect(self.openFileNameDialog2)
        self.pushButton_16.setText(_translate("Neuroptimus", "Define function"))
        self.pushButton_16.clicked.connect(self.UF)
        self.label_26.setText(_translate("Neuroptimus", "Command"))
        self.label_26.hide()
        self.label_27.setText(_translate("Neuroptimus", "Number of parameters"))
        self.label_27.hide()
        self.setter.setText(_translate("Neuroptimus", "Set"))
        self.setter.clicked.connect(self.Set)
        self.remover.setText(_translate("Neuroptimus", "Remove"))
        self.remover.clicked.connect(self.Remove)
        self.modellist.setColumnCount(4)
        self.modellist.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.modellist.setHorizontalHeaderLabels(("Section;Segment;Mechanism;Parameter").split(";"))
        #self.modellist.resizeColumnsToContents()
        self.modellist.horizontalHeader().setStretchLastSection(True)
        self.modellist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.modellist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        self.input_tree.setWidgetResizable(True)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.input_label.setFont(font)
        self.input_label.setObjectName("label")
        self.input_tree.setWidget(self.input_label)


        #filetab 1
        self.datfileName = ""
        self.label_3.setText(_translate("Neuroptimus", "Base directory"))
        self.label_4.setText(_translate("Neuroptimus", "Length of traces (ms)"))
        self.label_5.setText(_translate("Neuroptimus", "Number of traces"))
        self.label_7.setText(_translate("Neuroptimus", "Units"))
        self.pushButton_3.setText(_translate("Neuroptimus", "Load data"))
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.clicked.connect(self.Load)
        self.label_2.setText(_translate("Neuroptimus", "Data file"))
        self.base_dir_controll.setText(_translate("Neuroptimus", "Browse..."))
        self.base_dir_controll.clicked.connect(self.openFolderNameDialog)
        self.label_6.setText(_translate("Neuroptimus", "Sampling frequency (Hz)"))
        self.type_selector.setItemText(0, _translate("Neuroptimus", "Voltage trace"))
        self.type_selector.setItemText(1, _translate("Neuroptimus", "Current trace"))
        self.type_selector.setItemText(2, _translate("Neuroptimus", "Features"))
        self.type_selector.setItemText(3, _translate("Neuroptimus", "Other"))

        self.type_selector.currentTextChanged.connect(self.unitchange)
        self.input_file_controll.setText(_translate("Neuroptimus", "Browse..."))
        self.input_file_controll.clicked.connect(self.openFileNameDialog)
        self.time_checker.setText(_translate("Neuroptimus", "Contains time"))
        self.time_checker.toggled.connect(self.time_calc)
        self.dropdown.setItemText(0, _translate("Neuroptimus", "uV"))
        self.dropdown.setItemText(1, _translate("Neuroptimus", "mV"))
        self.dropdown.setItemText(2, _translate("Neuroptimus", "V"))
        self.dropdown.setCurrentIndex(1)

        self.tvoltage=None
        self.tcurrent=None
        self.tspike_t=None
        self.tother=None
        self.tfeatures=None
    
        #Input data plot
        self.figure = plt.figure(figsize=(4,2.5), dpi=80)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.widget)
        # self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        #add to horizontal layout
        self.hbox = QtWidgets.QHBoxLayout(self.widget)
        self.hbox.addWidget(self.canvas)
        self.widget.setLayout(self.hbox)
        

        
        
        # plot  = MyWidget(parent=self.widget)
        # self.figure = plot.figure
        # self.canvas = plot.canvas
        #enable this later
        self.loaded_input_types=[self.tvoltage ,
                                 self.tcurrent ,
#                                 self.tspike_t ,
#                                 self.tother,
                                  self.tfeatures]
        self.core=Core.coreModul()

        #optiontab 3
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.modeltab), _translate("Neuroptimus", "Model"))
        self.label_44.setText(_translate("Neuroptimus", "Delay (ms)"))
        self.label_66.setText(_translate("Neuroptimus", "Initial voltage (mV)"))
        self.label_67.setText(_translate("Neuroptimus", "tstop (ms)"))
        self.label_45.setText(_translate("Neuroptimus", "Section"))
        self.label_46.setText(_translate("Neuroptimus", "Duration (ms)"))
        self.base_dir_controll9.setText(_translate("Neuroptimus", "Amplitude(s)"))
        self.base_dir_controll9.clicked.connect(self.amplitudes_fun)
        self.label_48.setText(_translate("Neuroptimus", "Section"))
        self.label_49.setText(_translate("Neuroptimus", "Stimulus Type"))
        self.label_68.setText(_translate("Neuroptimus", "Time step"))
        self.label_51.setText(_translate("Neuroptimus", "Position inside section"))
        self.label_52.setText(_translate("Neuroptimus", "Parameter to record"))
        self.label_55.setText(_translate("Neuroptimus", "Stimulation protocol"))
        self.label_71.setText(_translate("Neuroptimus", "Position inside section"))
        self.lineEdit_pos.setText("0.5")
        self.lineEdit_posins.setText("0.5")
        self.lineEdit_initv.setText("-65")
        self.lineEdit_dt.setText("0.05")
        
        self.stimprot.addItems(["IClamp","VClamp"])
        self.stimulus_type.addItems(["Step Protocol","Custom Waveform"])
        self.stimulus_type.currentIndexChanged.connect(self.typeChange)
        self.param_to_record.addItems(["v","i"])
        #self.stimprot.setItemText(0, _translate("Neuroptimus", "IClamp"))
        #self.stimprot.setItemText(1, _translate("Neuroptimus", "VClamp"))
        self.container = []
        self.temp=[]


        #fittab 4
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.simtab), _translate("Neuroptimus", "Settings"))
        self.fitlist.setColumnCount(2)
        #self.fitlist.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        #self.flist.setHorizontalHeaderLabels(("Section;Segment;Mechanism;Parameter").split(";"))
        self.fitlist.resizeColumnsToContents()
        
        #self.fitlist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.fitlist.setHorizontalHeaderLabels(["Fitness functions","Weights"])
        #self.fitlist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.fitlist.setColumnWidth(0,200)
        self.fitlist.setColumnWidth(1,80)
        self.fitlist.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        #self.fitlist.itemSelectionChanged.connect(self.fitselect)
        #self.fitlist.cellClicked.connect(self.fitselect)
        self.fitlist.horizontalHeader().setStretchLastSection(True)
        self.label_69.setText(_translate("Neuroptimus", "Spike detection tresh. (mV)"))
        self.label_70.setText(_translate("Neuroptimus", "Spike window (ms)"))
        self.pushButton_normalize.clicked.connect(self.Fit_normalize)
        #self.fittab_help.clicked.connect(self.help_popup_fit)

        #runtab 5
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.fittab), _translate("Neuroptimus", "Fitness"))
        self.pushButton_30.setText(_translate("Neuroptimus", "Run"))
        self.pushButton_30.clicked.connect(self.startFittingThread)
        # self.pushButton_31.setText(_translate("Neuroptimus", "Starting points"))
        # self.pushButton_31.clicked.connect(self.startingpoints)
        # self.pushButton_31.setEnabled(False)
        self.pushButton_33.setText(_translate("Neuroptimus", "Evaluate"))
        self.pushButton_33.clicked.connect(self.evaluatewindow)
        self.pushButton_33.setToolTip("Evaluate user defined parameter set")
        self.pushButton_32.setText(_translate("Neuroptimus", "Boundaries"))
        self.pushButton_32.clicked.connect(self.boundarywindow)
        self.label_59.setText(_translate("Neuroptimus", "Algorithms"))
        self.label_60.setText(_translate("Neuroptimus", "Parameters"))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.runtab), _translate("Neuroptimus", "Run"))
        
        self.pushButton_Recom.setText(_translate("Neuroptimus", "Recommended"))
        self.pushButton_Recom.clicked.connect(partial(self.packageselect,"Recommended"))
        self.pushButton_Inspyred.setText(_translate("Neuroptimus", "Inspyred"))
        self.pushButton_Inspyred.clicked.connect(partial(self.packageselect,"Inspyred"))
        self.pushButton_Pygmo.setText(_translate("Neuroptimus", "Pygmo"))
        self.pushButton_Pygmo.clicked.connect(partial(self.packageselect,"Pygmo"))
        self.pushButton_Bluepyopt.setText(_translate("Neuroptimus", "Bluepyopt"))
        self.pushButton_Bluepyopt.clicked.connect(partial(self.packageselect,"Bluepyopt"))
        self.pushButton_Scipy.setText(_translate("Neuroptimus", "Scipy"))
        self.pushButton_Scipy.clicked.connect(partial(self.packageselect,"Scipy"))
        self.algolist.setColumnCount(1)
        self.algolist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.algolist.clicked.connect(self.algoselect)
        self.algolist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.algolist.setColumnWidth(0,440)
        self.algolist.setHorizontalHeaderLabels(['Algorithms'])
        self.algorithm_parameter_list.setColumnCount(2)
        self.algorithm_parameter_list.horizontalHeader().setStretchLastSection(True)
        self.algorithm_parameter_list.setHorizontalHeaderLabels(["Option","Value"])
        self.algorithm_parameter_list.cellChanged.connect(self.aspect_changed)
        self.seed = []
        self.resolution=0
        self.Recom=["Classical Evolution Strategy (CES) - Inspyred","Covariance Matrix Adaptation ES (CMAES) - Cmaes", "Covariance Matrix Adaptation ES (CMAES) - Pygmo",
                "Particle Swarm (PSO) - Inspyred","Particle Swarm Gen (PSOG) - Pygmo","Indicator Based (IBEA) - Bluepyopt","L-BFGS-B - Scipy","Random Search"]
        self.Inspyred=["Classical Evolution Strategy (CES) - Inspyred","Particle Swarm (PSO) - Inspyred",
                "Differential Evolution (DE) - Inspyred",
                "Nondominated Sorted GA (NSGA2) - Inspyred","Pareto Archived ES (PAES) - Inspyred",
                "Simulated Annealing (SA) - Inspyred"]
        self.Scipy=["Basinhopping (BH) - Scipy","Nelder-Mead (NM) - Scipy","L-BFGS-B - Scipy"]
        self.Bluepyopt=["Nondominated Sorted GA (NSGA2) - Bluepyopt","Indicator Based (IBEA) - Bluepyopt"]
        self.Pygmo=["Particle Swarm Gen (PSOG) - Pygmo","Nondominated Sorted Particle Swarm (NSPSO) - Pygmo",
                "Nondominated Sorted GA (NSGA2) - Pygmo","Differential Evolution (DE) - Pygmo",
                "Extended Ant Colony (GACO) - Pygmo","Multi-Objective Ant Colony (MACO) - Pygmo","Self-Adaptive DE (SADE) - Pygmo",
                "Particle Swarm (PSO) - Pygmo","Exponential Natural ES (XNES) - Pygmo",
                "Simple Genetic Algorithm (SGA) - Pygmo","Covariance Matrix Adaptation ES (CMAES) - Pygmo",
                "Differential Evolution (DE1220) - Pygmo", "Bee Colony (ABC) - Pygmo","Praxis - Pygmo","Nelder-Mead (NM) - Pygmo"] #"FullGrid - Pygmo","Single Differential Evolution (SDE) - Pygmo"
        self.algos={
            'Recommended':self.Recom,
            'Inspyred': self.Inspyred,
            'Scipy': self.Scipy,
            'Bluepyopt': self.Bluepyopt,
            'Pygmo': self.Pygmo}
        self.algolist.setRowCount(len(self.Recom))
        for index,item in enumerate(self.Recom): 
            self.algolist.setItem(index, 0, QTableWidgetItem(item))  
        
        self.algo_param_dict = {"ker" : "Kernel: number of solutions stored in the solution archive.",
                                "q" : "Convergence speed parameter: this parameter is useful for managing \nthe convergence speed towards the found minima (the smaller the faster).",
                                "oracle" : "Oracle parameter: this is the oracle parameter used in the penalty method.",
                                "acc" : "Accuracy parameter: for maintaining a minimum penalty function's values distances.",
                                "threshold" : "Threshold parameter: when the generations reach the threshold \nthen q is set to 0.01 automatically.",
                                "n_gen_mark" : "Standard deviations convergence speed parameter: this parameters \ndetermines the convergence speed of the standard deviations values.",
                                "impstop" : "Improvement stopping criterion: if a positive integer is assigned here, \nthe algorithm will count the runs without improvements, \nif this number will exceed impstop value, the algorithm will be stopped.",
                                "evalstop" : "Evaluation stopping criterion: same as previous one, but with function evaluations.",
                                "focus" : "Focus parameter: this parameter makes the search for the optimum greedier \nand more focused on local improvements (the higher the greedier). \nIf the value is very high, the search is more focused around the current best solutions.",
                                "memory" : " Memory parameter: if true, memory is activated in the algorithm for multiple calls",
                                "cc"  :  "backward time horizon for the evolution path",
                                "cs"  :  "makes partly up for the small variance loss in case the indicator is zero",
                                "c1"  :  "CMAES: learning rate for the rank-one update of the covariance matrix \nNSPSO: magnitude of the force, applied to the particle's velocity, in the direction of its previous best position.",
                                "cmu"  :  "learning rate for the rank - update of the covariance matrix",
                                "sigma0"  :  "initial step-size",
                                "ftol"  :  "stopping criteria on the x tolerance",
                                "xtol"  :  "stopping criteria on the f tolerance",
                                "memory"  :  "when true the adapted parameters are not reset between successive calls to the evolve method",
                                "force_bounds"  :  "when true the box bounds are enforced. The fitness will never be called outside the bounds but the covariance matrix adaptation mechanism will worsen",
                                "omega"  :  "particles' inertia weight, or alternatively, the constriction coefficient (definition depends on the variant used)",
                                "eta1"  :  "magnitude of the force, applied to the particle's velocity, in the direction of its previous best position",
                                "eta2"  :  "magnitude of the force, applied to the particle's velocity, in the direction of the best position in its neighborhood",
                                "max_vel"  :  "maximum allowed particle velocity (as a fraction of the box bounds)",
                                "variant"  :  "PSO: algorithm variant to use (one of 1 .. 6) \nDE: mutation variant",
                                "neighb_type"  :  "swarm topology to use (one of 1 .. 4) [gbest, lbest, Von Neumann, adaptive random]",
                                "neighb_param"  :  "the neighbourhood parameter. If the lbest topology is selected (neighb_type=2), it represents each particle's indegree (also outdegree) in the swarm topology. Particles have neighbours up to a radius of k = neighb_param / 2 in the ring. If the Randomly-varying neighbourhood topology is selected (neighb_type=4), it represents each particle's maximum outdegree in the swarm topology. The minimum outdegree is 1 (the particle always connects back to itself). If neighb_type is 1 or 3 this parameter is ignored.",
                                "F" : "weight coefficient",
                                "CR" : "crossover probability",
                                "cr" : "crossover probability",
                                "variant_adptv" : "weight coefficient and crossover probability parameter adaptation scheme to be used (one of 1..2)",
                                "c2" : "magnitude of the force, applied to the particle's velocity, in the direction of its global best (i.e., leader).",
                                "chi" : "velocity scaling factor.",
                                "v_coeff" : "velocity coefficient (determining the maximum allowed particle velocity).",
                                "leader_selection_range" : "leader selection range parameter (i.e., the leader of each particle is selected among the best).",
                                "diversity_mechanism" : "the diversity mechanism used to maintain diversity on the Pareto front.",
                                "cr" : "Crossover probability.",
                                "eta_c" : "Distribution index for crossover.",
                                "m" : "Mutation probability.",
                                "eta_m" : "Distribution index for mutation.",
                                "eta_c" : "distribution index for “sbx” crossover. This is an inactive parameter if other types of crossovers are selected.",
                                "m" : "mutation probability.",
                                "param_m" : "distribution index (“polynomial” mutation), gaussian width (“gaussian” mutation) or inactive (“uniform” mutation)",
                                "param_s" : "when “truncated” selection is used this indicates the number of best individuals to use. When “tournament” selection is used this indicates the size of the tournament.",
                                "eta_mu" : "learning rate for mean update ",
                                "eta_sigma" : "learning rate for step-size update",
                                "eta_b" : "learning rate for the covariance matrix update",
                                "fatol"  :  "stopping criteria on the x tolerance",
                                "xatol"  :  "stopping criteria on the f tolerance",
                                "mutpb" : "Mutation probability",
                                "cxpb" : "Crossover probability",
                                "sigma" : "coordinate wise standard deviation (step size)"
                                }


        self.algo_dict=self.core.option_handler.algorithm_parameters_dict.copy()

        self.tabwidget.setTabText(self.tabwidget.indexOf(self.results_tab), _translate("Neuroptimus", "Results"))
        self.label_72.setText(_translate("Neuroptimus", "Final Result"))
        self.figure2, self.results_tab_axes = plt.subplots( dpi=80)
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.setParent(self.plot_widget)
        hbox2 = QtWidgets.QHBoxLayout(self.plot_widget)
        hbox2.addWidget(self.canvas2)
        self.plot_widget.setLayout(hbox2)
       
        self.pushButton_34.setText(_translate("Neuroptimus", "Save Parameters"))
        self.pushButton_34.clicked.connect(self.SaveParam)


        self.tabwidget.setTabText(self.tabwidget.indexOf(self.stat_tab), _translate("Neuroptimus", "Statistics"))
        self.label_74.setText(_translate("Neuroptimus", "Analysis"))
        self.pushButton_35.setText(_translate("Neuroptimus", "Generation Plot"))
        self.pushButton_35.clicked.connect(self.PlotGen)
        self.pushButton_37.setText(_translate("Neuroptimus", "Error Details"))
        self.pushButton_37.clicked.connect(self.ShowErrorDialog)
        self.errorlist.setColumnCount(4)
        self.errorlist.setHorizontalHeaderLabels(["Error Functions","Value","Weight","Weighted Value"])
        self.errorlist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


        self.menuMenu.setTitle(_translate("Neuroptimus", "Menu"))
        self.actionunlock.setText(_translate("Neuroptimus", "Unlock Tabs"))
        self.actionexit.setText(_translate("Neuroptimus", "Exit"))
        self.tabwidget.setTabEnabled(1,False)
        self.tabwidget.setTabEnabled(2,False)
        self.tabwidget.setTabEnabled(3,False)
        self.tabwidget.setTabEnabled(4,False)
        self.tabwidget.setTabEnabled(5,False)
        self.tabwidget.setTabEnabled(6,False)
        self.result_labels = []

        for curr_tab in [self.results_tab,self.stat_tab]:
            label = QtWidgets.QLabel()
            font = QtGui.QFont()
            font.setFamily("Ubuntu")
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            label.setFont(font)
            label.setObjectName("label")
            self.result_labels.append(label)
            scroll_area = QtWidgets.QScrollArea(curr_tab)
            # scroll_area.setGeometry(QtCore.QRect(10, 100, 170, 256))
            scroll_area.setGeometry(QtCore.QRect(10, 100, 300+50, 500))

            scroll_area.setWidget(label)
            scroll_area.setWidgetResizable(True)



            
            if curr_tab is self.results_tab:
                scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.canvas2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.results_tab_grid.addWidget(self.label_72, 0, 0, 1, 2)          
                self.results_tab_grid.addWidget(scroll_area, 1, 0, 1, 2)
                self.results_tab_grid.addWidget(self.plot_widget, 0, 3, 2, 3)

            elif curr_tab is self.stat_tab:
                self.statLayout.addWidget(self.label_74, 0, 0, 1, 2)
                self.statLayout.addWidget(scroll_area,1,0,2,2)
                self.scroll_area2_stat = QtWidgets.QScrollArea(self.stat_tab)
                self.stats_label = QtWidgets.QLabel(self.stat_tab)
                self.stats_label.setGeometry(QtCore.QRect(300, 80, 250, 146))
                font = QtGui.QFont()
                font.setFamily("Ubuntu")
                font.setPointSize(10)
                font.setBold(False)
                font.setWeight(50)
                self.stats_label.setFont(font)
                self.stats_label.setObjectName("label")
                # scroll_area_2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.scroll_area2_stat.setGeometry(QtCore.QRect(300,80, 350, 100))
                self.scroll_area2_stat.setWidgetResizable(True)
                self.statLayout.addWidget(self.pushButton_35, 3, 0, 1, 2)


                self.statLayout.addWidget(self.fitstat, 0, 4, 1, 4) #label
                self.statLayout.addWidget(self.scroll_area2_stat, 1, 4, 1, 2)
                #making a bold label
                font = QtGui.QFont()
                font.setFamily("Ubuntu")
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.fitstat.setFont(font)
                self.statLayout.addWidget(self.errorlist, 2, 4, 1, 4) 
                self.statLayout.addWidget(self.pushButton_37, 3, 4, 1, 1)
                self.errorlist.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.errorlist.horizontalHeader().setStretchLastSection(True)
                # self.statLayout.setColumnStretch(0, 1)
                # self.statLayout.setColumnStretch(1, 2)





    # def startFittingThread(self):
    

    #     # Create a new thread for optimization
    #     optimization_thread = threading.Thread(target=self.runsim)
    #     optimization_thread.start()


    def startFittingThread(self):
        # Create a new thread for optimization
        self.fitting_thread = FittingThread(self)
        # self.fitting_thread.finished.connect(self.on_fitting_finished)
        # self.fitting_thread.error.connect(self.on_fitting_error)

        # Start the thread
        self.fitting_thread.start()    

        
    def help_popup_fit(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText("""Normalize button will adjust active fitness weights sum to 1
        \nFitness functions with 0 values considered as inactive""")
        msg.exec()


    def unlocktabs(self): 
        self.tabwidget.setTabEnabled(1,True)
        self.tabwidget.setTabEnabled(2,True)
        self.tabwidget.setTabEnabled(3,True)
        self.tabwidget.setTabEnabled(4,True)
        self.tabwidget.setTabEnabled(5,True)
        self.tabwidget.setTabEnabled(6,True)

                

    def openFileNameDialog(self): 
        """
        File dialog for the file tab to open file.
        """
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.datfileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Data files (*.dat *.json);;All Files (*);;", options=options)
        if self.datfileName:
            self.lineEdit_file.setText(self.datfileName)
            self.lineEdit_folder.setText(os.path.dirname(os.path.realpath(self.datfileName)))
            self.pushButton_3.setEnabled(True)
            if self.time_checker.isChecked():
                self.time_calc()

    def time_calc(self):
        try:
            with open(str(self.lineEdit_file.text())) as data:
                all_line=data.read().splitlines()
                time_vec=[float(x.split()[0]) for x in all_line]
                self.length_ctrl.setText(str(round(max(time_vec))))
                self.freq_ctrl.setText(str(((len(time_vec)-1)*1000)/(max(time_vec)-min(time_vec))))   #frequency 
                self.size_ctrl.setText(str(len(all_line[0].split())-1))  #trace number
        except:
                print('No data file selected')
            

    def openFolderNameDialog2(self): 
        """
        File dialog for the model tab to open folder.
        """ 
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        folderName= QFileDialog.getExistingDirectory(None, options=options)
        if folderName:
            self.lineEdit_folder2.setText(folderName)

    def openFileNameDialog2(self):  
        """
        File dialog for the model tab to open file.
        """  
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Hoc Files (*.hoc);;All Files (*);;", options=options)
        if fileName:
            self.lineEdit_file2.setText(fileName)
            self.lineEdit_folder2.setText(os.path.dirname(os.path.realpath(fileName)))
            self.pushButton_3.setEnabled(True)

    def openFolderNameDialog(self):
        """
        File dialog for the file tab to open folder.
        """  
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        folderName= QFileDialog.getExistingDirectory(None, options=options)
        if folderName:
            self.lineEdit_folder.setText(folderName)

    def disable_mod_path(self):
        """
        Disables mod files path if checked for usage
        """
        if self.load_mods_checkbox.isChecked():
            self.lineEdit_folder2.setEnabled(True)
            self.pushButton_14.setEnabled(True)
        else:
            self.lineEdit_folder2.setEnabled(False)
            self.pushButton_14.setEnabled(False)


    def unitchange(self):
        """
        Sets units for drop down widget selecting simulation type.
        """
        self.dropdown.clear()
        if self.type_selector.currentIndex()==0:
            self.dropdown.addItems(["uV","mV","V"])
        elif self.type_selector.currentIndex()==1:
            self.dropdown.addItems(["pA","nA","uA"])
        elif self.type_selector.currentIndex()==2:
            self.dropdown.addItems(["uV","mV","V","pA","nA","uA"])
        else:
            self.dropdown.addItems(["none"])
        self.dropdown.setCurrentIndex(1)

        
    def add_data_dict(self,data_dict):
        """
        Creates Input tree *not implemented yet*
        :param data_dict:
        :param root:
        """
        
        stack = data_dict
        string=""
        while stack:
            key, value = stack.popitem()
            if isinstance(value, dict):
                string+=str("{0} : ".format(key))+"\n"
                stack.update(value)
            else:
                string+=str("  {0} : {1}".format(key, value))+"\n"  
        
        
        return string
        

    def Load(self):
        """
        Loads the model after the 'Load Trace' clicked

        First creates a dictionary with the paths and options and call the First step, giving these as argument
        Plots the trace in matplotlib on the file tab.

        """
        if (self.type_selector.currentText() == 'Features'):
            try:

                kwargs = {"file" : str(self.lineEdit_folder.text()),
                        "input" : [str(self.lineEdit_file.text()),
                                   None,
                                   str(self.dropdown.currentText()),
                                   None,
                                   None,
                                   None,
                                   self.type_selector.currentText().split()[0].lower()]}
                
            except ValueError as ve:
                print(ve)

        else:
            try:

                kwargs = {"file" : str(self.lineEdit_folder.text()),
                        "input" : [str(self.lineEdit_file.text()),
                                   int(self.size_ctrl.text()),
                                   str(self.dropdown.currentText()),
                                   float(self.length_ctrl.text()),
                                   float(self.freq_ctrl.text()),
                                   self.time_checker.isChecked(),
                                   self.type_selector.currentText().split()[0].lower()]}
                
            except ValueError as ve:
                print(ve)
        self.core.FirstStep(kwargs)
        self.tabwidget.setTabEnabled(1,True)
        if self.type_selector.currentIndex()==0 or self.type_selector.currentIndex()==1 or self.type_selector.currentIndex()==3:
            
            f = self.core.option_handler.input_freq
            t = self.core.option_handler.input_length
            no_traces=self.core.option_handler.input_size
            _type="voltage" if self.type_selector.currentIndex==0 else "current" if self.type_selector.currentIndex==1 else "unkown"
            exp_data = []
            
            freq=float(self.freq_ctrl.text())
            for k in range(self.core.data_handler.number_of_traces()):
                exp_data.extend(self.core.data_handler.data.GetTrace(k))
            
            self.figure.clf()
            ax = self.figure.add_subplot(111)
            ax.cla()
            if self.time_checker.isChecked():
               ax.plot([x/freq*1000 for x in range(len(exp_data))],exp_data) 
            else:
                ax.plot(exp_data)
            self.canvas.draw()
            
            
            
            for k in range(self.core.data_handler.number_of_traces()):
                exp_data.extend(self.core.data_handler.data.GetTrace(k))
            self.model.insertRow(0)
            if self.type_selector.currentIndex()==0:
                for n in [x for x in enumerate(self.loaded_input_types) if x[1]!=None and x[0]!=2]:
                    self.loaded_input_types[n[0]]=None
                input_string="Voltage trace \n" 
                self.loaded_input_types[0]=self.tvoltage
                
                input_string+=str(str(self.lineEdit_file.text()).split("/")[-1])+"\n"
            elif self.type_selector.currentIndex()==1:
                for n in [x for x in enumerate(self.loaded_input_types) if x[1]!=None and x[0]!=2]:
                    self.loaded_input_types[n[0]]=None
                input_string="Current trace"
                self.loaded_input_types[1]=self.tcurrent
                input_string+=str(str(self.lineEdit_file.text()).split("/")[-1])+"\n"

            '''
            elif self.type_selector.GetSelection()==3:
                try:
                    self.input_tree.Delete(self.tspike_t)
                except ValueError:
                    pass
                self.tspike_t=self.input_tree.AppendItem(self.troot,"Spike times")
                self.input_tree.AppendItem(self.tspike_t,self.input_file_controll.GetValue().split("/")[-1])
                '''

        elif self.type_selector.currentIndex()==2:
            for n in [x for x in enumerate(self.loaded_input_types) if x[1]!=None and x[0]!=2]:
                self.loaded_input_types[n[0]]=None
            input_string="Features"
            input_string+=str(str(self.lineEdit_file.text()).split("/")[-1])+"\n"
            input_string+=self.add_data_dict(self.core.data_handler.features_dict)

        else:
            pass
        
        self.input_label.setText(QtCore.QCoreApplication.translate("Neuroptimus", input_string))
        if self.core.option_handler.type[-1]!="features":
                self.my_list = copy(self.core.ffun_calc_list)
               
        else:
            self.my_list=list(self.core.data_handler.features_data.keys())[3:]
        self.param_list = [[]] * len(self.my_list)
        if self.core.option_handler.type[-1]!="features":
            self.param_list[2] = [("Spike detection thres. (mV)",0.0)]
            self.param_list[1] = [("Spike detection thres. (mV)",0.0), ("Spike Window (ms)",1.0)]
        else:
            self.param_list[0] = [("Spike detection thres. (mV)",0.0)]

        if self.core.option_handler.type[-1]=="features":
            for l in range(len(self.core.data_handler.features_data["stim_amp"])):
                self.container.append(float(self.core.data_handler.features_data["stim_amp"][l]))

        self.fitlist.setRowCount(len(self.my_list))
        for index,elems in enumerate(self.my_list):  
            item = QTableWidgetItem(elems)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )      
            self.fitlist.setItem(index, 0, item)
            if self.core.option_handler.type[-1]=="features":
                itemv = QTableWidgetItem(str(self.core.data_handler.features_data[self.my_list[index]]["weight"]))
            else:
                itemv = QTableWidgetItem("0")
            self.fitlist.setItem(index, 1, itemv)

        if self.core.option_handler.type[-1]!="features":
            self.kwargs={"runparam" : [self.core.data_handler.data.t_length,
                                        self.core.data_handler.data.step,
                                        "record",
                                        "soma",
                                        "pos",
                                        "vrest"]
                            }
        else:
            self.kwargs={"runparam" : [self.core.data_handler.features_data["stim_delay"] + self.core.data_handler.features_data["stim_duration"]+100,
                                        0.05,
                                        "record",
                                        "soma",
                                        "pos",
                                        "vrest"]}
        if self.core.option_handler.output_level=="1":
            self.core.Print()
        self.fit_container=[]
        if self.core.option_handler.type[-1]!="features":
            self.lineEdit_tstop.setText(str(self.core.data_handler.data.t_length))
        else:
            self.lineEdit_tstop.setText(str(self.core.data_handler.features_data["stim_delay"] + self.core.data_handler.features_data["stim_duration"]+100))
            self.lineEdit_delay.setText(str(self.core.data_handler.features_data["stim_delay"]))
            self.lineEdit_duration.setText(str(self.core.data_handler.features_data["stim_duration"]))    


        
        
        
    def Set(self, e):
        """
        Set the selected parameters to optimize on the model.

        Loop through every selected line.
        """
        items = self.modellist.selectionModel().selectedRows()
        self.remover.setEnabled(True)
        for item_selected in items:
                selected_row=item_selected.row()
                section = str(self.modellist.item(selected_row, 0).text())
                segment = str(self.modellist.item(selected_row, 1).text())
                chan = str(self.modellist.item(selected_row, 2).text())
                morph=""
                par = str(self.modellist.item(selected_row, 3).text())
                if chan == "morphology":
                    chan = "None"
                    par= "None"
                    morph = str(self.modellist.item(selected_row, 3).text())



                kwargs = {"section" : section,
                        "segment" : segment,
                        "channel" : chan,
                        "morph" : morph,
                        "params" : par,
                        "values" : 0}

      
                for j in range(4):
                    self.modellist.item(selected_row,j).setBackground(QtGui.QColor(255,0,0))


                self.core.SetModel2(kwargs)
                
            

    def Remove(self, e):
        """
        Remove the selected parameters to optimize on the model.
        Loop through every selected line.
        """
        items = self.modellist.selectionModel().selectedRows()
        for item_selected in items:
                selected_row=item_selected.row()
                section = str(self.modellist.item(selected_row, 0).text())
                segment = str(self.modellist.item(selected_row, 1).text())
                chan = str(self.modellist.item(selected_row, 2).text())
                morph=""
                par = str(self.modellist.item(selected_row, 3).text())
                if chan == "morphology":
                    chan = "None"
                    par= "None"
                    morph = str(self.modellist.item(selected_row, 3).text())

                kwargs = {"section" : section,
                        "segment" : segment,
                        "channel" : chan,
                        "morph" : morph,
                        "params" : par}

                if kwargs["channel"] == "None":
                    temp = kwargs["section"] + " " + kwargs["morph"]
                else:
                    temp = kwargs["section"] + " " + kwargs["segment"] +  " " + kwargs["channel"] + " " + kwargs["params"]
                self.core.option_handler.param_vals.pop(self.core.option_handler.GetObjTOOpt().index(temp))
                self.core.option_handler.adjusted_params.remove(temp)
                if len(self.core.option_handler.GetObjTOOpt()) == 0:
                    self.remover.setEnabled(False )
                for j in range(4):
                    self.modellist.item(selected_row,j).setBackground(QtGui.QColor(255,255,255))



    def sim_plat(self):
        """
        Called when simulation platform changed, locks unnecessary widgets and swap Label of Load button.
        """
        if self.dd_type.currentIndex()==1:
            self.sim_path.show()
            self.sim_param.show()
            self.pushButton_13.setText(QtCore.QCoreApplication.translate("Neuroptimus", "Set"))
            self.pushButton_12.show()
            self.pushButton_14.hide()
            self.pushButton_15.hide()
            self.pushButton_16.hide()
            self.setter.hide()
            self.remover.hide()
            self.modellist.hide()
            self.lineEdit_file2.hide()
            self.lineEdit_folder2.hide()
            self.label_23.hide()
            self.label_24.hide()
            self.label_26.show()
            self.label_27.show()
            self.load_mods_checkbox.hide()
        elif self.dd_type.currentIndex()==2:        
            self.sim_path.show()
            self.sim_param.show()
            self.pushButton_13.setText(QtCore.QCoreApplication.translate("Neuroptimus", "Set"))
            self.pushButton_12.hide()
            self.pushButton_14.hide()
            self.pushButton_15.hide()
            self.pushButton_16.hide()
            self.setter.hide()
            self.remover.hide()
            self.modellist.hide()
            self.lineEdit_file2.hide()
            self.lineEdit_folder2.hide()
            self.label_23.hide()
            self.label_24.hide()
            self.label_26.show()
            self.label_27.show()
            self.load_mods_checkbox.hide()
        else:
            self.pushButton_13.setText(QtCore.QCoreApplication.translate("Neuroptimus", "Load"))
            self.sim_path.hide()
            self.sim_param.hide()
            self.pushButton_12.hide()
            self.pushButton_14.show()
            self.pushButton_15.show()
            self.pushButton_16.show()
            self.setter.show()
            self.remover.show()
            self.modellist.show()
            self.lineEdit_file2.show()
            self.lineEdit_folder2.show()
            self.label_23.show()
            self.label_24.show()
            self.label_26.hide()
            self.label_27.hide()
            self.load_mods_checkbox.show()

    def Loadpython(self, e):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Python files (*.py);;All Files (*);;", options=options)
        if fileName:
            self.sim_path.setText("python "+str(fileName))


    def Load2(self, e):
        """
        Load the selected Neuron model and displays the sections in a tablewidget
        """
        self.model_file = self.lineEdit_file2.text()
        self.tabwidget.setTabEnabled(2,True)
        self.tabwidget.setTabEnabled(3,True)
        self.tabwidget.setTabEnabled(4,True)
        if self.load_mods_checkbox.isChecked():
            self.spec_file = self.lineEdit_folder2.text()
        else:
            self.spec_file = None

        try:
            self.core.LoadModel({"model" : [self.model_file, self.spec_file],
                                 "simulator" : self.dd_type.currentText(),
                                 "sim_command" : self.sim_path.text() if not self.dd_type else self.sim_path.text()+" "+self.sim_param.text()})
            temp = self.core.model_handler.GetParameters()
            if temp!=None:
                with open("model.txt", 'w+') as out:
                    for i in temp:
                        out.write(str(i))
                        out.write("\n")
                    index=0
                self.modellist.setRowCount(self.recursive_len(temp))
                for row in temp:
                    for k in (row[1]):
                        if k != []:
                            for s in (k[2]):
                                self.modellist.setItem(index, 0, QTableWidgetItem(row[0]))
                                self.modellist.setItem(index, 1, QTableWidgetItem(str(k[0])))
                                self.modellist.setItem(index, 2, QTableWidgetItem(k[1]))
                                self.modellist.setItem(index, 3, QTableWidgetItem(s))
                                index+=1
                self.modellist.setRowCount(index)
            else:
                pass

        except OSError as oe:
            print(oe)
        if not self.dd_type.currentIndex():  
            try:
                tmp=self.core.ReturnSections()
                [tmp.remove("None") for i in range(tmp.count("None"))]
                self.section_rec.addItems(tmp)
                self.section_stim.addItems(tmp)
                if "soma" in tmp:
                    self.section_rec.setCurrentText("soma")
                    self.section_stim.setCurrentText("soma")
            except:
                popup("Section error")

    def typeChange(self):
        _translate = QtCore.QCoreApplication.translate
        if self.stimulus_type.currentIndex()==0:#step prot
            self.lineEdit_delay.setDisabled(False)
            self.lineEdit_duration.setDisabled(False)
            self.base_dir_controll9.clicked.disconnect(self.openFileNameDialogWaveform)
            self.base_dir_controll9.clicked.connect(self.amplitudes_fun)
            self.base_dir_controll9.setText(_translate("Neuroptimus", "Amplitude(s)"))
        if self.stimulus_type.currentIndex()==1:#wave prot
            self.lineEdit_delay.setDisabled(True)
            self.lineEdit_delay.setText("0")
            self.lineEdit_duration.setDisabled(True)
            self.lineEdit_duration.setText("1e9")
            self.base_dir_controll9.setText(_translate("Neuroptimus", "Load Waveform"))
            self.base_dir_controll9.clicked.disconnect(self.amplitudes_fun)
            self.base_dir_controll9.clicked.connect(self.openFileNameDialogWaveform)

    def openFileNameDialogWaveform(self): 
        """
        File dialog for the file tab to open file.
        """
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Data files (*.dat *.json);;All Files (*);;", options=options)
        if fileName:
            self.container=[fileName]
               


    def recursive_len(self,item):
        if type(item) == list:
            return sum(self.recursive_len(subitem) for subitem in item)
        else:
            return 1


    def UF(self):
        """
        Calls the user function window for the Model tab.
        """

        self.SW = SecondWindow(self) 
        self.SW.setObjectName("Neuroptimus")
        self.SW.resize(500, 500)
        self.SW.show()

    def amplitudes_fun(self):
        """
        Calls the amplitude window for the Options tab.
        """

        self.SiW = StimuliWindow(self) 
        self.SiW.setObjectName("Neuroptimus")
        self.SiW.resize(400, 500)
        self.SiW.show()

    
    def fitselect(self):
        """
        Calls when fitness functions selected, colours the item and adds them to a set.
        """
        items = self.fitlist.selectionModel().selectedIndexes()
        for item_selected in items:
            if item_selected.column()==0:
                current_item=str(self.fitlist.item(item_selected.row(), 0).text())
                if current_item in self.fitset:
                    self.fitlist.item(item_selected.row(),0).setBackground(QtGui.QColor(255,255,255))
                    self.fitset.remove(current_item)
                else:
                    self.fitlist.item(item_selected.row(),0).setBackground(QtGui.QColor(0,255,0))
                    self.fitset.add(current_item)


    def fitchanged(self):
        """
        Calls when the weights changed for the fitness functions. Stores the weights in a list.
        """
        self.weights=[]
        try:
            allRows = self.fitlist.rowCount()
            for row in range(0,allRows):
                current_fun=str(self.fitlist.item(row, 0).text())
                current_weight=float(self.fitlist.item(row, 1).text())
                if current_weight:
                    self.weights.append(current_weight) 
        except:
            self.fitlist.item(row, 1).setText("0")
        

    def Fit_normalize(self, e):
        """
        Normalize the weigths of only the selected fitness functions.
        Iterates through all fitness functions and scans the ones contained in the fitness set (selected ones) with an 'if' statement.
        """
        try:
            #self.fitselect()
            #self.fitchanged()
            allRows = self.fitlist.rowCount()
            self.weights=[float(self.fitlist.item(row, 1).text()) for row in range(0,allRows)] 
            sum_o_weights = float(sum(self.weights))
            for row in range(0,allRows):
                current_fun=str(self.fitlist.item(row, 0).text())
                current_weight=float(str(self.fitlist.item(row, 1).text()))
                if current_weight:
                    try:
                        self.fitlist.item(row, 1).setText(str(round(current_weight / sum_o_weights,4)))
                    except:
                        continue
                else:
                    try:
                        self.fitlist.item(row, 1).setText("0")
                    except:
                        continue
        except Exception as e:
            popup("Wrong values given. "+str(e))

    def packageselect(self,pack_name):
            """
            Writes the given aspects to algorithm in an other table, where the user can change the option (generation, population size, etc.).
            Iterates through the selected algorithms options list and writes the names of it to the first column and sets the cell immutable, 
            and the values to the second row.
            """

            selected_package = self.algos.get(pack_name)
            self.algolist.setRowCount(len(selected_package))
            for index,elems in enumerate(selected_package):
                item = QTableWidgetItem(str(elems))   
                self.algolist.setItem(index, 0, item)
            self.algolist.item(0,0)

    def algoselect(self):
        """
        Writes the given aspects to algorithm in an other table, where the user can change the option (generation, population size, etc.).
        Iterates through the selected algorithms options list and writes the names of it to the first column and sets the cell immutable, 
        and the values to the second row.
        """
        try:
            selected_algo = self.algolist.selectionModel().selectedRows()[0].row()
            algo_name = str(self.algolist.item(selected_algo, 0).text()).upper()
            aspects = self.algo_dict[algo_name[algo_name.find("(")+1:].replace(")","").replace(" - ","_").replace("-","_").replace(" ","_")]
            self.algorithm_parameter_list.setRowCount(len(aspects)+1)
            item = QTableWidgetItem('Seed')
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )      
            self.algorithm_parameter_list.setItem(0, 0, item)
            item2 = QTableWidgetItem('1234')   
            self.algorithm_parameter_list.setItem(0, 1, item2)
            for index, (key, value) in enumerate(aspects.items()):
                item = QTableWidgetItem(key)
                if self.algo_param_dict.get(key):
                    item.setToolTip(str(self.algo_param_dict.get(key)).rjust(30))
                item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )      
                self.algorithm_parameter_list.setItem(index+1, 0, item)     
                item2 = QTableWidgetItem(str(value))
                if str(value)=='True' or str(value)=='False':
                    item2 = QTableWidgetItem()
                    item2.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    if str(value)=='True':
                        item2.setCheckState(QtCore.Qt.Checked) 
                    else:
                        item2.setCheckState(QtCore.Qt.Unchecked)    
                self.algorithm_parameter_list.setItem(index+1, 1, item2)
            self.algorithm_parameter_list.resizeColumnsToContents() #setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
        except Exception as e:
            print('Algorithm parameter error')
            print(e)


    def aspect_changed(self):
        """
        Stores the options value separately for each algorithm.
        Clears selection, because if other algorithm clicked after change, it's counts as a change again.
        So the same value is going to be stored for the next algorirhm selection.
        """
        try:
            selected_algo = self.algolist.selectionModel().selectedRows()
            selected_asp = self.algorithm_parameter_list.selectionModel().selectedIndexes()
            if selected_asp[0].row():
                self.algo_dict[str(self.algolist.item(selected_algo[0].row(), 0).text())][selected_asp[0].row()-1][str(self.algorithm_parameter_list.item(selected_asp[0].row(), 0).text())]=float(self.algorithm_parameter_list.item(selected_asp[0].row(), 1).text())
                self.algorithm_parameter_list.clearSelection()
        except:
            "ok"


    def runsim(self,singlerun=False): 
        """
        Check all the tabs and sends the options to the Core.
        Check the fitness values and if they are normalized.
        Check the selected algorithm and the options for it then launch the optimization.
        Calls the last step if the optimization ended.
        If an error happens, stores the number of tab in a list and it's error string in an other list.
        Switch to the tab, where the error happened and popup the erro.
        """
        err=[]
        errpop=[]
        if not self.dd_type.currentIndex():
            try:
                self.core.SecondStep({"stim" : [str(self.stimprot.currentText()), float(self.lineEdit_pos.text()), str(self.section_rec.currentText())],
                                    "stimparam" : [self.container, float(self.lineEdit_delay.text()), float(self.lineEdit_duration.text())]})
                self.kwargs = {"runparam":[float(self.lineEdit_tstop.text()),
                                        float(self.lineEdit_dt.text()),
                                        str(self.param_to_record.currentText()),
                                        str(self.section_stim.currentText()),
                                        float(self.lineEdit_posins.text()),
                                        float(self.lineEdit_initv.text())]}
            except AttributeError:
                err.append(2)
                errpop.append("No stimulus amplitude was selected!")
            except ValueError:
                errpop.append('Some of the cells are empty. Please fill out all of them!')
                err.append(2)
            except Exception as e:
                err.append(2)
                print(e)
                errpop.append("There was an error")
        self.fitfun_list=[] 
        self.weights=[]
        allRows = self.fitlist.rowCount()
        try:
            for row in range(0,allRows):
                current_fun=str(self.fitlist.item(row, 0).text())
                current_weight=float(self.fitlist.item(row, 1).text())
                if current_weight:
                    self.fitfun_list.append(current_fun)
                    self.weights.append(current_weight) 
            if self.core.option_handler.type[-1]!="features":
                self.kwargs.update({"feat":
                                    [{"Spike Detection Thres. (mv)": float(self.spike_tresh.text()), "Spike Window (ms)":float(self.spike_window.text())},
                                    self.fitfun_list]
                                    })
                self.kwargs.update({"weights" : self.weights})
            else:
                self.kwargs.update({"feat":
                                    [{"Spike Detection Thres. (mv)": float(self.spike_tresh.text()), "Spike Window (ms)":float(self.spike_window.text())},
                                    self.fitfun_list]
                                    })
                self.kwargs.update({"weights" : self.weights})
            if not(0.99<sum(self.kwargs["weights"])<=1.01):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("You did not normalize your weights! \n Would you like to continue anyway?")
                msg.setWindowTitle('Normalization')
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No)
                retval = msg.exec()
                if retval == QtWidgets.QMessageBox.No:
                    err.append(3)
                    errpop.append("Normalize")     
        except: 
            ""
        try:
            if singlerun:
                tmp = {"seed" : None,
                    "current_algorithm" : "singleRun"}
            else:
                selected_algo = self.algolist.selectionModel().selectedRows()
                algo_name=str(self.algolist.item(selected_algo[0].row(), 0).text())
                algo_str=algo_name[algo_name.find("(")+1:].replace(")","")
                tmp = {"seed" : int(self.algorithm_parameter_list.item(0,1).text()),
                    "current_algorithm" : str(algo_str)
                    }
                allRows = self.algorithm_parameter_list.rowCount()
                for row in range(1,allRows):
                    aspect = str(self.algorithm_parameter_list.item(row,0).text())
                    item = self.algorithm_parameter_list.item(row,1).text()
                    if item:
                        try:
                            if item.find(".")>0:
                                value=float(self.algorithm_parameter_list.item(row,1).text())
                            else:
                                value=int(self.algorithm_parameter_list.item(row,1).text())
                        except ValueError as e:
                            value=self.algorithm_parameter_list.item(row,1).text()
                    else:
                        value=bool(self.algorithm_parameter_list.item(row,1).checkState())
                    tmp.update({aspect:value})
            tmp.update({
                "num_params" : len(self.core.option_handler.GetObjTOOpt()),
                "boundaries" : self.core.option_handler.boundaries,
                "starting_points" : self.seed
                })
            self.kwargs.update({"algo_options":tmp})
        except Exception as e:
            err.append(4)
            print(e)
            errpop.append("Please select an algorithm")
        if err:
            if not errpop[0]=="Normalize":
                popup(errpop[0])
            self.tabwidget.setCurrentIndex(int(min(err)))
        else:
            try:
                self.seed = None
                self.core.ThirdStep(self.kwargs)
            except:
                    popup("Run step error")
            if self.core.option_handler.output_level=="1":
                self.core.Print()
            
            else:
                try:
                    self.core.FourthStep()
                    self.tabwidget.setTabEnabled(5,True)
                    self.tabwidget.setTabEnabled(6,True)
                    self.tabwidget.setCurrentIndex(5)
                    self.results_tab_plot()
                    if not singlerun:
                        self.stat_tab_fun()
                except:
                    popup("Evaluation step error")



    def results_tab_plot(self):
        text = "Results:"
        if self.core.cands:
            for n, k in zip(self.core.option_handler.GetObjTOOpt(), self.core.optimal_params):
                if n.split()[0]==n.split()[-1]:
                    param=[n.split()[0], n.split()[-1]]
                    text += "\n" + param[0] + "\n" + "\t" + str(k)
                else:
                    param=[n.split()[0], "segment: " + n.split()[1], n.split()[-1]]
                    if n.split()[1]!=n.split()[-1]:
                        text += "\n" + ": \n".join(param) + ":" + "\n" + "\t" + str(k)
                    else:
                        text += "\n" + param[0] + ": " + param[-1] + "\n" + "\t" + str(k)
        text += "\n" + "Fitness:\n" + "\t" + str(self.core.best_fit)
        for curr_label in self.result_labels:
            curr_label.setText(QtCore.QCoreApplication.translate("Neuroptimus", text))
            
        exp_data = []
        model_data = []
        
        self.results_tab_axes.cla()
        if self.core.option_handler.type[-1]!="features":
            for n in range(self.core.data_handler.number_of_traces()):
                exp_data.extend(self.core.data_handler.data.GetTrace(n))
                model_data.extend(self.core.final_result[n])
            no_traces=self.core.data_handler.number_of_traces()
            t = self.core.option_handler.input_length
            step = self.core.option_handler.run_controll_dt

            self.results_tab_axes.set_xlabel("time [ms]")
            _type=self.core.data_handler.data.type
            unit="mV" if _type=="voltage" else "nA" if _type=="current" else ""
            self.results_tab_axes.set_ylabel(_type+" [" + unit + "]")
            self.results_tab_axes.set_xticks([n for n in range(0, int((t * no_traces) / (step)), int((t * no_traces) / (step) / 5.0)) ])
            self.results_tab_axes.set_xticklabels([str(n) for n in range(0, int(t * no_traces), int((t * no_traces) / 5))])
            self.results_tab_axes.plot(list(range(0, len(exp_data))), exp_data)
            self.results_tab_axes.plot(list(range(0, len(model_data))), model_data, 'r')
            self.results_tab_axes.legend(["target", "model"])
            self.canvas2.draw()
            plt.tight_layout()
            plt.close()

        else:
            for n in range(len(self.core.data_handler.features_data["stim_amp"])):
                model_data.extend(self.core.final_result[n])
            no_traces=len(self.core.data_handler.features_data["stim_amp"])
            t = int(self.core.option_handler.run_controll_tstop)         # instead of input_length
            step = self.core.option_handler.run_controll_dt
            self.results_tab_axes.set_xlabel("time [ms]")
            _type=str(self.kwargs["runparam"][2])       #parameter to record
            _type_ = "Voltage" if _type =="v" else "Current" if _type=="c" else ""
            unit="mV" if _type=="v" else "nA" if _type=="c" else ""
            self.results_tab_axes.set_ylabel(_type_+" [" + unit + "]")
            self.results_tab_axes.set_xticks([n for n in range(0, int((t * no_traces) / (step)), int((t * no_traces) / (step) / 5.0)) ])
            self.results_tab_axes.set_xticklabels([str(n) for n in range(0, int(t * no_traces), int((t * no_traces) / 5))])
            self.results_tab_axes.plot(list(range(0, len(model_data))),model_data, 'r')
            self.results_tab_axes.legend(["model"])
            self.canvas2.draw()
            plt.tight_layout()
            plt.close()
        
    def SaveParam(self, e):
        """
        Saves the found values in a file.
        """
        try:
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            save_file_name, _ = QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()", "","Data files (*txt);;All Files (*);;", options=options)
            if save_file_name[0]:
                with open(str(save_file_name),"w+") as f:
                    f.write("\n".join(map(str,self.core.optimal_params)))
        except Exception as e:
            popup("Couldn't save the parameters." + str(e))


    def stat_tab_fun(self):
        """
        Writes out the same fitnesses for parameters as in the previous tab.
        """
        try:
            fits=self.core.fits
            stats={'best' : str(min(fits)),'worst' : str(max(fits)),'mean' : str(numpy.mean(fits)),'median' : str(numpy.median(fits)), 'std' : str(numpy.std(fits))}
        except AttributeError:
            stats={'best' : "unkown",'worst' : "unkown",'mean' : "unkown",'median' : "unkown", 'std' : "unkown"}
        string = "Best: " + str(stats['best']) + "\nWorst: " + str(stats['worst']) + "\nMean: " + str(stats['mean']) + "\nMedian: " + str(stats['median']) + "\nStd:" + str(stats['std'])
        self.stats_label.setText(QtCore.QCoreApplication.translate("Neuroptimus", string))
        self.scroll_area2_stat.setWidget(self.stats_label)
        self.errorlist.setRowCount(self.recursive_len(self.core.error_comps))

        idx=0
        for c_idx,c in enumerate(zip(*self.core.error_comps)):
            tmp=[0]*4
            for t_idx in range(len(c)):
      
                tmp[1]+=c[t_idx][2]
                tmp[2]=c[t_idx][0]
                tmp[3]+=c[t_idx][2]*c[t_idx][0]
            if self.core.option_handler.type[-1]!='features':
                tmp[0]=self.core.ffun_mapper[c[t_idx][1].__name__]
            else:
                tmp[0]=(c[t_idx][1])
            idx+=1
            tmp=list(map(str,tmp))
            self.errorlist.setItem(c_idx, 0, QTableWidgetItem(tmp[0]))
            self.errorlist.setItem(c_idx, 1, QTableWidgetItem("{:.4f}".format(float(tmp[1]))))
            self.errorlist.setItem(c_idx, 2, QTableWidgetItem("{:.4f}".format(float(tmp[2]))))
            self.errorlist.setItem(c_idx, 3, QTableWidgetItem("{:.4f}".format(float(tmp[3]))))

        self.errorlist.setRowCount(idx)

    def PlotGen(self, e):
        """
        Creates the Generation plot from the statistics file.
        """
        plt.close('all')
        generation, psize, worst, best, median, average, stdev  = [], [], [], [], [], [], []
        import json
        with open("stat_file.txt") as stat_file:
            for line in stat_file:
                row = json.loads("["+line+"]")
                generation.append(int(row[0]))
                psize.append(int(row[1]))
                worst.append(row[2])
                best.append(row[3])
                median.append(row[4])
                average.append(row[5])
                stdev.append(row[6])
        stderr = [s / numpy.sqrt(p) for s, p in zip(stdev, psize)]
        data = [average, median, best, worst]
        colors = ['black', 'blue', 'green', 'red']
        labels = ['average', 'median', 'best', 'worst']
        figure = plt.figure()
        try:
            plt.errorbar(generation, average, stderr, color=colors[0], label=labels[0])
        except:
            plt.plot(generation, average, color=colors[0], label=labels[0])
        for d, col, lab in zip(data[1:], colors[1:], labels[1:]):
            plt.plot(generation, d, '.-', color=col, label=lab)
        plt.fill_between(generation, data[2], data[3], color='#e6f2e6')
        plt.grid(True)
        ymin = min([min(d) for d in data])
        ymax = max([max(d) for d in data])
        yrange = ymax - ymin
        plt.ylim((ymin - 0.1*yrange, ymax + 0.1*yrange))  
        plt.legend(loc='upper left')    
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.show() 


    def PlotGrid(self, e):
        self.prev_bounds=copy(self.core.option_handler.boundaries)
        self.PG=gridwindow(self)
        self.PG.setObjectName("Neuroptimus")
        self.PG.resize(400, 500)
        self.PG.show()

    def ShowErrorDialog(self,e):
        self.extra_error_dialog=ErrorDialog(self)
        self.extra_error_dialog.setObjectName("Neuroptimus")
        self.extra_error_dialog.resize(400, 500)
        self.extra_error_dialog.show()

    def boundarywindow(self):
        self.BW = BoundaryWindow(self) 
        self.BW.setObjectName("Neuroptimus")
        self.BW.resize(400, 500)
        self.BW.show()

    def startingpoints(self):
        num_o_params=len(self.core.option_handler.GetObjTOOpt())
        self.SPW = Startingpoints(self,num_o_params) 
        self.SPW.setObjectName("Neuroptimus")
        self.SPW.resize(400, 500)
        self.SPW.show()

    def evaluatewindow(self):
        num_o_params=len(self.core.option_handler.GetObjTOOpt())
        self.EW = EvaluateSingle(self,num_o_params) 
        self.EW.setObjectName("Neuroptimus")
        self.EW.resize(400, 500)
        self.EW.show()
    
class SecondWindow(QtWidgets.QMainWindow):
    def __init__(self,parent): 
        super(SecondWindow, self).__init__()
        _translate = QtCore.QCoreApplication.translate
        self.core=Core.coreModul()
        self.plaintext = QtWidgets.QPlainTextEdit(self)
        self.plaintext.insertPlainText("#Please define your function below in the template!\n"+
                "#You may choose an arbitrary name for your function,\n"+
                "#but the input parameters must be self and a vector!In the first line of the function specify the length of the vector in a comment!\n"+
                "#In the second line you may specify the names of the parameters in a comment, separated by spaces.\n")
        self.plaintext.move(10,10)
        self.plaintext.resize(350,400)
        self.pushButton_45 = QtWidgets.QPushButton(self)
        self.pushButton_45.setGeometry(QtCore.QRect(370, 30, 80, 22))
        self.pushButton_45.setObjectName("pushButton_45")
        self.pushButton_45.setText(_translate("Ufun", "Load"))
        self.pushButton_45.clicked.connect(self.loaduserfun)
        self.pushButton_46 = QtWidgets.QPushButton(self)
        self.pushButton_46.setGeometry(QtCore.QRect(20, 440, 80, 22))
        self.pushButton_46.setObjectName("pushButton_46")
        self.pushButton_46.setText(_translate("Ufun", "Ok"))
        self.pushButton_46.clicked.connect(self.OnOk)
        self.pushButton_47 = QtWidgets.QPushButton(self)
        self.pushButton_47.setGeometry(QtCore.QRect(120, 440, 80, 22))
        self.pushButton_47.setObjectName("pushButton_47")
        self.pushButton_47.setText(_translate("Ufun", "Cancel"))
        self.pushButton_47.clicked.connect(self.close)
        self.option_handler=parent.core.option_handler 
        self.modellist=parent.modellist

        # Create the central widget
        self.central = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central)
            
        # Create a new QGridLayout
        grid = QtWidgets.QGridLayout(self.central)
        
        # Add the widgets to the grid layout
        grid.addWidget(self.plaintext, 0, 0, 1, 2)
        grid.addWidget(self.pushButton_45, 1, 0)
        grid.addWidget(self.pushButton_46, 1, 1)
        grid.addWidget(self.pushButton_47, 2, 1)

        # Set the layout of the central widget to the grid layout
        self.central.setLayout(grid)

        # Set the properties of the main window
        self.setWindowTitle("User Defined Function")
        self.setGeometry(100, 100, 500, 500)


    def loaduserfun(self):    
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*);;", options=options)
        if fileName:
            
            with open(fileName, "r") as f:
                fun =   ("#Please define your function below in the template!\n"+
                    "#You may choose an arbitrary name for your function,\n"+
                    "#but the input parameters must be self and a vector!In the first line of the function specify the length of the vector in a comment!\n"+
                    "#In the second line you may specify the names of the parameters in a comment, separated by spaces.\n")
                for l in f:
                    fun = fun + l
            self.plaintext.setPlainText(str(fun))
    
    def OnOk(self, e):
        try:
            self.option_handler.u_fun_string = str(self.plaintext.toPlainText())
            self.option_handler.adjusted_params=[]
            self.modellist.setRowCount(0)
            text = ""
            text = list(map(str.strip, str(self.plaintext.toPlainText()).split("\n")))[4:-1]
            variables = []
            variables = list(map(str.strip, str(text[0][text[0].index("(") + 1:text[0].index(")")]).split(",")))
            var_len = int(text[1].lstrip("#"))
            i=0
            var_names=[]
            while text[i+2][0]=="#" and i<var_len:
                var_names.append(text[i+2].lstrip("#"))
                i+=1
            if len(var_names)!=var_len and len(var_names)!=0:
                raise SyntaxError("Number of parameter names must equal to number of parameters")
            if var_names==[]:
                var_names=None
            for i in range(var_len):
                self.option_handler.SetOptParam(0.1)
                if var_names != None:
                    self.option_handler.SetObjTOOpt(var_names[i])
                else:
                    self.option_handler.SetObjTOOpt("Vector" + "[" + str(i) + "]")
            if variables[0] == '':
                raise ValueError
            compile(self.plaintext.toPlainText(), '<string>', 'exec')
            self.close()
        except ValueError as val_err:
            popup("Your function doesn't have any input parameters!")
        except SyntaxError as syn_err:
            popup(str(syn_err) +"Syntax Error")
    

class StimuliWindow(QtWidgets.QMainWindow):
    def __init__(self,parent): 
        super(StimuliWindow, self).__init__()
        _translate = QtCore.QCoreApplication.translate
        self.parent=parent
        # Create the central widget
        self.central = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central)
        self.amplit_edit = QtWidgets.QLineEdit(self)
        self.amplit_edit.setGeometry(QtCore.QRect(140, 10, 61, 22))
        self.amplit_edit.setObjectName("amplit_edit")
        self.amplit_edit.setValidator(self.parent.intvalidator)
        self.label_amplit = QtWidgets.QLabel(self)
        self.label_amplit.setGeometry(QtCore.QRect(10, 10, 141, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_amplit.setFont(font)
        self.label_amplit.setObjectName("label_amplit")
        self.label_amplit.setText(_translate("Neuroptimus", "Number of stimuli:"))
        self.pushButton_create = QtWidgets.QPushButton(self)
        self.pushButton_create.setGeometry(QtCore.QRect(250, 10, 61, 21))
        self.pushButton_create.setObjectName("pushButton_create")
        self.pushButton_create.setText(_translate("Neuroptimus", "Create"))
        self.pushButton_create.clicked.connect(self.Set)
        self.pushButton_accept = QtWidgets.QPushButton(self)
        self.pushButton_accept.setGeometry(QtCore.QRect(200, 450, 61, 21))
        self.pushButton_accept.setObjectName("pushButton_accept")
        self.pushButton_accept.setText(_translate("Neuroptimus", "Accept"))
        self.pushButton_accept.clicked.connect(self.Accept)
        self.pushButton_accept.setEnabled(False)
        self.option_handler=self.parent.core.option_handler
        self.data_handler=self.parent.core.data_handler
        self.stim_table= QtWidgets.QTableWidget(self)
        self.stim_table.setGeometry(QtCore.QRect(80, 50, 150, 361))
        self.stim_table.setObjectName("stim_table")
        self.stim_table.setColumnCount(1)
        _type=self.parent.stimprot.currentText()
        unit="mV" if _type=="VClamp" else "nA" if _type=="IClamp" else ""
        self.stim_table.setHorizontalHeaderLabels(["Amplitude ("+unit+")"])
        self.stim_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.stim_table.horizontalHeader().setStretchLastSection(True)



        # Create a new QGridLayout
        grid = QtWidgets.QGridLayout(self.central)

        # Add the widgets to the grid layout
        grid.addWidget(self.label_amplit, 0, 0)
        grid.addWidget(self.amplit_edit, 0, 1)
        grid.addWidget(self.pushButton_create, 0, 2)
        grid.addWidget(self.stim_table, 1, 0, 1, 3)
        grid.addWidget(self.pushButton_accept, 2, 2)

        # Set the layout of the central widget to the grid layout
        self.centralWidget().setLayout(grid)

        # Set the properties of the main window
        self.setWindowTitle("Stimuli Window")
        self.setGeometry(100, 100, 400, 500)


        if self.parent.container:
            self.amplit_edit.setText(str(len(self.parent.container)))
            self.stim_table.setRowCount(len(self.parent.container))
            for idx,n in enumerate(self.parent.container):
                self.stim_table.setItem(idx, 0, QTableWidgetItem(str(n)))

        
        try:
            if self.option_handler.type[-1]=="features":
                self.amplit_edit.setText(str(len(self.data_handler.features_data["stim_amp"])))
                self.Set(self) 
        except:
            print("No input file found")

    def Set(self, e):
        try:
            self.stim_table.setRowCount(int(self.amplit_edit.text()))
            self.pushButton_accept.setEnabled(True)
        except:
            self.close()
        

    def Accept(self, e):
        self.parent.container=[]
        try:
            for n in range(self.stim_table.rowCount()):
                self.parent.container.append(float(self.stim_table.item(n, 0).text()))
        except:
                print("Stimuli values are missing or incorrect")
        self.close()

    
class BoundaryWindow(QtWidgets.QMainWindow):
    def __init__(self,parent): 
        super(BoundaryWindow, self).__init__()
        _translate = QtCore.QCoreApplication.translate
        hstep = 130
        vstep = 35
        hoffset = 10
        voffset = 15
        self.option_handler=parent.core.option_handler
        self.boundary_table = QtWidgets.QTableWidget(self)
        self.boundary_table.setGeometry(QtCore.QRect(10, 10, 302, 361))
        self.boundary_table.setObjectName("boundary_table")
        self.boundary_table.setColumnCount(3)
        self.boundary_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.boundary_table.setHorizontalHeaderLabels(("Parameters;Minimum;Maximum").split(";"))
        self.boundary_table.setRowCount(len(self.option_handler.GetObjTOOpt()))
        

        for l in range(len(self.option_handler.GetObjTOOpt())):
            param=self.option_handler.GetObjTOOpt()[l].split()
            if len(param)==4:
                label=param[0] + " " + param[1] + " " + param[3]
            else:
                if param[0]!=param[-1]:
                    label=param[0] + " " + param[-1]
                else:
                    label=param[-1]
           
            
            item = QTableWidgetItem(label)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )      
            self.boundary_table.setItem(l, 0, item)
            if len(self.option_handler.boundaries[1]) == len(self.option_handler.GetObjTOOpt()):
                minitem = QTableWidgetItem(str(self.option_handler.boundaries[0][l]))
                maxitem = QTableWidgetItem(str(self.option_handler.boundaries[1][l]))
                self.boundary_table.setItem(l, 1, minitem)
                self.boundary_table.setItem(l, 2, maxitem)
            
        
           
        Setbutton = QtWidgets.QPushButton(self)
        Setbutton.setGeometry(QtCore.QRect(10, 400, 80, 22))
        Setbutton.setObjectName("Setbutton")
        Setbutton.setText(_translate("Neuroptimus", "Set"))
        Setbutton.clicked.connect(self.Set)
        Savebutton = QtWidgets.QPushButton(self)
        Savebutton.setGeometry(QtCore.QRect(100, 400, 80, 22))
        Savebutton.setObjectName("Savebutton")
        Savebutton.setText(_translate("Neuroptimus", "Save"))
        Savebutton.clicked.connect(self.Save)
        Loadbutton = QtWidgets.QPushButton(self)
        Loadbutton.setGeometry(QtCore.QRect(190, 400, 80, 22))
        Loadbutton.setObjectName("Savebutton")
        Loadbutton.setText(_translate("Neuroptimus", "Load"))
        Loadbutton.clicked.connect(self.Load)

    def Set(self, e):
        try:
            min_l=[]
            max_l=[]
            for idx in range(self.boundary_table.rowCount()):
                min_l.append(float(self.boundary_table.item(idx,1).text()))
                max_l.append(float(self.boundary_table.item(idx,2).text()))
            self.option_handler.boundaries[0] = min_l
            self.option_handler.boundaries[1] = max_l
            for i in range(len(self.option_handler.boundaries[0])):
                if self.option_handler.boundaries[0][i] >= self.option_handler.boundaries[1][i]:
                    popup("""Min boundary must be lower than max
                                Invalid Values""")
                    raise Exception
        except ValueError:
            popup("Invalid Value")
        except Exception:
            print('Error Occured')
        self.close()

    def Save(self,e): 
        save_bound = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
        if save_bound[0]:
            with open(str(save_bound[0]),'w+') as f:
                for idx in range(self.boundary_table.rowCount()):
                    f.write(str(self.boundary_table.item(idx,1).text()))
                    f.write("\t")
                    f.write(str(self.boundary_table.item(idx,2).text()))
                    f.write("\n")
            

    def Load(self,e):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*);;", options=options)
        if fileName:
            with open(fileName, "r") as f:
                for idx,l in enumerate(f):
                    bounds=l.split()
                    self.boundary_table.setItem(idx, 1, QTableWidgetItem(str(bounds[0])))
                    self.boundary_table.setItem(idx, 2, QTableWidgetItem(str(bounds[1])))

                


class Startingpoints(QtWidgets.QMainWindow):
    def __init__(self,parent,*args,**kwargs):
        super(Startingpoints,self).__init__()
        _translate = QtCore.QCoreApplication.translate
        n_o_params=args[0]
        self.parent=parent
        self.container=[]
        hstep = 130
        vstep = 35
        hoffset = 10
        voffset = 15
        for n in range(n_o_params):
            param=parent.core.option_handler.GetObjTOOpt()[n].split()
            if len(param)==4:
                p_name=param[0] + " " + param[1] + " " + param[3]
            else:
                if param[0]!=param[-1]:
                    p_name=param[0] + " " + param[-1]
                else:
                    p_name=param[-1]
            
            #p_name=self.parent.core.option_handler.GetObjTOOpt()[n].split()[-1]
            lbl = QtWidgets.QLabel(self)
            lbl.setGeometry(QtCore.QRect(hoffset, voffset + n * vstep, 121, 16))
            font = QtGui.QFont()
            font.setFamily("Ubuntu")
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            lbl.setFont(font)
            lbl.setObjectName("ctrl")
            lbl.setText(QtCore.QCoreApplication.translate("Neuroptimus", p_name))

            ctrl = QtWidgets.QLineEdit(self)
            ctrl.setGeometry(QtCore.QRect(hstep, voffset + n * vstep, 61, 22))
            ctrl.setObjectName("ctrl")
            if self.parent.seed:
                ctrl.setText(str(self.parent.seed[n]))
            lbl.show()
            ctrl.show()
            self.container.append(ctrl)

        Okbutton = QtWidgets.QPushButton(self)
        Okbutton.setGeometry(QtCore.QRect(10, 400, 80, 22))
        Okbutton.setObjectName("Okbutton")
        Okbutton.setText(_translate("Neuroptimus", "Ok"))
        Okbutton.clicked.connect(self.OnOk)
        Closebutton = QtWidgets.QPushButton(self)
        Closebutton.setGeometry(QtCore.QRect(100, 400, 80, 22))
        Closebutton.setObjectName("Closebutton")
        Closebutton.setText(_translate("Neuroptimus", "Cancel"))
        Closebutton.clicked.connect(self.close)
        Loadpopbutton = QtWidgets.QPushButton(self)
        Loadpopbutton.setGeometry(QtCore.QRect(280, 400, 80, 22))
        Loadpopbutton.setObjectName("Loadpopbutton")
        Loadpopbutton.setText(_translate("Neuroptimus", "Load Population"))
        Loadpopbutton.clicked.connect(self.OnLoadPop)
        Loadbutton = QtWidgets.QPushButton(self)
        Loadbutton.setGeometry(QtCore.QRect(190, 400, 80, 22))
        Loadbutton.setObjectName("Loadbutton")
        Loadbutton.setText(_translate("Neuroptimus", "Load Point"))
        Loadbutton.clicked.connect(self.OnLoad)

        

    def OnOk(self,e):
        self.parent.seed=[]      
        for n in self.container:
            self.parent.seed.append(float(n.text()))
        self.close()
            

    def OnLoad(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*);;", options=options)
        if fileName:
            with open(fileName, "r") as f:
                for idx, l in enumerate(f):
                    self.container[idx].setText(str(l))
           
    
    def OnLoadPop(self,e):
        self.size_of_pop = 0
        file_path = ""
        popup("This function is only supported by the algorithms from inspyred!")
        
        text, ok = QInputDialog.getText(self, 'TLoad Population', 'Enter size of population:')
        if ok:
            self.size_of_pop = int(text)
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            file_path, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*);;", options=options)
               

        def lastlines(hugefile, n, bsize=2048):
            import errno
            with open(hugefile, 'rb') as hfile:
                if not hfile.readline():
                    return
                sep = hfile.newlines
                hfile.seek(0, os.SEEK_END)
                linecount = 0
                pos = 0

                while linecount <= n:

                    try:
                        hfile.seek(-bsize, os.SEEK_CUR)
                        linecount += hfile.read(bsize).count(sep)
                        hfile.seek(-bsize, os.SEEK_CUR)
                    except IOError as e:
                        if e.errno == errno.EINVAL:
                            # Attempted to seek past the start, can't go further
                            bsize = hfile.tell()
                            hfile.seek(0, os.SEEK_SET)
                            linecount += hfile.read(bsize).count(sep)
                    pos = hfile.tell()

                for line in hfile:
                # We've located n lines *or more*, so skip if needed
                    if linecount > n:
                        linecount -= 1
                        continue
                # The rest we yield
                    yield line

                for l in lastlines(file_path, self.size_of_pop, 1):
                    s=l.strip()
                    params = [float(x.lstrip("[").rstrip("]")) for x in s.split(", ")][3:-1]
                    params = params[0:len(params) / 2 + 1]
                    self.parent.seed.append(params)
        self.close()

class EvaluateSingle(QtWidgets.QMainWindow):
    def __init__(self,parent,*args,**kwargs):
        super(EvaluateSingle,self).__init__()
        _translate = QtCore.QCoreApplication.translate
        n_o_params=args[0]
        self.parent=parent
        self.container=[]
        hstep = 130
        vstep = 35
        hoffset = 10
        voffset = 15
        self.option_handler=parent.core.option_handler
        self.evaluate_table = QtWidgets.QTableWidget(self)
        self.evaluate_table.setGeometry(QtCore.QRect(10, 10, 302, 361))
        self.evaluate_table.setObjectName("evaluate_table")
        self.evaluate_table.setColumnCount(2)
        self.evaluate_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.evaluate_table.setHorizontalHeaderLabels(("Parameters;Value").split(";"))
        self.evaluate_table.setRowCount(len(self.option_handler.GetObjTOOpt()))
        

        for l in range(len(self.option_handler.GetObjTOOpt())):
            param=self.option_handler.GetObjTOOpt()[l].split()
            if len(param)==4:
                label=param[0] + " " + param[1] + " " + param[3]
            else:
                if param[0]!=param[-1]:
                    label=param[0] + " " + param[-1]
                else:
                    label=param[-1]
           
            
            item = QTableWidgetItem(label)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )      
            self.evaluate_table.setItem(l, 0, item)
            
        
           

        Evaluatebutton = QtWidgets.QPushButton(self)
        Evaluatebutton.setGeometry(QtCore.QRect(10, 400, 80, 22))
        Evaluatebutton.setObjectName("Evaluatebutton")
        Evaluatebutton.setText(_translate("Neuroptimus", "Evaluate"))
        Evaluatebutton.clicked.connect(self.OnEvaluate)
        Loadbutton = QtWidgets.QPushButton(self)
        Loadbutton.setGeometry(QtCore.QRect(100, 400, 80, 22))
        Loadbutton.setObjectName("Loadbutton")
        Loadbutton.setText(_translate("Neuroptimus", "Load"))
        Loadbutton.clicked.connect(self.OnLoad)
        Closebutton = QtWidgets.QPushButton(self)
        Closebutton.setGeometry(QtCore.QRect(190, 400, 80, 22))
        Closebutton.setObjectName("Closebutton")
        Closebutton.setText(_translate("Neuroptimus", "Cancel"))
        Closebutton.clicked.connect(self.close)
        

    def OnEvaluate(self,e):
        self.parent.core.optimal_params = []
        self.parent.core.option_handler.boundaries = [[],[]]
        for idx in range(self.evaluate_table.rowCount()):
            param_value=float(self.evaluate_table.item(idx,1).text())
            self.parent.core.optimal_params.append(param_value)
            self.parent.core.option_handler.boundaries[0].append(param_value*0.99)
            self.parent.core.option_handler.boundaries[1].append(param_value*1.01)
        self.parent.runsim(singlerun=True)
        self.close()

    def OnLoad(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*);;", options=options)
        if fileName:
            f = open(fileName, "r")
            for idx,l in enumerate(f):
                self.evaluate_table.setItem(idx, 1, QTableWidgetItem(str(l)))
                
    
   

class gridwindow(QtWidgets.QMainWindow):
    def __init__(self,parent,*args):
        super(gridwindow,self).__init__()
        _translate = QtCore.QCoreApplication.translate
        hstep = 200
        vstep = 35
        hoffset = 10
        voffset = 15
        self.min = []
        self.max = []
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.option_handler=parent.core.option_handler

        for l in range(len(self.option_handler.GetObjTOOpt())):
            lbl = QtWidgets.QLabel(self)
            lbl.setGeometry(QtCore.QRect(hoffset, voffset + l * vstep, 121, 16))
            
            lbl.setFont(font)
            lbl.setObjectName("ctrl")
            lbl.setText(QtCore.QCoreApplication.translate("Neuroptimus", self.option_handler.GetObjTOOpt()[l].split()[-1]))

            
            tmp_min = QtWidgets.QLineEdit(self)
            tmp_min.setGeometry(QtCore.QRect(hstep, voffset + l * vstep, 75, 30))
            tmp_min.setObjectName("tmp_min")
            tmp_max = QtWidgets.QLineEdit(self)
            tmp_max.setGeometry(QtCore.QRect(hstep + hstep/2, voffset + l * vstep, 75, 30))
            tmp_max.setObjectName("tmp_min")
            lbl.show()
            tmp_min.show()
            self.min.append(tmp_min)
            self.max.append(tmp_max)
            if len(self.option_handler.boundaries[1]) == len(self.option_handler.GetObjTOOpt()):
                tmp_min.setText(str(self.option_handler.boundaries[0][l]))
                tmp_max.setText(str(self.option_handler.boundaries[1][l]))

        self.resolution_ctrl = QtWidgets.QLineEdit(self)
        self.resolution_ctrl.setGeometry(QtCore.QRect(hstep,600, 75, 30))
        self.resolution_ctrl.setObjectName("ctrl")
        self.resolution_ctrl.setText(str(parent.resolution))

        Setbutton = QtWidgets.QPushButton(self)
        Setbutton.setGeometry(QtCore.QRect(hstep, 650, 80, 22))
        Setbutton.setObjectName("Okbutton")
        Setbutton.setText(_translate("Neuroptimus", "Ok"))
        Setbutton.clicked.connect(self.Set)
        


    def Set(self, e):
        try:
            self.option_handler.boundaries[0] = [float(n.GetValue()) for n in self.min]
            self.option_handler.boundaries[1] = [float(n.GetValue()) for n in self.max]
            self.resolution=int(self.resolution_ctrl.text())
            self.close()
        except ValueError as ve:
           popup("Invalid Value")
        


class ErrorDialog(QtWidgets.QMainWindow):
    def __init__(self,parent):
        super(ErrorDialog,self).__init__()
        self.error_comp_table = QtWidgets.QTableWidget(self)
        self.error_comp_table.setGeometry(QtCore.QRect(10, 200, 441, 261))
        self.error_comp_table.setObjectName("error_comp_table")
        self.error_comp_table.setColumnCount(4)
        self.error_comp_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.error_comp_table.setHorizontalHeaderLabels(("Error Function;Value;Weight;Weighted Value").split(";"))
        self.error_comp_table.setRowCount(parent.recursive_len(parent.core.error_comps))
        tmp_w_sum=0
        c_idx=0
        for t in parent.core.error_comps:
            for c in t:
                #tmp_str.append( "*".join([str(c[0]),c[1].__name__]))
                if parent.core.option_handler.type[-1]!="features":
                    self.error_comp_table.setItem(c_idx,0,QTableWidgetItem(parent.core.ffun_mapper[c[1].__name__]))
                else:
                    self.error_comp_table.setItem(c_idx,0,QTableWidgetItem(c[1]))
                self.error_comp_table.setItem(c_idx,1,QTableWidgetItem(str("{:.4f}".format(c[2]))))
                self.error_comp_table.setItem(c_idx,2,QTableWidgetItem(str("{:.4f}".format(c[0]))))
                self.error_comp_table.setItem(c_idx,3,QTableWidgetItem(str("{:.4f}".format(c[0]*c[2]))))
                c_idx+=1
                tmp_w_sum +=c[0]*c[2]
            c_idx+=1
            self.error_comp_table.setItem(c_idx,0,QTableWidgetItem("Weighted Sum"))
            self.error_comp_table.setItem(c_idx,1,QTableWidgetItem("-"))
            self.error_comp_table.setItem(c_idx,2,QTableWidgetItem("-"))
            self.error_comp_table.setItem(c_idx,3,QTableWidgetItem(str(tmp_w_sum)))
            
            tmp_w_sum=0
            self.error_comp_table.setRowCount(c_idx)


def main(param=None):
    if param!=None:
        core=Core.coreModul()
        core.option_handler.output_level=param.lstrip("-v_level=")
    app = QtWidgets.QApplication(sys.argv)
    Neuroptimus = QtWidgets.QMainWindow()
    ui = Ui_Neuroptimus()
    ui.setupUi(Neuroptimus)
    Neuroptimus.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()    

