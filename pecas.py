from PySide2.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                               QDoubleSpinBox, QVBoxLayout, QHBoxLayout,
                               QSpinBox, QMessageBox)
from PySide2.QtCore import Slot, Signal
from PySide2.QtGui import QFont
from DB import driver_db


class Janela_Pecas(QWidget):
    signal_data = Signal(dict)

    def __init__(self):
        QWidget.__init__(self)
        Font = QFont()
        Font.setBold(True)
        self.db = driver_db()

        # Labels:
        self.label_code = QLabel('Código:')
        self.label_code.setFont(Font)
        self.label_nome = QLabel('Nome:')
        self.label_nome.setFont(Font)
        self.label_qty = QLabel('Quantidade:')
        self.label_qty.setFont(Font)
        self.label_valor_un = QLabel('Valor Unitário:')
        self.label_valor_un.setFont(Font)
        self.label_valor = QLabel('Valor:')
        self.label_valor.setFont(Font)

        # Entries:
        self.entry_code = QLineEdit()
        self.entry_nome = QLineEdit()
        self.entry_nome.setReadOnly(True)
        self.entry_qty = QSpinBox()
        self.entry_qty.setEnabled(False)
        self.entry_qty.setValue(1)
        self.entry_qty.valueChanged.connect(self.atualizar_valor)
        self.entry_valor_un = QDoubleSpinBox()
        self.entry_valor_un.setMaximum(9999)
        self.entry_valor_un.setPrefix("R$ ")
        self.entry_valor_un.setReadOnly(True)
        self.entry_valor = QDoubleSpinBox()
        self.entry_valor.setMaximum(9999)
        self.entry_valor.setPrefix("R$ ")
        self.entry_valor.setReadOnly(True)

        # Botões:
        self.button_buscar = QPushButton("&Buscar")
        self.button_buscar.clicked.connect(self.buscar)
        self.button_buscar.setShortcut("Ctrl+B")
        self.button_adicionar = QPushButton("&Adicionar")
        self.button_adicionar.clicked.connect(self.adicionar)
        self.button_adicionar.setShortcut("Ctrl+S")

        # Leiaute:
        self.layout = QVBoxLayout()
        self.layout_busca = QHBoxLayout()
        self.layout.addWidget(self.label_code)
        self.layout_busca.addWidget(self.entry_code)
        self.layout_busca.addWidget(self.button_buscar)
        self.layout.addLayout(self.layout_busca)
        self.layout.addWidget(self.label_nome)
        self.layout.addWidget(self.entry_nome)
        self.layout.addWidget(self.label_valor_un)
        self.layout.addWidget(self.entry_valor_un)
        self.layout.addWidget(self.label_qty)
        self.layout.addWidget(self.entry_qty)
        self.layout.addWidget(self.label_valor)
        self.layout.addWidget(self.entry_valor)
        self.layout.addWidget(self.button_adicionar)
        self.setLayout(self.layout)

    @Slot()
    def adicionar(self):
        code = self.entry_code.text()
        nome = self.entry_nome.text()
        if nome == '':
            self.buscar()
            nome = self.entry_nome.text()
        qty = self.entry_qty.value()
        valor_un = self.entry_valor_un.value()
        data = {
            'code': code,
            'nome': nome,
            'qty': str(qty),
            'valor_un': str(valor_un),
            'valor': valor_un * qty,
        }
        if qty > self.data['quantidade']:
            self.alerta('Estoque insuficiente')
        elif qty <= 0:
            self.alerta('Quantidade Inválida')
        else:
            self.signal_data.emit(data)
            self.close()

    @Slot()
    def buscar(self):
        code = self.entry_code.text()
        self.data = self.db.busca_peca(code)
        if self.data is not None:
            self.entry_nome.setText(self.data['nome'])
            self.entry_valor_un.setValue(self.data['preco_venda'])
            self.entry_qty.setEnabled(True)
            self.atualizar_valor()

    @Slot()
    def atualizar_valor(self):
        qty = self.entry_qty.value()
        valor_un = self.entry_valor_un.value()
        if valor_un > 0:
            self.entry_valor.setValue(qty * valor_un)

    @Slot()
    def alerta(self, msg: str):
        popup = QMessageBox(QMessageBox.Warning, 'Erro', msg)
        popup.exec()
