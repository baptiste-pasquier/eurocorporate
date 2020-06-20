import win32com.client as win32
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir, QSettings, pyqtSlot, QStandardPaths, QTemporaryDir, Qt
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QProgressDialog
from PyPDF2 import PdfFileMerger

from Gestionnaires.GestionnaireEtatUI import Ui_MainWindowEtat
from Tools.message import detailed_message
import pythoncom


class MainWindowEtat(QtWidgets.QMainWindow, Ui_MainWindowEtat):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        Ui_MainWindowEtat.__init__(self)
        self.setupUi(self)

    def init(self, clientChoisi, portefeuilleChoisi, dateChoisie):
        self.client = clientChoisi
        self.portefeuille = portefeuilleChoisi
        self.date = dateChoisie

        self.tb_client.setText(str(self.client.noClient) + " - " + self.client.nomEntreprise)
        self.tb_portefeuille.setText(str(self.portefeuille.noPortefeuille) + " - " + self.portefeuille.nomPortefeuille)
        self.tb_date.setText(self.date.toString("dd/MM/yyyy"))

        self.strNoPort = str(portefeuilleChoisi.noPortefeuille)
        self.strDate = dateChoisie.toString("MM/dd/yyyy")
        self.legendePort = portefeuilleChoisi.nomPortefeuille.strip()

        settings = QSettings()
        self.fileBDD = settings.value("BDD")

        # Bouton exigcap
        # query = QtSql.QSqlQuery()
        # query.exec("UPDATE Obligation SET ExigenceCap = null WHERE noSousSecteur=1 OR noSousSecteur=2 OR noSousSecteur=3 OR noSousSecteur=4 OR noSousSecteur=5 OR noSousSecteur=6 OR noSousSecteur=7 OR noSousSecteur=8 OR noSousSecteur=9 OR noSousSecteur=10 OR noSousSecteur=11 OR noSousSecteur=12 OR noSousSecteur=13 OR noSousSecteur=14 OR noSousSecteur=15 OR noSousSecteur=16 OR noSousSecteur=17 OR noSousSecteur=18 OR noSousSecteur=19 OR noSousSecteur=20 OR noSousSecteur=21 OR noSousSecteur=22 OR noSousSecteur=23 OR noSousSecteur=24 OR noSousSecteur=25 OR noSousSecteur=26 OR noSousSecteur=27 OR noSousSecteur=28 OR noSousSecteur=29 OR noSousSecteur=30 OR noSousSecteur=32 OR noSousSecteur=33 OR noSousSecteur=34 OR noSousSecteur=35 OR noSousSecteur=36 OR noSousSecteur=37 OR noSousSecteur=38 OR noSousSecteur=51;")
        # query.exec("UPDATE Obligation SET ExigenceCap = 0 WHERE noSousSecteur=39 OR noSousSecteur=40 OR noSousSecteur=41 OR noSousSecteur=42 OR noSousSecteur=43 OR noSousSecteur=44 OR noSousSecteur=45 OR noSousSecteur=46 OR noSousSecteur=47 OR noSousSecteur=48 OR noSousSecteur=49 OR noSousSecteur=50")
        # query.clear()

    def Etat(self, nomEtat, action, fileName=""):
        try:
            whereCondition = "[noPortefeuille] = " + self.strNoPort + " AND DateDeMAJ = #" + self.strDate + "#"

            # Ouverture de la base de données
            acc = win32.gencache.EnsureDispatch('Access.Application')
            acc.OpenCurrentDatabase(self.fileBDD, True)

            acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewReport, None, whereCondition)

            acc.Reports.Item(nomEtat).Controls.Item("txt_nomportefeuille").Caption = self.legendePort
            acc.Reports.Item(nomEtat).Controls.Item("txt_datemaj").Caption = "Mise à jour le " + self.date.toString("dd/MM/yyyy")

            if action == "Ouvrir":
                # acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewPreview, None, whereCondition)
                acc.DoCmd.Maximize()
                acc.Visible = True

            if action == "PDF":
                if fileName:
                    acc.DoCmd.OutputTo(win32.constants.acOutputReport, nomEtat, win32.constants.acFormatPDF, fileName)
                else:
                    acc.DoCmd.OutputTo(win32.constants.acOutputReport, nomEtat, win32.constants.acFormatPDF)
                acc.Quit()
        except pythoncom.com_error as error:
            detailed_message(self, QMessageBox.Critical, "Erreur Access", "Ouverture impossible. Merci de vérifier que la base de données n'est pas ouverte.", str(error))

    def Graphique(self, nomEtat, nomGraphique, sourceSQL, action, fileName=''):
        try:
            # Ouverture de la base de données
            acc = win32.gencache.EnsureDispatch('Access.Application')
            acc.OpenCurrentDatabase(self.fileBDD, True)

            acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewReport)

            acc.Reports.Item(nomEtat).Controls.Item(nomGraphique).RowSource = sourceSQL
            acc.Reports.Item(nomEtat).Controls.Item("txt_nomportefeuille").Caption = self.legendePort
            acc.Reports.Item(nomEtat).Controls.Item("txt_datemaj").Caption = "Mise à jour le " + self.date.toString("dd/MM/yyyy")
            # champs dlm

            if action == "Ouvrir":
                # acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewPreview, None, whereCondition)
                acc.DoCmd.Maximize()
                acc.Visible = True

            if action == "PDF":
                if fileName:
                    acc.DoCmd.OutputTo(win32.constants.acOutputReport, nomEtat, win32.constants.acFormatPDF, fileName)
                else:
                    acc.DoCmd.OutputTo(win32.constants.acOutputReport, nomEtat, win32.constants.acFormatPDF)
                acc.Quit()
        except pythoncom.com_error as error:
            detailed_message(None, QMessageBox.Critical, "Erreur Access", "Ouverture impossible. Merci de vérifier que la base de données n'est pas ouverte.", str(error))

    @pyqtSlot()
    def on_btn_echeplus_clicked(self):
        self.Etat("EchéancierValue", "Ouvrir")

    @pyqtSlot()
    def on_btn_echeplusPDF_clicked(self):
        self.Etat("EchéancierValue", "PDF")

    @pyqtSlot()
    def on_btn_echeancier_clicked(self):
        self.Etat("Echéancier", "Ouvrir")

    @pyqtSlot()
    def on_btn_echeancierPDF_clicked(self):
        self.Etat("Echéancier", "PDF")

    @pyqtSlot()
    def on_btn_exigence_clicked(self):
        self.Etat("ExigenceCapital", "Ouvrir")

    @pyqtSlot()
    def on_btn_exigencePDF_clicked(self):
        self.Etat("ExigenceCapital", "PDF")

    @pyqtSlot()
    def on_btn_emetteur_clicked(self):
        self.Etat("Libelle", "Ouvrir")

    @pyqtSlot()
    def on_btn_emetteurPDF_clicked(self):
        self.Etat("Libelle", "PDF")

    @pyqtSlot()
    def on_btn_PDF_clicked(self):
        resultFileName = QFileDialog.getSaveFileName(self, "Save File", QDir(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)).filePath('exportation.pdf'),
                                                     "PDF (*.pdf)")[0]
        if resultFileName:
            list_cb_checked = [self.cb_echeplus.isChecked(), self.cb_echeancier.isChecked(), self.cb_exigence.isChecked(), self.cb_emetteur.isChecked(), 
                               self.cb_histoType.isChecked(), self.cb_gType.isChecked(), self.cb_gRating.isChecked(), self.cb_gSecteur.isChecked(),
                               self.cb_gGovnt.isChecked(), self.cb_gCorp.isChecked(), self.cb_gFin.isChecked(), self.cb_synthese.isChecked()]
            nb_checked = sum(list_cb_checked)
            nb_pdfs = nb_checked
            if nb_checked == 0:
                nb_pdfs = len(list_cb_checked)

            progress = QProgressDialog("Exportation PDF", "Annuler", 0, nb_pdfs, self)
            progress.setWindowTitle("Générations des états")
            progress.setWindowModality(Qt.WindowModal)
            progress.show()

            tempdir = QTemporaryDir()

            def file(i):
                return tempdir.filePath("{}.pdf".format(i)).replace("/", "\\")
            i = 0
            if self.cb_echeplus.isChecked() or nb_checked == 0:
                self.Etat("EchéancierValue", "PDF", fileName=file(i))
                i += 1
                progress.setValue(i)
            if self.cb_echeancier.isChecked() or nb_checked == 0:
                self.Etat("Echéancier", "PDF", fileName=file(i))
                i += 1
                progress.setValue(i)
            if self.cb_exigence.isChecked() or nb_checked == 0:
                self.Etat("ExigenceCapital", "PDF", fileName=file(i))
                i += 1
                progress.setValue(i)
            if self.cb_emetteur.isChecked() or nb_checked == 0:
                self.Etat("Libelle", "PDF", fileName=file(i))
                i += 1
                progress.setValue(i)

            pdfs = [file(j) for j in range(0, i)]
            merger = PdfFileMerger()
            for pdf in pdfs:
                merger.append(pdf)
            try:
                merger.write(resultFileName)
            except Exception as e:
                detailed_message(self, QMessageBox.Critical, "Exportation PDF", "Echec de l'écriture du fichier PDF", str(e))
            merger.close()

            QMessageBox.information(self, "Exportation PDF", "Exportation terminée")


# def on_btn_emetteurPDF_clicked(self):
#         # self.Etat("Libelle", "PDF")
#         tempdir = QTemporaryDir()
#         print(tempdir.path())
#         # print(tempdir.isValid())
#         # print(tempdir.filePath("1.pdf"))
#         self.Etat("Libelle", "PDF", fileName=tempdir.filePath("1.pdf").replace("/", "\\"))
#         print('bonjour')
