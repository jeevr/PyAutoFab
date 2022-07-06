# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowshKGhT.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(428, 425)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setStyleSheet(u"")
        self.frame_main = QWidget(MainWindow)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setMinimumSize(QSize(400, 400))
        self.frame_main.setMaximumSize(QSize(400, 400))
        self.frame_main.setStyleSheet(u"QWidget#frame_main{\n"
"background-color: rgb(32, 56, 100);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 20px;	\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton {\n"
"	background-color: #2F5597;\n"
"	border-radius: 18px;	\n"
"	padding: 5px;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
" \n"
"QPushButton:hover {\n"
"	background-color: #ff00ff;\n"
"}\n"
" \n"
"\n"
"QPushButton:pressed {\n"
"	background-color: #ff007f;\n"
"}\n"
"\n"
"QLabel{\n"
"	border: 0px;	\n"
"}\n"
"\n"
"\n"
"")
        self.verticalLayout = QVBoxLayout(self.frame_main)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frm_header = QFrame(self.frame_main)
        self.frm_header.setObjectName(u"frm_header")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frm_header.sizePolicy().hasHeightForWidth())
        self.frm_header.setSizePolicy(sizePolicy1)
        self.frm_header.setMinimumSize(QSize(0, 30))
        self.frm_header.setMaximumSize(QSize(16777215, 30))
        self.frm_header.setCursor(QCursor(Qt.SizeAllCursor))
        self.frm_header.setLayoutDirection(Qt.LeftToRight)
        self.frm_header.setFrameShape(QFrame.StyledPanel)
        self.frm_header.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frm_header)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frm_header_title = QFrame(self.frm_header)
        self.frm_header_title.setObjectName(u"frm_header_title")
        self.frm_header_title.setFrameShape(QFrame.StyledPanel)
        self.frm_header_title.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frm_header_title)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.title_header = QLabel(self.frm_header_title)
        self.title_header.setObjectName(u"title_header")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.title_header.setFont(font)

        self.horizontalLayout_3.addWidget(self.title_header)

        self.frm_dummy = QFrame(self.frm_header_title)
        self.frm_dummy.setObjectName(u"frm_dummy")
        self.frm_dummy.setMaximumSize(QSize(110, 16777215))
        self.frm_dummy.setFrameShape(QFrame.StyledPanel)
        self.frm_dummy.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_3.addWidget(self.frm_dummy)


        self.gridLayout.addWidget(self.frm_header_title, 0, 0, 1, 1)

        self.frm_header_buttons = QFrame(self.frm_header)
        self.frm_header_buttons.setObjectName(u"frm_header_buttons")
        self.frm_header_buttons.setMaximumSize(QSize(100, 16777215))
        self.frm_header_buttons.setLayoutDirection(Qt.LeftToRight)
        self.frm_header_buttons.setStyleSheet(u"\n"
"QPushButton {\n"
"	background-color: #203864;\n"
"	border-radius: 7px;	\n"
"	padding: 3px;\n"
"	selection-color: rgb(32, 56, 100);\n"
"}\n"
" \n"
"QPushButton:hover {\n"
"	background-color: #ff00ff;\n"
"}\n"
" \n"
"\n"
"QPushButton:pressed {\n"
"	background-color: #ff007f;\n"
"}\n"
"\n"
"QLabel{\n"
"	border: 0px;	\n"
"}")
        self.frm_header_buttons.setFrameShape(QFrame.StyledPanel)
        self.frm_header_buttons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frm_header_buttons)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(40, 3, 0, 0)
        self.btn_minimize = QPushButton(self.frm_header_buttons)
        self.btn_minimize.setObjectName(u"btn_minimize")
        self.btn_minimize.setMaximumSize(QSize(30, 30))
        self.btn_minimize.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/svg_icons/icon_minimize.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_minimize.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.btn_minimize, 0, Qt.AlignRight)

        self.btn_close = QPushButton(self.frm_header_buttons)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setMaximumSize(QSize(30, 30))
        self.btn_close.setCursor(QCursor(Qt.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/svg_icons/icon_close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.btn_close, 0, Qt.AlignRight)


        self.gridLayout.addWidget(self.frm_header_buttons, 0, 1, 1, 1, Qt.AlignVCenter)


        self.verticalLayout.addWidget(self.frm_header)

        self.frm_body = QFrame(self.frame_main)
        self.frm_body.setObjectName(u"frm_body")
        self.frm_body.setMinimumSize(QSize(0, 0))
        self.frm_body.setMaximumSize(QSize(16777215, 16777215))
        self.frm_body.setFrameShape(QFrame.StyledPanel)
        self.frm_body.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frm_body)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frm_left = QFrame(self.frm_body)
        self.frm_left.setObjectName(u"frm_left")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frm_left.sizePolicy().hasHeightForWidth())
        self.frm_left.setSizePolicy(sizePolicy2)
        self.frm_left.setMinimumSize(QSize(170, 0))
        self.frm_left.setFrameShape(QFrame.StyledPanel)
        self.frm_left.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frm_left)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frm_welcome = QFrame(self.frm_left)
        self.frm_welcome.setObjectName(u"frm_welcome")
        self.frm_welcome.setMinimumSize(QSize(0, 0))
        self.frm_welcome.setMaximumSize(QSize(16777215, 16777215))
        self.frm_welcome.setFrameShape(QFrame.StyledPanel)
        self.frm_welcome.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frm_welcome)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.lbl_welcome = QLabel(self.frm_welcome)
        self.lbl_welcome.setObjectName(u"lbl_welcome")
        sizePolicy3 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lbl_welcome.sizePolicy().hasHeightForWidth())
        self.lbl_welcome.setSizePolicy(sizePolicy3)
        self.lbl_welcome.setMinimumSize(QSize(0, 0))
        self.lbl_welcome.setMaximumSize(QSize(16777215, 16777215))
        self.lbl_welcome.setStyleSheet(u"color: rgb(218, 227, 243);")
        self.lbl_welcome.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.lbl_welcome)


        self.verticalLayout_3.addWidget(self.frm_welcome)

        self.frm_link_btn = QFrame(self.frm_left)
        self.frm_link_btn.setObjectName(u"frm_link_btn")
        sizePolicy.setHeightForWidth(self.frm_link_btn.sizePolicy().hasHeightForWidth())
        self.frm_link_btn.setSizePolicy(sizePolicy)
        self.frm_link_btn.setFrameShape(QFrame.StyledPanel)
        self.frm_link_btn.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frm_link_btn)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btn_docum_link = QPushButton(self.frm_link_btn)
        self.btn_docum_link.setObjectName(u"btn_docum_link")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.btn_docum_link.sizePolicy().hasHeightForWidth())
        self.btn_docum_link.setSizePolicy(sizePolicy4)
        self.btn_docum_link.setMinimumSize(QSize(80, 20))
        self.btn_docum_link.setMaximumSize(QSize(40, 20))
        self.btn_docum_link.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_docum_link.setStyleSheet(u"QPushButton#btn_docum_link {\n"
"	background-color: #2F5597;\n"
"	border-radius: 8px;	\n"
"	padding: 2px;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"\n"
"QPushButton:hover#btn_docum_link {\n"
"	background-color: #ff00ff;\n"
"}\n"
" \n"
"\n"
"QPushButton:pressed#btn_docum_link{\n"
"	background-color: #ff007f;\n"
"}\n"
"\n"
"\n"
"\n"
"color: rgb(218, 227, 243);")

        self.verticalLayout_5.addWidget(self.btn_docum_link)


        self.verticalLayout_3.addWidget(self.frm_link_btn, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.frm_status = QFrame(self.frm_left)
        self.frm_status.setObjectName(u"frm_status")
        self.frm_status.setMaximumSize(QSize(16777215, 0))
        self.frm_status.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.frm_status.setFrameShape(QFrame.StyledPanel)
        self.frm_status.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frm_status)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_2 = QLabel(self.frm_status)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_8.addWidget(self.label_2)

        self.label_3 = QLabel(self.frm_status)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_8.addWidget(self.label_3)

        self.label_5 = QLabel(self.frm_status)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_8.addWidget(self.label_5)

        self.label_4 = QLabel(self.frm_status)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_8.addWidget(self.label_4)

        self.label = QLabel(self.frm_status)
        self.label.setObjectName(u"label")

        self.verticalLayout_8.addWidget(self.label)

        self.label_7 = QLabel(self.frm_status)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_8.addWidget(self.label_7)


        self.verticalLayout_3.addWidget(self.frm_status)

        self.frm_verif = QFrame(self.frm_left)
        self.frm_verif.setObjectName(u"frm_verif")
        self.frm_verif.setMaximumSize(QSize(16777215, 0))
        self.frm_verif.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.frm_verif.setFrameShape(QFrame.StyledPanel)
        self.frm_verif.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frm_verif)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.lbl_verification_return = QLabel(self.frm_verif)
        self.lbl_verification_return.setObjectName(u"lbl_verification_return")
        self.lbl_verification_return.setAlignment(Qt.AlignCenter)
        self.lbl_verification_return.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.lbl_verification_return)


        self.verticalLayout_3.addWidget(self.frm_verif)

        self.verticalSpacer = QSpacerItem(20, 212, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.frm_footer = QFrame(self.frm_left)
        self.frm_footer.setObjectName(u"frm_footer")
        sizePolicy1.setHeightForWidth(self.frm_footer.sizePolicy().hasHeightForWidth())
        self.frm_footer.setSizePolicy(sizePolicy1)
        self.frm_footer.setFrameShape(QFrame.StyledPanel)
        self.frm_footer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frm_footer)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(3, 3, 3, 3)
        self.lbl_footer = QLabel(self.frm_footer)
        self.lbl_footer.setObjectName(u"lbl_footer")
        self.lbl_footer.setStyleSheet(u"color: rgb(143, 170, 220);")

        self.verticalLayout_6.addWidget(self.lbl_footer)


        self.verticalLayout_3.addWidget(self.frm_footer)


        self.horizontalLayout.addWidget(self.frm_left)

        self.frm_right = QFrame(self.frm_body)
        self.frm_right.setObjectName(u"frm_right")
        self.frm_right.setStyleSheet(u"QFrame {\n"
"	/*border: 1px solid #B4C7E7;*/\n"
"    border-radius: 20px;\n"
"   	padding: 1px;\n"
"	background-color: #B4C7E7;\n"
"\n"
"}\n"
"\n"
"")
        self.frm_right.setFrameShape(QFrame.StyledPanel)
        self.frm_right.setFrameShadow(QFrame.Raised)
        self.frm_right.setLineWidth(0)
        self.verticalLayout_2 = QVBoxLayout(self.frm_right)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frm_gif = QFrame(self.frm_right)
        self.frm_gif.setObjectName(u"frm_gif")
        sizePolicy.setHeightForWidth(self.frm_gif.sizePolicy().hasHeightForWidth())
        self.frm_gif.setSizePolicy(sizePolicy)
        self.frm_gif.setMinimumSize(QSize(0, 0))
        self.frm_gif.setMaximumSize(QSize(16777215, 16777215))
        self.frm_gif.setAcceptDrops(True)
        self.frm_gif.setLayoutDirection(Qt.LeftToRight)
        self.frm_gif.setStyleSheet(u"\n"
"background-color: rgb(0, 0, 0);\n"
"border-color: #B4C7E7;")
        self.frm_gif.setFrameShape(QFrame.StyledPanel)
        self.frm_gif.setFrameShadow(QFrame.Plain)
        self.gif_layout = QVBoxLayout(self.frm_gif)
        self.gif_layout.setSpacing(0)
        self.gif_layout.setObjectName(u"gif_layout")
        self.gif_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.frm_gif)

        self.frm_button = QFrame(self.frm_right)
        self.frm_button.setObjectName(u"frm_button")
        sizePolicy1.setHeightForWidth(self.frm_button.sizePolicy().hasHeightForWidth())
        self.frm_button.setSizePolicy(sizePolicy1)
        self.frm_button.setStyleSheet(u"")
        self.frm_button.setFrameShape(QFrame.StyledPanel)
        self.frm_button.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frm_button)
        self.verticalLayout_7.setSpacing(2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.btn_run = QPushButton(self.frm_button)
        self.btn_run.setObjectName(u"btn_run")
        self.btn_run.setMinimumSize(QSize(0, 40))
        self.btn_run.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_run.setStyleSheet(u"")
        self.btn_run.setFlat(True)

        self.verticalLayout_7.addWidget(self.btn_run, 0, Qt.AlignBottom)

        self.btn_open_folder = QPushButton(self.frm_button)
        self.btn_open_folder.setObjectName(u"btn_open_folder")
        self.btn_open_folder.setMinimumSize(QSize(0, 40))
        self.btn_open_folder.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_open_folder.setStyleSheet(u"")
        self.btn_open_folder.setFlat(True)

        self.verticalLayout_7.addWidget(self.btn_open_folder)


        self.verticalLayout_2.addWidget(self.frm_button)


        self.horizontalLayout.addWidget(self.frm_right)


        self.verticalLayout.addWidget(self.frm_body)

        MainWindow.setCentralWidget(self.frame_main)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.title_header.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; color:#ffffff;\">Py-AutoFab</span></p></body></html>", None))
        self.btn_minimize.setText("")
        self.btn_close.setText("")
        self.lbl_welcome.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-family:'Calibri'; font-size:10pt; color:#dae3f3;\">Welcome, User!</span></p><p align=\"center\"><span style=\" font-size:10pt; color:#dae3f3;\"><br/></span><span style=\" font-family:'Calibri'; font-size:10pt; color:#dae3f3;\">The purpose of this app is to automate the listing of THFL for Cableways thru transforming the extracted data from the attributed blocks of the CAD file.</span><span style=\" color:#dae3f3;\"><br/></span></p><p align=\"center\"><span style=\" font-family:'Calibri'; font-size:10pt; color:#dae3f3;\">For the full documentation, kindly click the button below.</span></p></body></html>", None))
        self.btn_docum_link.setText(QCoreApplication.translate("MainWindow", u"link.", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Input Verification", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Tray & Bracket", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Hanger", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Merging", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"THFL", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Material List", None))
        self.lbl_verification_return.setText(QCoreApplication.translate("MainWindow", u"Input Verification Return", None))
        self.lbl_footer.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"right\"><span style=\" font-size:8pt;\">Developed by: Jayver Lendio</span></p></body></html>", None))
        self.btn_run.setText(QCoreApplication.translate("MainWindow", u"Go", None))
        self.btn_open_folder.setText(QCoreApplication.translate("MainWindow", u"Open output folder", None))
    # retranslateUi

