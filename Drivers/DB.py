import os, sys, sqlite3
from pathlib import Path
from getpass import getuser
from time import time


class Providers():

    def __init__(self):
        if sys.platform.startswith('linux'):
            path_cliente = Path.home().joinpath('Documentos', 'Oficina',
                                                'Clientes', 'clientes.sqlite')
            path_estoque = Path.home().joinpath('Documentos', 'Oficina',
                                                'Estoque', 'estoque.sqlite')
        elif sys.platform.startswith('win'):
            path_cliente = Path.home().joinpath('Documents', 'Oficina',
                                                'Clientes', 'clientes.sqlite')
            path_estoque = Path.home().joinpath('Documentos', 'Oficina',
                                                'Estoque', 'estoque.sqlite')

        self.db_cliente = sqlite3.connect(str(path_cliente),
                                          detect_types=sqlite3.PARSE_DECLTYPES)
        self.db_cliente.row_factory = sqlite3.Row
        self.db_estoque = sqlite3.connect(str(path_estoque),
                                          detect_types=sqlite3.PARSE_DECLTYPES)
        self.db_estoque.row_factory = sqlite3.Row

    def busca_cliente(self, word: str) -> dict:
        search_word = "%{0}%".format(word)
        info = self.db_cliente.execute(
            "SELECT * FROM cliente WHERE nome LIKE ? ORDER BY id",
            (search_word,)).fetchone()
        return info

    def busca_peca(self, word: str) -> dict:
        data = self.db_estoque.execute("SELECT * FROM estoque WHERE code = ?",
                                       (word,)).fetchone()
        return data

    def get_id_peca(self, code: str) -> int:
        id = self.db_estoque.execute("SELECT id FROM estoque WHERE code = ?",
                                     (code,)).fetchone()
        return id["id"]

    def get_id_cliente(self, cpf: str) -> int:
        id = self.db_estoque.execute("SELECT id FROM cliente WHERE cpf = ?",
                                     (cpf,)).fetchone()
        return id["id"]

    def atualizacao_venda(self, data: dict):
        id = self.get_id_peca(data["code"])
        self.db_estoque.execute(
            "INSERT INTO tracker (codeid, time, delta) VALUES (?, ?, ?)",
            (id, int(time()), -data["qty"]),
        )
        old_data = dict(
            self.db_estoque.execute(
                "SELECT quantidade FROM estoque WHERE id = ?",
                (id,),
            ).fetchone())
        old_data["quantidade"] -= data["qty"]
        self.db_estoque.execute(
            "UPDATE estoque SET quantidade = ? WHERE id = ?",
            (old_data["quantidade"], id),
        )
        self.db_estoque.commit()
