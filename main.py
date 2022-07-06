import os
import subprocess
import sys
# from tkinter import FALSE

from gui.ui_main_window import *
from main_process import *
from drag_and_drop import *
from file_organizer import OutputResource
from tray_hanger import InputCsv

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import pythoncom
import win32com.client as client


import pymsgbox as pymsgbox #https://pymsgbox.readthedocs.io/en/latest/native.html
import time

from tray_hanger import InputCsv 


#--->>    pyside6-rcc resources.qrc -o resources_rc.py
# https://www.pythonguis.com/tutorials/packaging-pyqt6-applications-windows-pyinstaller/

# create a global variable 
output_folder_path = ''
final_input_path = ''


class WorkerThread(QThread):
    
    
    # signal to change the gif in the GUI
    thread_signal = Signal(str)

    def run(self):

        print('.... running main thread ..........')

        #below line will  be needed , ref link:https://github.com/xlwings/xlwings/issues/759
        pythoncom.CoInitialize()

        self.thread_signal.emit('main_process_started')

        #called from main_process.py
        app_run = main(final_input_path)
        app_run.run_main_process()

        # make the variable global
        global output_folder_path

        output_folder_path = app_run.output_folder_path

        print('output_folder_path..........')
        print(output_folder_path)

        # emit signal that main process is finished
        self.thread_signal.emit('main_process_finished')
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.help_file_link = '/data/_help/help.pdf'

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

        # set-up output folder value, this will hold the folder path after executing the code


        # initialization for DRAG & DROP functionality
        self.gif = Gif_drop('V Center', self)
        self.gif.setAcceptDrops(True)
        self.gif.fileDropped.connect(self.get_link_from_drop)
        self.ui.gif_layout.addWidget(self.gif)
        self.gif.setAlignment(Qt.AlignCenter)

        # set-up default gif
        self.start_up_load()

        
        # run main process thru a thread
        self.ui.btn_run.clicked.connect(self.process_button_start)


        # open folder if process finished
        self.ui.btn_open_folder.clicked.connect(self.open_output_folder)

        # open help file
        self.ui.btn_docum_link.clicked.connect(self.open_help_link)

        ## ==> MOVE WINDOW / MAXIMIZE / RESTORE
        ########################################################################
        def moveWindow(event):

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frm_header.mouseMoveEvent = moveWindow
        self.ui.title_header.mouseMoveEvent = moveWindow
        ## ==> END ##


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

        ### ==> MINIMIZE
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())


        ## SHOW ==> CLOSE APPLICATION
        self.ui.btn_close.clicked.connect(lambda: self.close())


        # CLOSE THE SPLASH SCREEN
        try:
            self.close_splashscreen()
        except:
            print('No Splash Screen Detected')


        time.sleep(.9)

        self.show()
    
    
    # SPLASHSCREEN
    ############################################################################
    ############################################################################
    ############################################################################

    def close_splashscreen(self):
        self.write_file()

    def get_parent_path(self):
        directory = os.getcwd()

        idx = directory.find('\main_app')
        print(idx)

        parent_path = directory[0:idx]
        print(parent_path)

        return parent_path

    
    def get_app_status_file_path(self):
        parent_path = self.get_parent_path()

        launcher_folder = os.listdir(parent_path + '\\' + 'launcher')
        print(launcher_folder)
        path = parent_path + '\\' + 'launcher' + '\\' + str(launcher_folder[0]) + '\\' + 'main_app_status.txt'
        print(path)

        return path

    def write_file(self):        
        path = self.get_app_status_file_path()
        print(path)
        f = open(path, "w")
        f.write("LOADED")
        f.close()

    ############################################################################
    ############################################################################
    ############################################################################



    ## EVENT ==> MOUSE CLICK
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MidButton:
            print('Mouse click: MIDDLE BUTTON')
    ## ==> END ##


    def process_button_start(self):
        self.worker = WorkerThread()
        self.worker.start()
        self.worker.thread_signal.connect(self.change_setup)

        self.ui.btn_run.setEnabled(False)
        self.ui.btn_run.setStyleSheet(self.style_button_2) #==> #2F5597

    def start_up_load(self):

        self.movie = QMovie('images/loader_2.gif')
        # self.movie = QMovie('images/ai_2.gif')
        self.gif.setMovie(self.movie)#-> jibber addin
        self.movie.start()#-> jibber addin
        
        # disable button run first
        
        self.ui.btn_run.setStyleSheet(self.style_button_2) #==> #2F5597
        self.ui.btn_open_folder.setStyleSheet(self.style_button_2) #==> #2F5597
        self.ui.btn_run.setEnabled(False)
        self.ui.btn_open_folder.setEnabled(False)
        
    def change_setup(self, signal_emitted):

        if signal_emitted == 'main_process_started':
            self.movie = QMovie('images/loader_3.gif')
            # self.movie = QMovie('images/ai_3.gif')
            self.gif.setMovie(self.movie)#-> jibber addin
            self.movie.start()#-> jibber addin


        if signal_emitted == 'main_process_finished':
            # self.movie = QMovie('images/loader_2.gif')
            self.movie = QMovie('images/loader_2.gif')
            self.gif.setMovie(self.movie)#-> jibber addin
            self.movie.start()#-> jibber addin

            #set up buttons
            self.ui.btn_run.setEnabled(False)
            self.ui.btn_run.setStyleSheet(self.style_button_2) #==> #2F5597
            self.ui.btn_open_folder.setStyleSheet(self.style_button_1) #==> #2F5597
            self.ui.btn_open_folder.setEnabled(True)
            
            pymsgbox.alert(text='THFL generated.', title='Process Information', button='OK')

    
    def open_help_link(self):
        # link = 'C:\jeevrapps\cway_thfl_automation - new\data\_help\help.pdf'
        cwd = os.getcwd()
        link = cwd + self.help_file_link
        # os.startfile(self.help_file_link)
        os.startfile(link)
        


    def open_output_folder(self):
        # input_file = OutputResource(final_input_path)
        # folder_path = input_file.complete_folder_path
        print(f'...output folder path {output_folder_path}')
        os.startfile(output_folder_path)



    def get_link_from_drop(self, l):
        print('\n')
        print('function: --get_link_from_drop--')

        print('file_dropped')
        global final_input_path

        for url in l:
            if os.path.exists(url):
                print(url)                
                # self.ui.lbl_link.setText(url)
                if not self.verify_input(url)[0]:
                    
                    pymsgbox.alert(text=self.verify_input(url)[1], title='Input Validation', button='OK')
                    
                    self.ui.btn_run.setEnabled(False)
                    self.ui.btn_run.setStyleSheet('background-color: #8FAADC;') #==> #2F5597

                else:

                    pymsgbox.alert(text=self.verify_input(url)[1], title='Input Validation', button='OK')

                    # self.ui.btn_run.setStyleSheet('background-color: #2F5597;') #==> #2F5597
                    # self.ui.btn_run.setEnabled(True)
                    # self.ui.btn_open_folder.setStyleSheet('background-color: #8FAADC;') #==> #2F5597
                    # self.ui.btn_open_folder.setEnabled(False)

                    #set up buttons
                    self.ui.btn_run.setEnabled(True)
                    self.ui.btn_run.setStyleSheet(self.style_button_1) #==> #2F5597
                    self.ui.btn_open_folder.setStyleSheet(self.style_button_2) #==> #2F5597
                    self.ui.btn_open_folder.setEnabled(False)

                    final_input_path = url
                    print(final_input_path)

                    file_input = OutputResource(url)
                    file_input.copy_filedropped_to_input_folder()


                
    def verify_input(self, file_link):
        print('\n')
        print('function: --verify_input--')

        # global final_input_path

        if '.txt' in file_link:

            print(file_link)

            input_cols = InputCsv()
            is_valid = input_cols.check_csv(file_link)

            if is_valid[0] == True:

                print(is_valid[1])
                return True, is_valid[1]
            else:
                print(is_valid[1])
                return False, is_valid[1]

        else:
            print('Input file invalid.')

            return False







if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('sharingan.ico'))
    window = MainWindow()
    
    # show GUI window form
    
    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    app.exec()

    # pyinstaller.exe --icon=sharingan.ico --onefile --noconsole --name=Py-AutoFab main.py