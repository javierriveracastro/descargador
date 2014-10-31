# coding=utf-8
"""
Descargardor de Umbria, programa para descargar partidas de:

http://www.comunidadumbria.com

(c) 2013 Javier Rivera
"""

import sys

from PyQt4 import QtGui, QtCore

from UmbriaDescargar.DescargarUi import Ui_MainWindow
from UmbriaDescargar.Umbria import Partida, PartidaPruebas
from UmbriaDescargar.UmbriaTex import GeneradorText

# TODO: Icono del programa
# TODO: Control de errores de conexión
# TODO: Refactorizar la pantalla de progreso, cambiar por algo más elegante.
#   Como por ejemplo un metodo de Principal y un callback. Y con más detalle
# TODO: Opcion de no descargar notas
# TODO: Limpiar los temporales


class Principal(QtGui.QMainWindow, object):
    """
    Ventana principal de la aplicacion
    """

    def __init__(self, pruebas=False):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushConectar.clicked.connect(self.cargar_partida)
        self.ui.btnPdf.clicked.connect(self.genera_pdf)
        self.partida = None
        self.pruebas = pruebas

    def cargar_partida(self):
        """
        Se conecta a Umbria y carga una partida.
        """
        if not self.pruebas:
            self.partida = Partida(self.ui.editCodigoPartida.text(),
                                   self.ui.editUsuario.text(),
                                   self.ui.editContrasena.text())
        else:
            self.partida = PartidaPruebas("", "", "")
        self.ui.labelTituloPartida.setText(self.partida.titulo)
        self.ui.listWidget.clear()
        for escena in self.partida.escenas:
            novo_item = QtGui.QListWidgetItem(escena.titulo)
            novo_item.setCheckState(QtCore.Qt.Checked)
            self.ui.listWidget.addItem(novo_item)
        self.ui.btnPdf.setEnabled(True)

    def genera_pdf(self):
        """
        Genera un pdf de la partida seleccionada
        """
        # Buscar las partidas seleccionadas
        self.partida.escenas_seleccionadas = []
        for escena in self.partida.escenas:
            item = self.ui.listWidget.findItems(escena.titulo,
                                                QtCore.Qt.MatchExactly)
            if item[0].checkState():
                self.partida.escenas_seleccionadas.append(escena)
        print(self.partida.escenas_seleccionadas)
        # Pedir una ruta donde guardar la partida
        # noinspection PyCallByClass,PyTypeChecker
        nome_dir = QtGui.QFileDialog.getExistingDirectory(
            self, "Guardar partida", "~", QtGui.QFileDialog.ShowDirsOnly)
        # LLamar a proceso de generacion de verdad
        GeneradorText(nome_dir, self.partida)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ventana = Principal(pruebas="--test" in sys.argv)
    ventana.show()
    sys.exit(app.exec_())
