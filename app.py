import os
import subprocess
import sys
# from tkinter import FALSE

from gui.ui_main_window import *

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import pythoncom
import win32com.client as client

import time

from modules.dragdrop.drag_and_drop import Gif_drop
from modules.verify.verify_dropped import DroppedFile
from modules.threads.thfl_process import THFLProcess

#--->>    pyside6-rcc resources.qrc -o resources_rc.py
# https://www.pythonguis.com/tutorials/packaging-pyqt6-applications-windows-pyinstaller/

# create a global variable 
output_folder_path = ''
final_input_path = ''

class MainProcess(QThread):
    # signal to change the gif in the GUI
    thread_signal = Signal(str)

    def run(self):

        pythoncom.CoInitialize() # this line will  be needed , ref link: https://github.com/xlwings/xlwings/issues/759

        self.thread_signal.emit('STARTED') # emit signal that main process has started
        
        time.sleep(2)

        thfl = THFLProcess() # initialize thfl process
        thfl.execute_process()
        print(thfl.input_raw_file_path)
        print(thfl.ship)
        print(thfl.space)
        
        self.thread_signal.emit('FINISHED') # emit signal that main process has finished


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setup_stylesheet()

        self.setup_GIF()

        self.setup_app_window_settings()

        self.setup_button_press()
        
        self.setup_window_movement()

        self.show()
    
    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    def setup_app_window_settings(self):
        ### ==> REMOVE DEFAULT WINDOW
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        ### ==> REMOVE DEFAULT WINDOW
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(5)
        self.shadow.setYOffset(5)
        self.shadow.setColor(QColor(0, 0, 0, 160))
        self.ui.frame_main.setAutoFillBackground(True)
        self.ui.frame_main.setGraphicsEffect(self.shadow)
    
    def setup_window_movement(self):
        ########################################################################
        ## ==> MOVE WINDOW / MAXIMIZE / RESTORE
        def moveWindow(event):

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()
        ## ==> MOVE WINDOW / MAXIMIZE / RESTORE
        ########################################################################

        # WIDGET TO MOVE
        self.ui.frm_header.mouseMoveEvent = moveWindow
        self.ui.title_header.mouseMoveEvent = moveWindow

    def setup_button_press(self):
        ### ==> MINIMIZE
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        ## SHOW ==> CLOSE APPLICATION
        self.ui.btn_close.clicked.connect(lambda: self.close())

        # # run main process thru a thread
        self.ui.btn_run.clicked.connect(self._process_start)

        # # open folder if process finished
        # self.ui.btn_open_folder.clicked.connect(self.open_output_folder)

        # # open help file
        self.ui.btn_docum_link.clicked.connect(self.open_help_link)

    def _process_start(self):
        print('process start')

        # initialize worker thread
        self.main_process = MainProcess()
        self.main_process.start()
        self.main_process.thread_signal.connect(self._gif_change_setup) # toggle gui GIF

        # toggle left gui labels
        self.ui.frm_welcome.setMaximumHeight(0)
        self.ui.frm_status.setMaximumHeight(16777215)
        self.ui.frm_verif.setMaximumHeight(0)

        # call the THFL main process to run into a new thread
        print('xxx')

    def setup_stylesheet(self):
        self.style_button_1 = '''QPushButton {
                                    background-color: #2F5597;
                                    border-radius: 18px;	
                                    padding: 5px;
                                
                                
                                QPushButton:hover {
                                    background-color: #ff00ff;
                                }
                                

                                QPushButton:pressed {
                                    background-color: #ff007f;
                                }'''

        self.style_button_2 = '''QPushButton {
                                    background-color: #8FAADC;
                                    border-radius: 18px;	
                                    padding: 5px;
                                }
                                
                                QPushButton:hover {
                                    background-color: #ff00ff;
                                }
                                

                                QPushButton:pressed {
                                    background-color: #ff007f;
                                }'''

    def setup_GIF(self):
        # initialization for DRAG & DROP functionality
        self.gif = Gif_drop('V Center', self)
        self.gif.setAcceptDrops(True)
        self.gif.fileDropped.connect(self.process_dropped_file)
        self.ui.gif_layout.addWidget(self.gif)
        self.gif.setAlignment(Qt.AlignCenter)

        # # set-up default gif
        self._gif_start_up_load()

    def _gif_start_up_load(self):

        self.movie = QMovie('images/loader_2.gif')
        # self.movie = QMovie('images/ai_2.gif')
        self.gif.setMovie(self.movie)#-> jibber addin
        self.movie.start()#-> jibber addin
        
        # disable button run first
        self.ui.btn_run.setStyleSheet(self.style_button_2) #==> #2F5597
        self.ui.btn_open_folder.setStyleSheet(self.style_button_2) #==> #2F5597
        self.ui.btn_run.setEnabled(False)
        self.ui.btn_open_folder.setEnabled(False)
        
    def _gif_change_setup(self, signal_emitted):

        if signal_emitted == 'STARTED':
            self.movie = QMovie('images/loader_3.gif')
            # self.movie = QMovie('images/ai_3.gif')
            self.gif.setMovie(self.movie)#-> jibber addin
            self.movie.start()#-> jibber addin

        if signal_emitted == 'FINISHED':
            # self.movie = QMovie('images/loader_2.gif')
            self.movie = QMovie('images/loader_2.gif')
            self.gif.setMovie(self.movie)#-> jibber addin
            self.movie.start()#-> jibber addin

            #set up buttons
            self.ui.btn_run.setEnabled(False)
            self.ui.btn_run.setStyleSheet(self.style_button_2) #==> #2F5597
            self.ui.btn_open_folder.setStyleSheet(self.style_button_1) #==> #2F5597
            self.ui.btn_open_folder.setEnabled(True)

            # toggle left gui labels
            self.ui.frm_welcome.setMaximumHeight(16777215)
            self.ui.frm_status.setMaximumHeight(0)
            self.ui.frm_verif.setMaximumHeight(0)
            
    def open_help_link(self):
        # link = 'C:\jeevrapps\cway_thfl_automation - new\data\_help\help.pdf'
        help_file_link = '/data/_help/help.pdf'
        cwd = os.getcwd()
        link = cwd + help_file_link
        # os.startfile(self.help_file_link)
        os.startfile(link)
    
    def process_dropped_file(self, dropped_file_path):
        dropped_file = DroppedFile(dropped_file_path)
        print(dropped_file.file_name, dropped_file.file_ext)
        print(dropped_file.ship, dropped_file.space)
        print(dropped_file.returned_error)

        # hide left gui labels
        self.ui.frm_welcome.setMaximumHeight(0)
        self.ui.frm_status.setMaximumHeight(0)
        # show verification status label
        self.ui.frm_verif.setMaximumHeight(16777215)

        if len(dropped_file.returned_error) == 0: # means file path is valid and has no error
            self.ui.btn_run.setEnabled(True)
            self.ui.btn_run.setStyleSheet(self.style_button_1) #==> #2F5597
            self.ui.btn_open_folder.setStyleSheet(self.style_button_2) #==> #2F5597
            self.ui.btn_open_folder.setEnabled(False)
            self.ui.lbl_verification_return.setText('FILE VALID')
        else:
            self.ui.btn_run.setEnabled(False)
            self.ui.btn_run.setStyleSheet('background-color: #8FAADC;') #==> #2F5597
            self.ui.lbl_verification_return.setText(str(dropped_file.returned_error) + '\nFOLLOW SAMPLE FORMAT: SC123_CW_ACC')




if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('sharingan.ico'))
    window = MainWindow()

    
    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    app.exec()

    # pyinstaller.exe --icon=sharingan.ico --onefile --noconsole --name=Py-AutoFab main.py