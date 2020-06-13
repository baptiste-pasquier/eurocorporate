from PyQt5 import QtSql


class Obligation:
    def __init__(self):
        self.ISIN = None
        self.Libelle = None

    # def get_values(self):
    #     query = QtSql.QSqlQuery()
    #     query.exec("SELECT noClient, nomPortefeuille FROM Portefeuille WHERE noPortefeuille = "+str(self.noPortefeuille))
    #     if query.next():
    #         self.noClient = str(query.value(0))
    #         self.nomPortefeuille = str(query.value(1))
    #     query.clear()
