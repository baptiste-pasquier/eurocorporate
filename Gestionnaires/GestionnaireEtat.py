import win32com.client as win32
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir, QSettings, pyqtSlot, QStandardPaths, QTemporaryDir, QTimer
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyPDF2 import PdfFileMerger, PdfFileReader

from Gestionnaires.GestionnaireEtatUI import Ui_MainWindowEtat
from Tools.message import detailed_message
import pythoncom
import os


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
        self.tb_portefeuille.setText(str(self.portefeuille.noPortefeuille) + " - " + self.portefeuille.nomPortefeuille.strip())
        self.tb_date.setText(self.date.toString("dd/MM/yyyy"))

        self.strNoPort = str(portefeuilleChoisi.noPortefeuille)
        self.strDate = dateChoisie.toString("MM/dd/yyyy")
        self.legendePort = portefeuilleChoisi.nomPortefeuille.strip()

        settings = QSettings()
        self.fileBDD = settings.value("BDD")
        self.file_avertissement = settings.value("AVERTISSEMENT", defaultValue='')
        while self.file_avertissement == '':
            self.on_btn_config_av_clicked()

        # Bouton exigcap
        # query = QtSql.QSqlQuery()
        # query.exec("UPDATE Obligation SET ExigenceCap = null WHERE noSousSecteur=1 OR noSousSecteur=2 OR noSousSecteur=3 OR noSousSecteur=4 OR noSousSecteur=5 OR noSousSecteur=6 OR noSousSecteur=7 OR noSousSecteur=8 OR noSousSecteur=9 OR noSousSecteur=10 OR noSousSecteur=11 OR noSousSecteur=12 OR noSousSecteur=13 OR noSousSecteur=14 OR noSousSecteur=15 OR noSousSecteur=16 OR noSousSecteur=17 OR noSousSecteur=18 OR noSousSecteur=19 OR noSousSecteur=20 OR noSousSecteur=21 OR noSousSecteur=22 OR noSousSecteur=23 OR noSousSecteur=24 OR noSousSecteur=25 OR noSousSecteur=26 OR noSousSecteur=27 OR noSousSecteur=28 OR noSousSecteur=29 OR noSousSecteur=30 OR noSousSecteur=32 OR noSousSecteur=33 OR noSousSecteur=34 OR noSousSecteur=35 OR noSousSecteur=36 OR noSousSecteur=37 OR noSousSecteur=38 OR noSousSecteur=51;")
        # query.exec("UPDATE Obligation SET ExigenceCap = 0 WHERE noSousSecteur=39 OR noSousSecteur=40 OR noSousSecteur=41 OR noSousSecteur=42 OR noSousSecteur=43 OR noSousSecteur=44 OR noSousSecteur=45 OR noSousSecteur=46 OR noSousSecteur=47 OR noSousSecteur=48 OR noSousSecteur=49 OR noSousSecteur=50")
        # query.clear()

        self.titre_save = {'nomEtat': "Titre"}
        self.sommaire_save = {'nomEtat': "Sommaire"}
        self.echeplus_save = {'type': 'etat', 'nomEtat': "EchéancierValue", 'ordre': 0, 'titreSommaire': "Plus ou moins values par échéance"}
        self.echeancier_save = {'type': 'etat', 'nomEtat': "Echéancier", 'ordre': 1, 'titreSommaire': "Remboursements par échéance"}
        self.exigence_save = {'type': 'etat', 'nomEtat': "ExigenceCapital", 'ordre': 2, 'titreSommaire': 'Répartition par rating et selon les exigences en fonds propres "Solvabilité 2"'}
        self.emetteur_save = {'type': 'etat', 'nomEtat': "Libelle", 'ordre': 3, 'titreSommaire': 'Classement par émetteurs'}

        self.titre = self.titre_save.copy()
        self.sommaire = self.sommaire_save.copy()
        self.echeplus = self.echeplus_save.copy()
        self.echeancier = self.echeancier_save.copy()
        self.exigence = self.exigence_save.copy()
        self.emetteur = self.emetteur_save.copy()

        self.on_btn_resetPerso_clicked()
        self.on_btn_resetOrdre_clicked()

    @pyqtSlot()
    def on_btn_config_av_clicked(self):
        QMessageBox.information(self, "Configuration", "Sélectionner le fichier PDF Avertissement")
        settings = QSettings()
        AVERTISSEMENT = settings.value("AVERTISSEMENT", defaultValue='')
        if AVERTISSEMENT == '':
            fileName = QFileDialog.getOpenFileName(self)[0]
        else:
            fileName = QFileDialog.getOpenFileName(self, directory=QDir(AVERTISSEMENT).path())[0]

        if fileName:
            settings = QSettings()
            settings.setValue("AVERTISSEMENT", fileName)
            self.file_avertissement = fileName

    @pyqtSlot()
    def on_btn_modifPerso_clicked(self):
        liste = [[self.tb_titre, self.titre, self.titre_save], [self.tb_sommaire, self.sommaire, self.sommaire_save],
                 [self.tb_echeplus, self.echeplus, self.echeplus_save], [self.tb_echeancier, self.echeancier, self.echeancier_save],
                 [self.tb_exigence, self.exigence, self.exigence_save], [self.tb_emetteur, self.emetteur, self.emetteur_save]]

        for elem in liste:
            elem[0].setEnabled(True)

        self.btn_modifPerso.setEnabled(False)
        self.btn_perso.setEnabled(True)
        self.btn_resetPerso.setEnabled(True)
        self.tabWidget.setTabEnabled(0, False)
        self.tabWidget.setTabEnabled(2, False)
        QTimer.singleShot(350, lambda: self.repaint())

    @pyqtSlot()
    def on_btn_perso_clicked(self):
        liste = [[self.tb_titre, self.titre, self.titre_save], [self.tb_sommaire, self.sommaire, self.sommaire_save],
                 [self.tb_echeplus, self.echeplus, self.echeplus_save], [self.tb_echeancier, self.echeancier, self.echeancier_save],
                 [self.tb_exigence, self.exigence, self.exigence_save], [self.tb_emetteur, self.emetteur, self.emetteur_save]]

        for elem in liste:
            elem[1]['nomEtat'] = elem[0].text()
            elem[0].setEnabled(False)

        self.btn_modifPerso.setEnabled(True)
        self.btn_perso.setEnabled(False)
        self.btn_resetPerso.setEnabled(True)
        self.tabWidget.setTabEnabled(0, True)
        self.tabWidget.setTabEnabled(2, True)
        QTimer.singleShot(350, lambda: self.repaint())

    @pyqtSlot()
    def on_btn_resetPerso_clicked(self):
        liste = [[self.tb_titre, self.titre, self.titre_save], [self.tb_sommaire, self.sommaire, self.sommaire_save],
                 [self.tb_echeplus, self.echeplus, self.echeplus_save], [self.tb_echeancier, self.echeancier, self.echeancier_save],
                 [self.tb_exigence, self.exigence, self.exigence_save], [self.tb_emetteur, self.emetteur, self.emetteur_save]]

        for elem in liste:
            elem[1] = elem[2].copy()
            elem[0].setText(elem[1]['nomEtat'])
            elem[0].setEnabled(False)

        self.btn_modifPerso.setEnabled(True)
        self.btn_perso.setEnabled(False)
        self.btn_resetPerso.setEnabled(True)
        self.tabWidget.setTabEnabled(0, True)
        self.tabWidget.setTabEnabled(2, True)
        QTimer.singleShot(350, lambda: self.repaint())

    @pyqtSlot()
    def on_btn_modifOrdre_clicked(self):
        liste = [[self.nb_echeplus, self.echeplus, self.echeplus_save], [self.nb_echeancier, self.echeancier, self.echeancier_save],
                 [self.nb_exigence, self.exigence, self.exigence_save], [self.nb_emetteur, self.emetteur, self.emetteur_save]]

        for elem in liste:
            elem[0].setEnabled(True)

        self.btn_modifOrdre.setEnabled(False)
        self.btn_ordre.setEnabled(True)
        self.btn_resetOrdre.setEnabled(True)
        self.tabWidget.setTabEnabled(0, False)
        self.tabWidget.setTabEnabled(1, False)
        QTimer.singleShot(350, lambda: self.repaint())

    @pyqtSlot()
    def on_btn_ordre_clicked(self):
        liste = [[self.nb_echeplus, self.echeplus, self.echeplus_save], [self.nb_echeancier, self.echeancier, self.echeancier_save],
                 [self.nb_exigence, self.exigence, self.exigence_save], [self.nb_emetteur, self.emetteur, self.emetteur_save]]

        for elem in liste:
            elem[1]['ordre'] = int(elem[0].text())
            elem[0].setEnabled(False)

        self.btn_modifOrdre.setEnabled(True)
        self.btn_ordre.setEnabled(False)
        self.btn_resetOrdre.setEnabled(True)
        self.tabWidget.setTabEnabled(0, True)
        self.tabWidget.setTabEnabled(1, True)
        QTimer.singleShot(350, lambda: self.repaint())

    @pyqtSlot()
    def on_btn_resetOrdre_clicked(self):
        liste = [[self.nb_echeplus, self.echeplus, self.echeplus_save], [self.nb_echeancier, self.echeancier, self.echeancier_save],
                 [self.nb_exigence, self.exigence, self.exigence_save], [self.nb_emetteur, self.emetteur, self.emetteur_save]]

        for elem in liste:
            elem[1] = elem[2].copy()
            elem[0].setText(str(elem[1]['ordre']))
            elem[0].setEnabled(False)

        self.btn_modifOrdre.setEnabled(True)
        self.btn_ordre.setEnabled(False)
        self.btn_resetOrdre.setEnabled(True)
        self.tabWidget.setTabEnabled(0, True)
        self.tabWidget.setTabEnabled(1, True)
        QTimer.singleShot(350, lambda: self.repaint())

    def acc_titre(self, nomEtat, action, fileName=""):
        try:
            # Ouverture de la base de données
            acc = win32.gencache.EnsureDispatch('Access.Application')
            acc.OpenCurrentDatabase(self.fileBDD, True)

            acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewReport)

            acc.Reports.Item(nomEtat).Controls.Item("txt_titre1").Caption = self.client.nomEntreprise.strip()
            acc.Reports.Item(nomEtat).Controls.Item("txt_titre2").Caption = "Portefeuille " + self.portefeuille.nomPortefeuille.strip() + " au " + self.date.toString("dd/MM/yyyy")

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

    def acc_etat(self, nomEtat, action, fileName="", nb_pages=0):
        try:
            whereCondition = "[noPortefeuille] = " + self.strNoPort + " AND DateDeMAJ = #" + self.strDate + "#"

            # Ouverture de la base de données
            acc = win32.gencache.EnsureDispatch('Access.Application')
            acc.OpenCurrentDatabase(self.fileBDD, True)

            acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewReport, None, whereCondition)

            acc.Reports.Item(nomEtat).Controls.Item("txt_nomportefeuille").Caption = self.legendePort
            acc.Reports.Item(nomEtat).Controls.Item("txt_datemaj").Caption = "Mise à jour le " + self.date.toString("dd/MM/yyyy")
            acc.Reports.Item(nomEtat).Controls.Item("txt_nbpages").ControlSource = '=[Page] + {}'.format(nb_pages)

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

    # def Graphique(self, nomEtat, nomGraphique, sourceSQL, action, fileName=''):
    #     try:
    #         # Ouverture de la base de données
    #         acc = win32.gencache.EnsureDispatch('Access.Application')
    #         acc.OpenCurrentDatabase(self.fileBDD, True)

    #         acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewReport)

    #         acc.Reports.Item(nomEtat).Controls.Item(nomGraphique).RowSource = sourceSQL
    #         acc.Reports.Item(nomEtat).Controls.Item("txt_nomportefeuille").Caption = self.legendePort
    #         acc.Reports.Item(nomEtat).Controls.Item("txt_datemaj").Caption = "Mise à jour le " + self.date.toString("dd/MM/yyyy")
    #         # champs dlm

    #         if action == "Ouvrir":
    #             # acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewPreview, None, whereCondition)
    #             acc.DoCmd.Maximize()
    #             acc.Visible = True

    #         if action == "PDF":
    #             if fileName:
    #                 acc.DoCmd.OutputTo(win32.constants.acOutputReport, nomEtat, win32.constants.acFormatPDF, fileName)
    #             else:
    #                 acc.DoCmd.OutputTo(win32.constants.acOutputReport, nomEtat, win32.constants.acFormatPDF)
    #             acc.Quit()
    #     except pythoncom.com_error as error:
    #         detailed_message(None, QMessageBox.Critical, "Erreur Access", "Ouverture impossible. Merci de vérifier que la base de données n'est pas ouverte.", str(error))

    @pyqtSlot()
    def on_btn_titre_clicked(self):
        self.acc_titre(self.titre['nomEtat'], "Ouvrir")

    @pyqtSlot()
    def on_btn_titrePDF_clicked(self):
        self.acc_titre(self.titre['nomEtat'], "PDF")

    @pyqtSlot()
    def on_btn_echeplus_clicked(self):
        self.acc_etat(self.echeplus['nomEtat'], "Ouvrir")

    @pyqtSlot()
    def on_btn_echeplusPDF_clicked(self):
        self.acc_etat(self.echeplus['nomEtat'], "PDF")

    @pyqtSlot()
    def on_btn_echeancier_clicked(self):
        self.acc_etat(self.echeancier['nomEtat'], "Ouvrir")

    @pyqtSlot()
    def on_btn_echeancierPDF_clicked(self):
        self.acc_etat(self.echeancier['nomEtat'], "PDF")

    @pyqtSlot()
    def on_btn_exigence_clicked(self):
        self.acc_etat(self.exigence['nomEtat'], "Ouvrir")

    @pyqtSlot()
    def on_btn_exigencePDF_clicked(self):
        self.acc_etat(self.exigence['nomEtat'], "PDF")

    @pyqtSlot()
    def on_btn_emetteur_clicked(self):
        self.acc_etat(self.emetteur['nomEtat'], "Ouvrir")

    @pyqtSlot()
    def on_btn_emetteurPDF_clicked(self):
        self.acc_etat(self.emetteur['nomEtat'], "PDF")

    # @pyqtSlot()
    # def on_btn_PDF_clicked(self):
    #     resultFileName = QFileDialog.getSaveFileName(self, "Save File", QDir(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)).filePath('exportation.pdf'),
    #                                                  "PDF (*.pdf)")[0]
    #     if resultFileName:
    #         list_cb_checked = [self.cb_echeplus.isChecked(), self.cb_echeancier.isChecked(), self.cb_exigence.isChecked(), self.cb_emetteur.isChecked(), 
    #                            self.cb_histoType.isChecked(), self.cb_gType.isChecked(), self.cb_gRating.isChecked(), self.cb_gSecteur.isChecked(),
    #                            self.cb_gGovnt.isChecked(), self.cb_gCorp.isChecked(), self.cb_gFin.isChecked(), self.cb_synthese.isChecked()]
    #         nb_checked = sum(list_cb_checked)
    #         nb_pdfs = nb_checked
    #         if nb_checked == 0:
    #             nb_pdfs = len(list_cb_checked)

    #         progress = QProgressDialog("Exportation PDF", "Annuler", 0, nb_pdfs, self)
    #         progress.setWindowTitle("Générations des états")
    #         progress.setWindowModality(Qt.WindowModal)
    #         progress.show()

    #         tempdir = QTemporaryDir()
    #         def file(self, i):
    #             return tempdir.filePath("{}.pdf".format(i)).replace("/", "\\")

            
    #         i = 0
    #         if self.cb_echeplus.isChecked() or nb_checked == 0:
    #             self.acc_etat("EchéancierValue", "PDF", fileName=file(i))
    #             i += 1
    #             progress.setValue(i)
    #         if self.cb_echeancier.isChecked() or nb_checked == 0:
    #             self.acc_etat("Echéancier", "PDF", fileName=file(i))
    #             i += 1
    #             progress.setValue(i)
    #         if self.cb_exigence.isChecked() or nb_checked == 0:
    #             self.acc_etat("ExigenceCapital", "PDF", fileName=file(i))
    #             i += 1
    #             progress.setValue(i)
    #         if self.cb_emetteur.isChecked() or nb_checked == 0:
    #             self.acc_etat("Libelle", "PDF", fileName=file(i))
    #             i += 1
    #             progress.setValue(i)

    #         pdfs = [file(j) for j in range(0, i)]
    #         merger = PdfFileMerger()
    #         for pdf in pdfs:
    #             merger.append(pdf)
    #         try:
    #             merger.write(resultFileName)
    #         except Exception as e:
    #             detailed_message(self, QMessageBox.Critical, "Exportation PDF", "Echec de l'écriture du fichier PDF", str(e))
    #         merger.close()

    #         QMessageBox.information(self, "Exportation PDF", "Exportation terminée")

    @pyqtSlot()
    def on_btn_PDF_clicked(self):
        resultFileName = QFileDialog.getSaveFileName(self, "Save File", QDir(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)).filePath('exportation.pdf'),
                                                     "PDF (*.pdf)")[0]
        if resultFileName:
            list_cb_checked = [self.cb_titre.isChecked(), self.cb_sommaire.isChecked(), self.cb_avertissement.isChecked(), self.cb_echeplus.isChecked(), self.cb_echeancier.isChecked(), self.cb_exigence.isChecked(), self.cb_emetteur.isChecked(), 
                               self.cb_histoType.isChecked(), self.cb_gType.isChecked(), self.cb_gRating.isChecked(), self.cb_gSecteur.isChecked(),
                               self.cb_gGovnt.isChecked(), self.cb_gCorp.isChecked(), self.cb_gFin.isChecked(), self.cb_synthese.isChecked()]
            nb_checked = sum(list_cb_checked)
            nb_pdfs = nb_checked
            if nb_checked == 0:
                nb_pdfs = len(list_cb_checked)

            # progress = QProgressDialog("Exportation PDF", "Annuler", 0, nb_pdfs, self)
            # progress.setWindowTitle("Générations des états")
            # progress.setWindowModality(Qt.WindowModal)
            # progress.show()

            tempdir = QTemporaryDir()
            # print(tempdir.path())

            def file(i):
                return tempdir.filePath("{}.pdf".format(i)).replace("/", "\\")
            file_titre = tempdir.filePath("titre.pdf").replace("/", "\\")
            file_sommaire = tempdir.filePath("sommaire.pdf").replace("/", "\\")

            # traiter graphique séparemment

            liste = [None] * 12

            if self.cb_echeplus.isChecked() or nb_checked == 0:
                etat = self.echeplus
                liste[etat['ordre']] = etat
            if self.cb_echeancier.isChecked() or nb_checked == 0:
                etat = self.echeancier
                liste[etat['ordre']] = etat
            if self.cb_exigence.isChecked() or nb_checked == 0:
                etat = self.exigence
                liste[etat['ordre']] = etat
            if self.cb_emetteur.isChecked() or nb_checked == 0:
                etat = self.emetteur
                liste[etat['ordre']] = etat

            liste_generation = [item for index, item in enumerate(liste) if item]

            # titre
            # sommaire
            # avertissement

            nb_pages_total = 0

            if self.cb_titre.isChecked() or nb_checked == 0:
                etat = self.titre
                self.acc_titre(self.titre['nomEtat'], "PDF", file_titre)
                nb_pages_total += 1

            if self.cb_sommaire.isChecked() or nb_checked == 0:
                # Création plus tard
                nb_pages_total += 1

            if self.cb_avertissement.isChecked() or nb_checked == 0:
                reader = PdfFileReader(self.file_avertissement)
                nb_pages = reader.getNumPages()
                nb_pages_total += nb_pages

            for i in range(len(liste_generation)):
                etat = liste_generation[i]
                if etat['type'] == 'etat':
                    self.acc_etat(etat['nomEtat'], "PDF", fileName=file(i), nb_pages=nb_pages_total)
                liste_generation[i]['first_page'] = nb_pages_total + 1
                reader = PdfFileReader(file(i))
                nb_pages = reader.getNumPages()
                nb_pages_total += nb_pages

            # CREATION DU SOMMAIRE
            if self.cb_sommaire.isChecked() or nb_checked == 0:
                # Ouverture de la base de données
                acc = win32.gencache.EnsureDispatch('Access.Application')
                acc.OpenCurrentDatabase(self.fileBDD, True)
                acc.DoCmd.OpenReport(self.sommaire['nomEtat'], win32.constants.acViewReport)
                imax = 0
                for i in range(len(liste_generation)):
                    etat = liste_generation[i]
                    acc.Reports.Item(self.sommaire['nomEtat']).Controls.Item("txt_titre{}".format(i + 1)).Caption = etat['titreSommaire'] + " ." * 200
                    acc.Reports.Item(self.sommaire['nomEtat']).Controls.Item("txt_page{}".format(i + 1)).Caption = "page " + str(etat['first_page'])
                    imax = i
                for i in range(imax + 1, 6):
                    acc.Reports.Item(self.sommaire['nomEtat']).Controls.Item("txt_titre{}".format(i + 1)).Caption = ""
                    acc.Reports.Item(self.sommaire['nomEtat']).Controls.Item("txt_page{}".format(i + 1)).Caption = ""
                acc.DoCmd.OutputTo(win32.constants.acOutputReport, self.sommaire['nomEtat'], win32.constants.acFormatPDF, file_sommaire)
                acc.Quit()

            # FUSION
            pdfs = []
            if self.cb_titre.isChecked() or nb_checked == 0:
                pdfs += [file_titre]
            if self.cb_sommaire.isChecked() or nb_checked == 0:
                pdfs += [file_sommaire]
            if self.cb_avertissement.isChecked() or nb_checked == 0:
                pdfs += [self.file_avertissement]

            pdfs += [file(i) for i in range(len(liste_generation))]
            merger = PdfFileMerger()
            for pdf in pdfs:
                merger.append(pdf)
            try:
                merger.write(resultFileName)
            except Exception as e:
                detailed_message(self, QMessageBox.Critical, "Exportation PDF", "Echec de l'écriture du fichier PDF", str(e))
            merger.close()
            tempdir.remove()

            QMessageBox.information(self, "Exportation PDF", "Exportation terminée")
            os.startfile(resultFileName)
