# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/javier/Dropbox/Programas/spikes/DescargarUmbria/trunk/UmbriaDescargar/media/Descargar.ui'
#
# Created: Fri Oct 31 20:12:42 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(573, 430)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/Umbria/alyan_logo.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.editUsuario = QtGui.QLineEdit(self.frame)
        self.editUsuario.setObjectName(_fromUtf8("editUsuario"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.editUsuario)
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.editContrasena = QtGui.QLineEdit(self.frame)
        self.editContrasena.setEchoMode(QtGui.QLineEdit.Password)
        self.editContrasena.setObjectName(_fromUtf8("editContrasena"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.editContrasena)
        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.editCodigoPartida = QtGui.QLineEdit(self.frame)
        self.editCodigoPartida.setObjectName(_fromUtf8("editCodigoPartida"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.editCodigoPartida)
        self.verticalLayout.addLayout(self.formLayout)
        self.pushConectar = QtGui.QPushButton(self.frame)
        self.pushConectar.setObjectName(_fromUtf8("pushConectar"))
        self.verticalLayout.addWidget(self.pushConectar)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.frame)
        self.labelTituloPartida = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelTituloPartida.setFont(font)
        self.labelTituloPartida.setObjectName(_fromUtf8("labelTituloPartida"))
        self.verticalLayout_2.addWidget(self.labelTituloPartida)
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout_2.addWidget(self.listWidget)
        self.btnPdf = QtGui.QPushButton(self.centralwidget)
        self.btnPdf.setEnabled(False)
        self.btnPdf.setObjectName(_fromUtf8("btnPdf"))
        self.verticalLayout_2.addWidget(self.btnPdf)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Descargar de Umbria", None))
        self.label_2.setText(_translate("MainWindow", "Descargador de partidas de Umbria", None))
        self.label_3.setText(_translate("MainWindow", "Usuario:", None))
        self.label_4.setText(_translate("MainWindow", "Contraseña", None))
        self.label_5.setText(_translate("MainWindow", "Código Partida", None))
        self.pushConectar.setText(_translate("MainWindow", "Conectar a la partida", None))
        self.labelTituloPartida.setText(_translate("MainWindow", "Ninguna partida conectada", None))
        self.btnPdf.setText(_translate("MainWindow", "Genera Tex", None))

import Descargar_rc
