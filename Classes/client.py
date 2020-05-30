from PyQt5 import QtSql

class Client:
    def __init__(self):
        self.noClient = None
        self.nomEntreprise = None
        self.nomContact = None
        self.prenomContact = None
        self.mailContact = None

    def get_values(self):
        query = QtSql.QSqlQuery()
        query.exec("SELECT nomEntreprise, nomContact, prenomContact, mailContact, noClient FROM Client WHERE noClient = " + str(self.noClient))
        if query.next():
            self.nomEntreprise = str(query.value(0))
            self.nomContact = str(query.value(1))
            self.prenomContact = str(query.value(2))
            self.mailContact = str(query.value(3))
        query.clear()