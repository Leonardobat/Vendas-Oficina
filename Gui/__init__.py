from PySide6.QtWidgets import (QWidget, QLabel, QComboBox, QLineEdit, QTextEdit,
                               QTableWidget, QPushButton, QHeaderView,
                               QTableWidgetItem, QVBoxLayout, QHBoxLayout,
                               QFrame, QGridLayout, QAbstractItemView, QWidget,
                               QDoubleSpinBox, QSpinBox, QMessageBox)
from PySide6.QtCore import Slot, Signal, Qt
from PySide6.QtGui import QFont
from Drivers.DB import Providers
from Drivers import Vendas
from datetime import date


class VendasWidget(QWidget):
    signal_status = Signal(str)
    signal_itens = Signal()

    def __init__(self):
        self.vendas = Vendas()
        self.db = Providers()
        QWidget.__init__(self)
        Font = QFont()
        Font.setBold(True)

        # Labels:
        self.label_nome = QLabel('Nome:')
        self.label_nome.setFont(Font)
        self.label_cpf = QLabel('CPF:')
        self.label_cpf.setFont(Font)
        self.label_numero = QLabel('Telefone:')
        self.label_numero.setFont(Font)
        self.label_placa = QLabel('Placa:')
        self.label_placa.setFont(Font)
        self.label_km = QLabel('Quilometragem:')
        self.label_km.setFont(Font)
        self.label_modelo = QLabel('Modelo:')
        self.label_modelo.setFont(Font)
        self.label_tabela = QLabel('Peças Utilizadas:')
        self.label_tabela.setFont(Font)
        self.label_total = QLabel('Total:')
        self.label_total.setFont(Font)
        self.label_servico = QLabel('Serviço:')
        self.label_servico.setFont(Font)

        # Lista de Modelos:
        self.combo_modelo = QComboBox()
        Modelos = ["Hilux", "Corolla", "SW4", "RAV", "Etios", "Outro"]
        for modelo in Modelos:
            self.combo_modelo.addItem(modelo)

        # Entradas:
        self.entry_nome = QLineEdit()
        self.entry_cpf = QLineEdit()
        self.entry_numero = QLineEdit()
        self.entry_placa = QLineEdit()
        self.entry_km = QLineEdit()
        self.entry_placa = QLineEdit()
        self.entry_total = QLineEdit()
        self.entry_total.setReadOnly(True)
        self.text_servico = QTextEdit()

        #Tabela das Peças:
        self.itens = 0
        self.tabela_pecas = QTableWidget()
        self.tabela_pecas.setColumnCount(5)
        self.tabela_pecas.setHorizontalHeaderLabels([
            "Código", "Nome", "Quantidade", "Preço Unitário (R$)",
            "Preço Total (R$)"
        ])
        self.tabela_pecas.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.tabela_pecas.resizeColumnsToContents()
        self.tabela_pecas.setEditTriggers(QAbstractItemView.NoEditTriggers)

        #Botões:
        self.button_salvar = QPushButton("&Salvar")
        self.button_salvar.clicked.connect(self.salvar)
        self.button_salvar.setShortcut("Ctrl+S")
        self.button_cliente = QPushButton("Buscar")
        self.button_cliente.setShortcut("Ctrl+F")
        self.button_cliente.clicked.connect(self.buscar_cliente)
        self.button_pecas = QPushButton("Adicionar P&eças")
        self.button_pecas.setShortcut("Ctrl+E")
        self.button_pecas.clicked.connect(self.exibir_janela)
        self.button_limpar_pecas = QPushButton("&Limpar Peças")
        self.button_limpar_pecas.setShortcut("Ctrl+L")
        self.button_limpar_pecas.clicked.connect(self.limpar_tabela)
        self.button_cancelar = QPushButton("Cancelar")
        self.button_cancelar.setShortcut("ESC")
        self.button_cancelar.clicked.connect(self.limpar)

        # Lado dos dados
        self.layout_Data = QVBoxLayout()
        self.layout_Data.addWidget(self.label_nome)
        self.layout_nome = QHBoxLayout()
        self.layout_nome.addWidget(self.entry_nome)
        self.layout_nome.addWidget(self.button_cliente)
        self.layout_Data.addLayout(self.layout_nome)
        self.layout_Data.addWidget(self.label_cpf)
        self.layout_Data.addWidget(self.entry_cpf)
        self.layout_Data.addWidget(self.label_numero)
        self.layout_Data.addWidget(self.entry_numero)
        self.layout_Data.addWidget(self.label_modelo)
        self.layout_Data.addWidget(self.combo_modelo)
        self.layout_Data.addWidget(self.label_placa)
        self.layout_Data.addWidget(self.entry_placa)
        self.layout_Data.addWidget(self.label_km)
        self.layout_Data.addWidget(self.entry_km)
        self.layout_Data.addWidget(self.label_servico)
        self.layout_Data.addWidget(self.text_servico)

        # Linha
        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setLineWidth(0)
        self.line.setMidLineWidth(1)

        # Lado das Peças
        self.layout_Pecas = QVBoxLayout()
        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.addWidget(self.button_pecas)
        self.layout_buttons.addWidget(self.button_limpar_pecas)
        self.layout_Pecas.addLayout(self.layout_buttons)
        self.layout_Pecas.addWidget(self.label_tabela)
        self.layout_Pecas.addWidget(self.tabela_pecas)
        self.layout_Pecas.addWidget(self.label_total)
        self.layout_total = QGridLayout()
        self.layout_total.addWidget(self.entry_total, 0, 0, 1, 2)
        self.layout_total.addWidget(self.button_salvar, 0, 2, 1, 1)
        self.layout_total.addWidget(self.button_cancelar, 0, 3, 1, 1)
        self.layout_Pecas.addLayout(self.layout_total)

        #Leiaute:
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.layout_Data)
        self.layout.addWidget(self.line)
        self.layout.addLayout(self.layout_Pecas)
        self.setLayout(self.layout)

    @Slot()
    def salvar(self):
        nome = self.entry_nome.text()
        numero = self.entry_numero.text()
        modelo = self.entry_nome.text()
        cpf = self.entry_cpf.text()
        placa = self.entry_placa.text()
        km = self.entry_km.text()
        servico = self.text_servico.toPlainText()
        total = self.entry_total.text()
        dia = str(date.today())
        pecas = []
        for i in range(self.itens):
            pecas.append({
                'code': self.tabela_pecas.item(i, 0).text(),
                'qty': int(self.tabela_pecas.item(i, 2).text()),
            })
        if pecas == []:
            pecas = ''

        data = {
            'nome': nome,
            'numero': numero,
            'modelo': modelo,
            'cpf': cpf,
            'placa': placa,
            'km': km,
            'data': dia,
            'total': total,
            'pecas': pecas,
            'servico': servico,
        }
        for peca in pecas:
            self.db.atualizacao_venda(peca)

        self.vendas.add(data)
        self.signal_status.emit('Salvo')

    @Slot()
    def exibir_janela(self):
        self.signal_itens.emit()

    @Slot()
    def adicionar_itens(self, item: dict):
        valor = self.entry_total.text()
        if valor == '':
            valor = 0
        else:
            valor = float(valor)
        self.entry_total.setText(str(item['valor'] + valor))
        code = QTableWidgetItem(item['code'])
        nome = QTableWidgetItem(item['nome'])
        qty = QTableWidgetItem(item['qty'])
        valor_un = QTableWidgetItem(item['valor_un'])
        valor = QTableWidgetItem(str(item['valor']))
        code.setTextAlignment(Qt.AlignCenter)
        nome.setTextAlignment(Qt.AlignCenter)
        qty.setTextAlignment(Qt.AlignCenter)
        valor_un.setTextAlignment(Qt.AlignCenter)
        valor.setTextAlignment(Qt.AlignCenter)
        exists = False

        for i in range(self.itens):
            code_table = self.tabela_pecas.item(i, 0).text()
            if code.text() == code_table:
                exists = True
                row = i
                break

        if exists:
            self.tabela_pecas.setItem(row, 0, code)
            self.tabela_pecas.setItem(row, 1, nome)
            self.tabela_pecas.setItem(row, 2, qty)
            self.tabela_pecas.setItem(row, 3, valor_un)
            self.tabela_pecas.setItem(row, 4, valor)
        else:
            self.tabela_pecas.insertRow(self.itens)
            self.tabela_pecas.setItem(self.itens, 0, code)
            self.tabela_pecas.setItem(self.itens, 1, nome)
            self.tabela_pecas.setItem(self.itens, 2, qty)
            self.tabela_pecas.setItem(self.itens, 3, valor_un)
            self.tabela_pecas.setItem(self.itens, 4, valor)
            self.itens += 1

    @Slot()
    def limpar_tabela(self):
        self.entry_valor.clear()
        self.tabela_pecas.clearContents()
        self.tabela_pecas.setRowCount(0)
        self.itens = 0

    @Slot()
    def limpar(self):
        self.limpar_tabela()
        self.entry_nome.clear()
        self.entry_numero.clear()
        self.entry_placa.clear()
        self.entry_cpf.clear()
        self.entry_km.clear()
        self.text_servico.clear()

    @Slot()
    def buscar_cliente(self):
        nome = self.entry_nome.text()
        data = self.db.busca_cliente(nome)
        if data != None:
            self.entry_nome.setText(data['nome'])
            self.entry_numero.setText(data['numero'])
            self.entry_cpf.setText(data['cpf'])


class AdicionarPeçasWidget(QWidget):
    signal_data = Signal(dict)

    def __init__(self):
        QWidget.__init__(self)
        Font = QFont()
        Font.setBold(True)
        self.db = Providers()

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
