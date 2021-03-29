import csv
from datetime import date


class Vendas():

    def __init__(self):
        self.arquivo = 'vendas.csv'
        self.fieldnames = [
            'nome', 'numero', 'cpf', 'modelo', 'placa', 'km', 'data', 'total', 'pecas',
            'servico'
        ]

    def show_all(self):
        with open(self.arquivo, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            lista_linhas = list(reader)
        return lista_linhas

    def search_name(self, word: str) -> list:
        lista_linhas = []
        with open(self.arquivo, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['nome'] == word:
                    lista_linhas.append(row)

        return lista_linhas

    def search_date(self, date1: str, date2: str) -> list:
        lista_linhas = []
        date1 = date.fromisocalendar(date1)
        date2 = date.fromisocalendar(date2)
        with open(self.arquivo, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data = date.fromisocalendar(row['data'])
                if date1 < data < date2:
                    lista_linhas.append(row)
        return lista_linhas

    def add(self, data: dict):
        with open(self.arquivo, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(data)


def init_vendas():
    with open('vendas.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'nome', 'numero', 'cpf', 'modelo', 'placa', 'km', 'total', 'data', 'pecas',
            'servico'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


if __name__ == "__main__":
    init_vendas()