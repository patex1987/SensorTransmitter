# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_design.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_frm_main(object):
    def setupUi(self, frm_main):
        frm_main.setObjectName(_fromUtf8("frm_main"))
        frm_main.resize(899, 721)
        self.gridLayout = QtGui.QGridLayout(frm_main)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.btn_Start = QtGui.QPushButton(frm_main)
        self.btn_Start.setObjectName(_fromUtf8("btn_Start"))
        self.verticalLayout_4.addWidget(self.btn_Start)
        self.btn_Stop = QtGui.QPushButton(frm_main)
        self.btn_Stop.setObjectName(_fromUtf8("btn_Stop"))
        self.verticalLayout_4.addWidget(self.btn_Stop)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.lbl_Temp_Title = QtGui.QLabel(frm_main)
        self.lbl_Temp_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_Temp_Title.setObjectName(_fromUtf8("lbl_Temp_Title"))
        self.verticalLayout.addWidget(self.lbl_Temp_Title)
        self.lbl_Temp_Value = QtGui.QLabel(frm_main)
        self.lbl_Temp_Value.setFrameShape(QtGui.QFrame.Box)
        self.lbl_Temp_Value.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_Temp_Value.setObjectName(_fromUtf8("lbl_Temp_Value"))
        self.verticalLayout.addWidget(self.lbl_Temp_Value)
        self.gr_Temperature = QtGui.QGraphicsView(frm_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gr_Temperature.sizePolicy().hasHeightForWidth())
        self.gr_Temperature.setSizePolicy(sizePolicy)
        self.gr_Temperature.setObjectName(_fromUtf8("gr_Temperature"))
        self.verticalLayout.addWidget(self.gr_Temperature)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.lbl_Heat_Title = QtGui.QLabel(frm_main)
        self.lbl_Heat_Title.setObjectName(_fromUtf8("lbl_Heat_Title"))
        self.verticalLayout_3.addWidget(self.lbl_Heat_Title)
        self.gr_Heat_State = QtGui.QGraphicsView(frm_main)
        self.gr_Heat_State.setObjectName(_fromUtf8("gr_Heat_State"))
        self.verticalLayout_3.addWidget(self.gr_Heat_State)
        self.lbl_Cooling = QtGui.QLabel(frm_main)
        self.lbl_Cooling.setObjectName(_fromUtf8("lbl_Cooling"))
        self.verticalLayout_3.addWidget(self.lbl_Cooling)
        self.gr_Cooling_state = QtGui.QGraphicsView(frm_main)
        self.gr_Cooling_state.setObjectName(_fromUtf8("gr_Cooling_state"))
        self.verticalLayout_3.addWidget(self.gr_Cooling_state)
        self.lbl_Ao1 = QtGui.QLabel(frm_main)
        self.lbl_Ao1.setObjectName(_fromUtf8("lbl_Ao1"))
        self.verticalLayout_3.addWidget(self.lbl_Ao1)
        self.gr_Venting = QtGui.QGraphicsView(frm_main)
        self.gr_Venting.setObjectName(_fromUtf8("gr_Venting"))
        self.verticalLayout_3.addWidget(self.gr_Venting)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 3, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.lbl_Lower_Temp_Title = QtGui.QLabel(frm_main)
        self.lbl_Lower_Temp_Title.setObjectName(_fromUtf8("lbl_Lower_Temp_Title"))
        self.verticalLayout_5.addWidget(self.lbl_Lower_Temp_Title)
        self.inp_Lower_Temp = QtGui.QLineEdit(frm_main)
        self.inp_Lower_Temp.setEnabled(True)
        self.inp_Lower_Temp.setObjectName(_fromUtf8("inp_Lower_Temp"))
        self.verticalLayout_5.addWidget(self.inp_Lower_Temp)
        self.lbl_Upper_Temp_Title = QtGui.QLabel(frm_main)
        self.lbl_Upper_Temp_Title.setObjectName(_fromUtf8("lbl_Upper_Temp_Title"))
        self.verticalLayout_5.addWidget(self.lbl_Upper_Temp_Title)
        self.inp_Upper_Temp = QtGui.QLineEdit(frm_main)
        self.inp_Upper_Temp.setEnabled(True)
        self.inp_Upper_Temp.setObjectName(_fromUtf8("inp_Upper_Temp"))
        self.verticalLayout_5.addWidget(self.inp_Upper_Temp)
        self.btn_Apply_Limit = QtGui.QPushButton(frm_main)
        self.btn_Apply_Limit.setEnabled(True)
        self.btn_Apply_Limit.setObjectName(_fromUtf8("btn_Apply_Limit"))
        self.verticalLayout_5.addWidget(self.btn_Apply_Limit)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.lbl_Humidity_Title = QtGui.QLabel(frm_main)
        self.lbl_Humidity_Title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_Humidity_Title.setObjectName(_fromUtf8("lbl_Humidity_Title"))
        self.verticalLayout_2.addWidget(self.lbl_Humidity_Title)
        self.lbl_Humidity_Value = QtGui.QLabel(frm_main)
        self.lbl_Humidity_Value.setFrameShape(QtGui.QFrame.Box)
        self.lbl_Humidity_Value.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_Humidity_Value.setObjectName(_fromUtf8("lbl_Humidity_Value"))
        self.verticalLayout_2.addWidget(self.lbl_Humidity_Value)
        self.gr_Humidity = QtGui.QGraphicsView(frm_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gr_Humidity.sizePolicy().hasHeightForWidth())
        self.gr_Humidity.setSizePolicy(sizePolicy)
        self.gr_Humidity.setObjectName(_fromUtf8("gr_Humidity"))
        self.verticalLayout_2.addWidget(self.gr_Humidity)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 2, 1, 1)

        self.retranslateUi(frm_main)
        QtCore.QMetaObject.connectSlotsByName(frm_main)

    def retranslateUi(self, frm_main):
        frm_main.setWindowTitle(_translate("frm_main", "Sensor processor", None))
        self.btn_Start.setText(_translate("frm_main", "Start measurement", None))
        self.btn_Stop.setText(_translate("frm_main", "Stop measurement", None))
        self.lbl_Temp_Title.setText(_translate("frm_main", "Actual temperature", None))
        self.lbl_Temp_Value.setText(_translate("frm_main", "TextLabel", None))
        self.lbl_Heat_Title.setText(_translate("frm_main", "Heating state", None))
        self.lbl_Cooling.setText(_translate("frm_main", "Cooling state", None))
        self.lbl_Ao1.setText(_translate("frm_main", "AO1 - air venting", None))
        self.lbl_Lower_Temp_Title.setText(_translate("frm_main", "Lower temperature limit", None))
        self.lbl_Upper_Temp_Title.setText(_translate("frm_main", "Upper temperature limit", None))
        self.btn_Apply_Limit.setText(_translate("frm_main", "Apply limits", None))
        self.lbl_Humidity_Title.setText(_translate("frm_main", "Actual humidity", None))
        self.lbl_Humidity_Value.setText(_translate("frm_main", "TextLabel", None))

