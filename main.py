# -*- coding: utf-8 -*-
import sys
from PySide6.QtCore import Slot, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QMessageBox,
    QApplication,
    QLabel,
    QGridLayout,
    QWidget,
    QFrame,
    QSizePolicy,
)
from Gui import VendasWidget, AdicionarPeçasWidget


class Principal(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Tião Automecânica - Vendas")
        self.widget = QWidget()

        # Janela
        self.principal = VendasWidget()
        self.principal.signal_status.connect(self.atualizar_status)
        self.principal.signal_itens.connect(self.adicionar_itens)
        self.setCentralWidget(self.principal)

        # Menu
        self.menu = QMenuBar()
        self.setMenuBar(self.menu)
        self.sobre = QAction("Sobre", self)
        self.sobre.setShortcut("F1")
        self.menu.addAction(self.sobre)
        self.sobre.triggered.connect(self.info)

        # Status
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status_label = QLabel("Pronto")
        self.status.addWidget(self.status_label)

    @Slot()
    def info(self):
        self.popup = QMessageBox(QMessageBox.Information, "Sobre",
                                 "Informações")
        self.popup.setInformativeText("""Suite de Apoio \nVersão 0.2
        \nFeito com S2 por Zero \nMIT License""")
        self.popup.addButton(QMessageBox.Ok)
        self.popup.exec()

    @Slot()
    def atualizar_status(self, msg: str):
        self.status_label.setText(msg)

    @Slot()
    def adicionar_itens(self):
        self.itens_janela = AdicionarPeçasWidget()
        self.itens_janela.setWindowTitle('Peças')
        self.itens_janela.signal_data.connect(self.principal.adicionar_itens)
        self.itens_janela.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Principal()
    window.showMaximized()
    sys.exit(app.exec_())