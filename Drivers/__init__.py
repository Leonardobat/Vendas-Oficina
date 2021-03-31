import csv, os, sys
from pathlib import Path
from datetime import date


def init_vendas():
    path = Path.home()
    fieldnames = [
        'nome', 'numero', 'cpf', 'endereco', 'modelo', 'placa', 'km', 'total',
        'data', 'pecas', 'servico'
    ]

    if sys.platform.startswith('linux'):
        path = path.joinpath('Documentos', 'Oficina', 'Vendas', 'vendas.csv')

    elif sys.platform.startswith('win'):
        path = path.joinpath('Documents', 'Oficina', 'Vendas', 'vendas.csv')

    if not Path.is_file(path):
        Path.mkdir(path.parent, parents=True, exist_ok=True)
        with Path.open(path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    return path, fieldnames


class Vendas():

    def __init__(self):
        self.path, self.fieldnames = init_vendas()

    def show_all(self):
        with open(self.path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            lista_linhas = list(reader)
        return lista_linhas

    def search_name(self, word: str) -> list:
        lista_linhas = []
        with open(self.path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['nome'] == word:
                    lista_linhas.append(row)

        return lista_linhas

    def search_date(self, date1: str, date2: str) -> list:
        lista_linhas = []
        date1 = date.fromisocalendar(date1)
        date2 = date.fromisocalendar(date2)
        with open(self.path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data = date.fromisocalendar(row['data'])
                if date1 < data < date2:
                    lista_linhas.append(row)
        return lista_linhas

    def add(self, data: dict):
        with open(self.path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(data)


if __name__ == "__main__":
    init_vendas()