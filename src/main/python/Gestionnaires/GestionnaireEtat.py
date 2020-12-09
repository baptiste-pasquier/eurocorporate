import win32com.client as win32
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDir, QSettings, pyqtSlot, QStandardPaths, QTemporaryDir, QTimer, Qt
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QProgressDialog
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

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
        self.btn_config_av.setStatusTip(self.file_avertissement)

        # Bouton exigcap
        # query = QtSql.QSqlQuery()
        # query.exec("UPDATE Obligation SET ExigenceCap = null WHERE noSousSecteur=1 OR noSousSecteur=2 OR noSousSecteur=3 OR noSousSecteur=4 OR noSousSecteur=5 OR noSousSecteur=6 OR noSousSecteur=7 OR noSousSecteur=8 OR noSousSecteur=9 OR noSousSecteur=10 OR noSousSecteur=11 OR noSousSecteur=12 OR noSousSecteur=13 OR noSousSecteur=14 OR noSousSecteur=15 OR noSousSecteur=16 OR noSousSecteur=17 OR noSousSecteur=18 OR noSousSecteur=19 OR noSousSecteur=20 OR noSousSecteur=21 OR noSousSecteur=22 OR noSousSecteur=23 OR noSousSecteur=24 OR noSousSecteur=25 OR noSousSecteur=26 OR noSousSecteur=27 OR noSousSecteur=28 OR noSousSecteur=29 OR noSousSecteur=30 OR noSousSecteur=32 OR noSousSecteur=33 OR noSousSecteur=34 OR noSousSecteur=35 OR noSousSecteur=36 OR noSousSecteur=37 OR noSousSecteur=38 OR noSousSecteur=51;")
        # query.exec("UPDATE Obligation SET ExigenceCap = 0 WHERE noSousSecteur=39 OR noSousSecteur=40 OR noSousSecteur=41 OR noSousSecteur=42 OR noSousSecteur=43 OR noSousSecteur=44 OR noSousSecteur=45 OR noSousSecteur=46 OR noSousSecteur=47 OR noSousSecteur=48 OR noSousSecteur=49 OR noSousSecteur=50")
        # query.clear()

        self.titre_save = {'nomEtat': "Titre"}
        self.sommaire_save = {'nomEtat': "Sommaire"}
        self.synthese_save = {'type': 'synthese', 'nomEtat': "Synthese", 'ordre': 4, 'titreSommaire': "Synthèse"}
        self.ESG_save = {'type': 'ESG', 'nomEtat': "ESG", 'ordre': 5, 'titreSommaire': "Rapport ESG"}
        self.echeplus_save = {'type': 'etat', 'nomEtat': "EchéancierValue", 'ordre': 6, 'titreSommaire': "Plus ou moins values par échéance"}
        self.echeancier_save = {'type': 'etat', 'nomEtat': "Echéancier", 'ordre': 7, 'titreSommaire': "Remboursements par échéance"}
        self.exigence_save = {'type': 'etat', 'nomEtat': "ExigenceCapital", 'ordre': 8, 'titreSommaire': 'Répartition par rating et selon les exigences en fonds propres "Solvabilité 2"'}
        self.histoType_save = {'type': 'graphiqueDetail', 'nomEtat': "GraphiqueRembTypeLegend", 'nomEtat2': "Select_TypeDoblig", 'nomGraphique': "Graphique", 'sourceSQL': "TRANSFORM Sum([Remboursement]) AS [SommeDeRemboursement] SELECT (Year([Maturite])) FROM [Valorisation] WHERE noPortefeuille=" + self.strNoPort + " AND DateDeMAJ=#" + self.strDate + "# GROUP BY (Year([Maturite])) PIVOT [nomType]",
                               'sourceSQL2': "SELECT TypeOblig.noType, TypeOblig.nomType, Sum(Valorisation.[Remboursement]) AS [Total remboursement] FROM Valorisation WHERE [noPortefeuille]=" + self.strNoPort + " And DateDeMAJ=#" + self.strDate + "# GROUP BY TypeOblig.noType, TypeOblig.nomType",
                               'titre1': "GRAPHIQUE DÉTAILLÉ DES REMBOURSEMENTS PAR TYPE", 'titre2': "Calculs réalisés avec les valeurs de remboursement", 'ordre': 9, 'titreSommaire': "Graphiques"}
        self.gType_save = {'type': 'graphique', 'nomEtat': "GraphiqueCamembert", 'nomGraphique': "Graphique",
                           'sourceSQL': "SELECT [nomType], Sum([Remboursement]) AS Remb FROM Valorisation WHERE [noPortefeuille] = " + self.strNoPort + " AND DateDeMAJ = #" + self.strDate + "# GROUP BY [nomType]",
                           'ordre': 10, 'titreSommaire': "Graphiques"}
        self.gRating_save = {'type': 'graphiqueDetail', 'nomEtat': "GraphCamLegend_RatingEmetteur", 'nomEtat2': "Select_TypeRating", 'nomGraphique': "Graphique", 'sourceSQL': "SELECT [Description pour la synthese], Sum([Remboursement]) AS Remb FROM Valorisation WHERE [noPortefeuille] = " + self.strNoPort + " AND DateDeMAJ = #" + self.strDate + "# GROUP BY [Description pour la synthese],[Ordre] ORDER BY [Ordre]",
                             'sourceSQL2': "SELECT Sum(Valorisation.Remboursement) AS SommeDeRemboursement, Valorisation.[Description pour la synthese], Valorisation.Ordre FROM Valorisation WHERE Valorisation.[noPortefeuille] =" + self.strNoPort + " AND Valorisation.DateDeMAJ =#" + self.strDate + "# GROUP BY Valorisation.[Description pour la synthese], Valorisation.Ordre ORDER BY Valorisation.Ordre",
                             'titre1': "GRAPHIQUE DE RÉPARTITION DÉTAILLÉ PAR RATING", 'titre2': "Calculs réalisés avec les valeurs de remboursement", 'ordre': 11, 'titreSommaire': "Graphiques"}
        self.gSecteur_save = {'type': 'graphiqueDetail', 'nomEtat': "GraphCamLegendSectToT", 'nomEtat2': "Select_SecteurTot", 'nomGraphique': "Graphique", 'sourceSQL': "SELECT [nomSSGraph], Sum([Remboursement]) AS Remb FROM Valorisation WHERE [noPortefeuille] = " + self.strNoPort + " AND DateDeMAJ =#" + self.strDate + "# GROUP BY [nomSSGraph]",
                              'sourceSQL2': "SELECT Valorisation.noSecteur, Valorisation.nomSection, Sum(Valorisation.[Remboursement]) AS [Total remboursement] FROM Valorisation WHERE [noPortefeuille]=" + self.strNoPort + "  And DateDeMAJ=#" + self.strDate + "# GROUP BY Valorisation.noSecteur, Valorisation.nomSection",
                              'titre1': "GRAPHIQUE DE RÉPARTITION DÉTAILLÉ PAR SECTEUR", 'titre2': "Données basées sur les valeurs de remboursement", 'ordre': 12, 'titreSommaire': "Graphiques"}
        self.gCorp_save = {'type': 'graphiqueDetail', 'nomEtat': "GraphCamLegend", 'nomEtat2': "Select_Secteur", 'nomGraphique': "Graphique", 'sourceSQL': "SELECT [nomSousSecteur], Sum([Remboursement]) AS Remb FROM Valorisation WHERE [noPortefeuille] = " + self.strNoPort + " AND DateDeMAJ = #" + self.strDate + "# AND [noSecteur]=2 GROUP BY [nomSousSecteur]",
                           'sourceSQL2': "SELECT Valorisation.noSecteur, Valorisation.nomSection, Valorisation.nomSousSecteur, Sum(Valorisation.[Remboursement]) AS [Total remboursement] FROM Valorisation WHERE [noPortefeuille]=" + self.strNoPort + "  AND DateDeMAJ= #" + self.strDate + "# AND [noSecteur]=2 GROUP BY Valorisation.noSecteur, Valorisation.nomSection, Valorisation.nomSousSecteur",
                           'titre1': "DÉTAIL DE LA RÉPARTITION DES VALEURS DU SECTEUR CORPORATE", 'titre2': "Calculs réalisés avec les valeurs de remboursement", 'ordre': 13, 'titreSommaire': "Graphiques"}
        self.gFin_save = {'type': 'graphiqueDetail', 'nomEtat': "GraphCamLegend", 'nomEtat2': "Select_Secteur", 'nomGraphique': "Graphique", 'sourceSQL': "SELECT [nomSousSecteur], Sum([Remboursement]) AS Remb FROM Valorisation WHERE [noPortefeuille] = " + self.strNoPort + " AND DateDeMAJ = #" + self.strDate + "# AND [noSecteur]=3 GROUP BY [nomSousSecteur]",
                          'sourceSQL2': "SELECT Valorisation.noSecteur, Valorisation.nomSection, Valorisation.nomSousSecteur, Sum(Valorisation.[Remboursement]) AS [Total remboursement] FROM Valorisation WHERE [noPortefeuille]=" + self.strNoPort + "  AND DateDeMAJ= #" + self.strDate + "# AND [noSecteur]=3 GROUP BY Valorisation.noSecteur, Valorisation.nomSection, Valorisation.nomSousSecteur",
                          'titre1': "DÉTAIL DE LA RÉPARTITION DES VALEURS DU SECTEUR FINANCIER", 'titre2': "Calculs réalisés avec les valeurs de remboursement", 'ordre': 14, 'titreSommaire': "Graphiques"}
        self.gGovnt_save = {'type': 'graphiqueDetail', 'nomEtat': "GraphCamLegend", 'nomEtat2': "Select_Secteur", 'nomGraphique': "Graphique", 'sourceSQL': "SELECT [nomSousSecteur], Sum([Remboursement]) AS Remb FROM Valorisation WHERE [noPortefeuille] = " + self.strNoPort + " AND DateDeMAJ = #" + self.strDate + "# AND [noSecteur]=4 GROUP BY [nomSousSecteur]",
                            'sourceSQL2': "SELECT Valorisation.noSecteur, Valorisation.nomSection, Valorisation.nomSousSecteur, Sum(Valorisation.[Remboursement]) AS [Total remboursement] FROM Valorisation WHERE [noPortefeuille]=" + self.strNoPort + "  AND DateDeMAJ= #" + self.strDate + "# AND [noSecteur]=4 GROUP BY Valorisation.noSecteur, Valorisation.nomSection, Valorisation.nomSousSecteur",
                            'titre1': "DÉTAIL DE LA RÉPARTITION DES VALEURS DU SECTEUR GOUVERNEMENT", 'titre2': "Calculs réalisés avec les valeurs de remboursement", 'ordre': 15, 'titreSommaire': "Graphiques"}
        self.emetteur_save = {'type': 'etat', 'nomEtat': "Libelle", 'ordre': 16, 'titreSommaire': 'Classement par émetteurs'}

        self.titre = self.titre_save.copy()
        self.sommaire = self.sommaire_save.copy()
        self.synthese = self.synthese_save.copy()
        self.ESG = self.ESG_save.copy()
        self.echeplus = self.echeplus_save.copy()
        self.echeancier = self.echeancier_save.copy()
        self.exigence = self.exigence_save.copy()
        self.histoType = self.histoType_save.copy()
        self.gType = self.gType_save.copy()
        self.gRating = self.gRating_save.copy()
        self.gSecteur = self.gSecteur_save.copy()
        self.gCorp = self.gCorp_save.copy()
        self.gFin = self.gFin_save.copy()
        self.gGovnt = self.gGovnt_save.copy()
        self.emetteur = self.emetteur_save.copy()

        self.on_btn_resetPerso_clicked()
        self.on_btn_resetOrdre_clicked()

        self.error = False

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
                 [self.tb_synthese, self.synthese, self.synthese_save], [self.tb_ESG, self.ESG, self.ESG_save],
                 [self.tb_echeplus, self.echeplus, self.echeplus_save], [self.tb_echeancier, self.echeancier, self.echeancier_save],
                 [self.tb_exigence, self.exigence, self.exigence_save], [self.tb_histoType, self.histoType, self.histoType_save],
                 [self.tb_gType, self.gType, self.gType_save],
                 [self.tb_gRating, self.gRating, self.gRating_save], [self.tb_gSecteur, self.gSecteur, self.gSecteur_save],
                 [self.tb_gCorp, self.gCorp, self.gCorp_save], [self.tb_gFin, self.gFin, self.gFin_save],
                 [self.tb_gGovnt, self.gGovnt, self.gGovnt_save], [self.tb_emetteur, self.emetteur, self.emetteur_save]]

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
                 [self.tb_synthese, self.synthese, self.synthese_save], [self.tb_ESG, self.ESG, self.ESG_save],
                 [self.tb_echeplus, self.echeplus, self.echeplus_save], [self.tb_echeancier, self.echeancier, self.echeancier_save],
                 [self.tb_exigence, self.exigence, self.exigence_save], [self.tb_histoType, self.histoType, self.histoType_save],
                 [self.tb_gType, self.gType, self.gType_save],
                 [self.tb_gRating, self.gRating, self.gRating_save], [self.tb_gSecteur, self.gSecteur, self.gSecteur_save],
                 [self.tb_gCorp, self.gCorp, self.gCorp_save], [self.tb_gFin, self.gFin, self.gFin_save],
                 [self.tb_gGovnt, self.gGovnt, self.gGovnt_save], [self.tb_emetteur, self.emetteur, self.emetteur_save]]

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
                 [self.tb_synthese, self.synthese, self.synthese_save], [self.tb_ESG, self.ESG, self.ESG_save],
                 [self.tb_echeplus, self.echeplus, self.echeplus_save], [self.tb_echeancier, self.echeancier, self.echeancier_save],
                 [self.tb_exigence, self.exigence, self.exigence_save], [self.tb_histoType, self.histoType, self.histoType_save],
                 [self.tb_gType, self.gType, self.gType_save],
                 [self.tb_gRating, self.gRating, self.gRating_save], [self.tb_gSecteur, self.gSecteur, self.gSecteur_save],
                 [self.tb_gCorp, self.gCorp, self.gCorp_save], [self.tb_gFin, self.gFin, self.gFin_save],
                 [self.tb_gGovnt, self.gGovnt, self.gGovnt_save], [self.tb_emetteur, self.emetteur, self.emetteur_save]]

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
        liste = [[self.nb_synthese, self.synthese, self.synthese_save], [self.nb_ESG, self.ESG, self.ESG_save],
                 [self.nb_echeplus, self.echeplus, self.echeplus_save], [self.nb_echeancier, self.echeancier, self.echeancier_save],
                 [self.nb_exigence, self.exigence, self.exigence_save], [self.nb_histoType, self.histoType, self.histoType_save],
                 [self.nb_gType, self.gType, self.gType_save],
                 [self.nb_gRating, self.gRating, self.gRating_save], [self.nb_gSecteur, self.gSecteur, self.gSecteur_save],
                 [self.nb_gCorp, self.gCorp, self.gCorp_save], [self.nb_gFin, self.gFin, self.gFin_save],
                 [self.nb_gGovnt, self.gGovnt, self.gGovnt_save], [self.nb_emetteur, self.emetteur, self.emetteur_save]]

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
        liste = [[self.nb_synthese, self.synthese, self.synthese_save], [self.nb_ESG, self.ESG, self.ESG_save],
                 [self.nb_echeplus, self.echeplus, self.echeplus_save], [self.nb_echeancier, self.echeancier, self.echeancier_save],
                 [self.nb_exigence, self.exigence, self.exigence_save], [self.nb_histoType, self.histoType, self.histoType_save],
                 [self.nb_gType, self.gType, self.gType_save],
                 [self.nb_gRating, self.gRating, self.gRating_save], [self.nb_gSecteur, self.gSecteur, self.gSecteur_save],
                 [self.nb_gCorp, self.gCorp, self.gCorp_save], [self.nb_gFin, self.gFin, self.gFin_save],
                 [self.nb_gGovnt, self.gGovnt, self.gGovnt_save], [self.nb_emetteur, self.emetteur, self.emetteur_save]]

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
        liste = [[self.nb_synthese, self.synthese, self.synthese_save], [self.nb_ESG, self.ESG, self.ESG_save],
                 [self.nb_echeplus, self.echeplus, self.echeplus_save], [self.nb_echeancier, self.echeancier, self.echeancier_save],
                 [self.nb_exigence, self.exigence, self.exigence_save], [self.nb_histoType, self.histoType, self.histoType_save],
                 [self.nb_gType, self.gType, self.gType_save],
                 [self.nb_gRating, self.gRating, self.gRating_save], [self.nb_gSecteur, self.gSecteur, self.gSecteur_save],
                 [self.nb_gCorp, self.gCorp, self.gCorp_save], [self.nb_gFin, self.gFin, self.gFin_save],
                 [self.nb_gGovnt, self.gGovnt, self.gGovnt_save], [self.nb_emetteur, self.emetteur, self.emetteur_save]]

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
            detailed_message(self, QMessageBox.Critical, "Erreur Access", "Merci de vérifier que la base de données n'est pas ouverte.", str(error))
            self.error = True

    def acc_etat(self, nomEtat, action, fileName="", nb_pages=0):
        try:
            whereCondition = "[noPortefeuille] = " + self.strNoPort + " AND DateDeMAJ = #" + self.strDate + "#"

            # Ouverture de la base de données
            acc = win32.gencache.EnsureDispatch('Access.Application')
            acc.OpenCurrentDatabase(self.fileBDD, True)

            acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewReport, None, whereCondition)

            acc.Reports.Item(nomEtat).Controls.Item("txt_nomportefeuille").Caption = self.legendePort
            acc.Reports.Item(nomEtat).Controls.Item("txt_datemaj").Caption = "Mise à jour du " + self.date.toString("dd/MM/yyyy")
            acc.Reports.Item(nomEtat).Controls.Item("txt_page").ControlSource = '=[Page] + {}'.format(nb_pages)

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
            detailed_message(self, QMessageBox.Critical, "Erreur Access", "Merci de vérifier que la base de données n'est pas ouverte.", str(error))
            self.error = True

    def acc_graphique(self, nomEtat, nomGraphique, sourceSQL, action, fileName="", nb_pages=0):
        try:
            # Ouverture de la base de données
            acc = win32.gencache.EnsureDispatch('Access.Application')
            acc.OpenCurrentDatabase(self.fileBDD, True)

            # On ouvre l'état type pour éditer les sources du graphique
            acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewReport)
            acc.Reports.Item(nomEtat).Controls.Item(nomGraphique).RowSource = sourceSQL

            acc.Reports.Item(nomEtat).Controls.Item("txt_nomportefeuille").Caption = self.legendePort
            acc.Reports.Item(nomEtat).Controls.Item("txt_datemaj").Caption = "Mise à jour du " + self.date.toString("dd/MM/yyyy")
            acc.Reports.Item(nomEtat).Controls.Item("txt_page").ControlSource = '=[Page] + {}'.format(nb_pages)

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
            detailed_message(self, QMessageBox.Critical, "Erreur Access", "Merci de vérifier que la base de données n'est pas ouverte.", str(error))
            self.error = True

    def acc_graphiqueDetail(self, nomEtat, nomEtat2, nomGraphique, sourceSQL, sourceSQL2, titre1, titre2, action, fileName="", nb_pages=0):
        try:
            # Ouverture de la base de données
            acc = win32.gencache.EnsureDispatch('Access.Application')
            acc.OpenCurrentDatabase(self.fileBDD, True)

            # On ouvre l'état type pour éditer les sources du graphique
            acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewReport)
            acc.Reports.Item(nomEtat).Controls.Item(nomGraphique).RowSource = sourceSQL
            acc.Reports.Item(nomEtat).Controls.Item(nomEtat2).Report.RecordSource = sourceSQL2  # On édite la légende
            acc.Reports.Item(nomEtat).Controls.Item("titre1").Caption = titre1
            acc.Reports.Item(nomEtat).Controls.Item("titre2").Caption = titre2

            acc.Reports.Item(nomEtat).Controls.Item("txt_nomportefeuille").Caption = self.legendePort
            acc.Reports.Item(nomEtat).Controls.Item("txt_datemaj").Caption = "Mise à jour du " + self.date.toString("dd/MM/yyyy")
            acc.Reports.Item(nomEtat).Controls.Item("txt_page").ControlSource = '=[Page] + {}'.format(nb_pages)

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
            detailed_message(self, QMessageBox.Critical, "Erreur Access", "Merci de vérifier que la base de données n'est pas ouverte.", str(error))
            self.error = True

    def acc_ESG(self, nomEtat, action, fileName="", nb_pages=0):
        try:
            # Ouverture de la base de données
            acc = win32.gencache.EnsureDispatch('Access.Application')
            acc.OpenCurrentDatabase(self.fileBDD, True)

            acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewReport)

            acc.Reports.Item(nomEtat).Report.RecordSource = "SELECT SUM(IIf([TotEuro]<>0,[TotEuro]*[Valo par le prix]))/SUM(IIf([TotEuro]<>0,[Valo par le prix])) AS NoteESG FROM Valorisation WHERE noPortefeuille=" + self.strNoPort + " AND DateDeMAJ = #" + self.strDate + "#"
            acc.Reports.Item(nomEtat).Controls.Item('ESG tableau').Report.RecordSource = "SELECT TOP 10 * FROM (SELECT A.*, (SELECT COUNT(*) FROM Valorisation WHERE [noPortefeuille]= " + self.strNoPort + " AND [DateDeMAJ]= #" + self.strDate + "# AND A.TotEuro <= TotEuro) AS RowNum, [Valo par le prix]/(SELECT SUM([Valo par le prix]) FROM Valorisation WHERE [noPortefeuille]= " + self.strNoPort + " AND [DateDeMAJ]= #" + self.strDate + "#) AS Pourcentage FROM Valorisation AS A WHERE (((A.noPortefeuille)= " + self.strNoPort + ") AND ((A.DateDeMAJ)= #" + self.strDate + "#)) ORDER BY A.TotEuro DESC);"
            acc.Reports.Item(nomEtat).Controls.Item('Graphique').RowSource = "\
            SELECT ID, Iif(EXPR1 IS NULL, 0, EXPR1) FROM ( SELECT CatTotEuro, Count(CatTotEuro) / (\
                            SELECT COUNT(*) FROM Valorisation WHERE TotEuro IS NOT NULL AND noPortefeuille = {} AND DateDeMAJ = #{}#) AS EXPR1\
                            FROM ( SELECT Iif(TotEuro >= 90,90,\
                                            Iif(TotEuro >= 80,80,\
                                                Iif(TotEuro >= 70,70,\
                                                    Iif(TotEuro >= 60,60,\
                                                        Iif(TotEuro >= 50,50,\
                                                            Iif(TotEuro >= 40,40,\
                                                                Iif(TotEuro >= 30,30,\
                                                                    Iif(TotEuro >= 20,20,\
                                                                        Iif(TotEuro >= 10,10,0))))))))) AS CatTotEuro \
                                    FROM Valorisation WHERE TotEuro IS NOT NULL AND noPortefeuille = {} AND DateDeMAJ = #{}#) GROUP BY CatTotEuro) AS A RIGHT JOIN HistoESG ON A.CatTotEuro = HistoESG.ID ORDER BY ID;".format(self.strNoPort, self.strDate, self.strNoPort, self.strDate)
            acc.Reports.Item(nomEtat).Controls.Item("txt_nomportefeuille").Caption = self.legendePort
            acc.Reports.Item(nomEtat).Controls.Item("txt_datemaj").Caption = "Mise à jour du " + self.date.toString("dd/MM/yyyy")
            acc.Reports.Item(nomEtat).Controls.Item("txt_page").ControlSource = '=[Page] + {}'.format(nb_pages)

            note = acc.Reports.Item(nomEtat).Controls.Item("Note").Value
            if not note:
                note = 0
            acc.Reports.Item(nomEtat).Controls.Item("PetiteFleche").Move((6 + (19.9 - 6) * note / 100) * 567)

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
                return note

            if action == "Value":
                acc.Quit()
                return note
        except pythoncom.com_error as error:
            detailed_message(self, QMessageBox.Critical, "Erreur Access", "Merci de vérifier que la base de données n'est pas ouverte.", str(error))
            self.error = True

    def acc_synthese(self, nomEtat, action, fileName="", nb_pages=0, noteESG=False):
        try:
            if not noteESG:
                noteESG = self.acc_ESG(self.ESG['nomEtat'], "Value")

            whereCondition = "[noPortefeuille] = " + self.strNoPort + " AND DateDeMAJ = #" + self.strDate + "#"

            # Ouverture de la base de données
            acc = win32.gencache.EnsureDispatch('Access.Application')
            acc.OpenCurrentDatabase(self.fileBDD, True, )

            acc.DoCmd.OpenReport(nomEtat, win32.constants.acViewReport, None, whereCondition)

            acc.Reports.Item(nomEtat).Controls.Item('SE_Synthese_rating').Report.RecordSource = "SELECT RATING.[Description pour la synthese], Sum(Valorisation.[Valeur d'acquisition]) AS [SommeDeValeur d'acquisition], Sum(Valorisation.[Valo par le prix]) AS [SommeDeValorisation par le prix], Sum(Valorisation.Remboursement) AS [SommeDeValorisation par le principal], RATING.Ordre, Sum(Valorisation.[+ ou - Value]) AS [SommeDe+ ou - Value], Sum(IIf([Valorisation].[Sensibilite] Is Not Null,[Valorisation].[Sensibilite]*[Valo par le prix]))/Sum(IIf([Valorisation].[Sensibilite] Is Not Null,[Valo par le prix])) AS Sensiblité, Sum(IIf([Valorisation].[Rendement] Is Not Null,[Valorisation].[Rendement]*[Valo par le prix]))/Sum(IIf([Valorisation].[Rendement] Is Not Null,[Valo par le prix])) AS Rendement, Sum(IIf([Valorisation].[Duration] Is Not Null,[Valorisation].[Duration]*[Valo par le prix]))/Sum(IIf([Valorisation].[Duration] Is Not Null,[Valo par le prix])) AS Duration \
                                                                                                 FROM RATING INNER JOIN Valorisation ON RATING.[Rating] = Valorisation.RatingEmetteur \
                                                                                                 WHERE (((RATING.Ordre)=1 Or (RATING.Ordre)=2 Or (RATING.Ordre)=3 Or (RATING.Ordre)=4 Or (RATING.Ordre)=5 Or (RATING.Ordre)=6 Or (RATING.Ordre)=7 Or (RATING.Ordre)=8) AND ((Valorisation.noPortefeuille)= " + self.strNoPort + ") AND ((Valorisation.DateDeMAJ)=#" + self.strDate + "#)) \
                                                                                                 GROUP BY RATING.[Description pour la synthese], RATING.Ordre ORDER BY RATING.Ordre;"
            acc.Reports.Item(nomEtat).Controls.Item('SE_Synthese_secteur').Report.RecordSource = "SELECT Sum(Valorisation.[Valeur d'acquisition]) AS [SommeDeValeur d'acquisition], Sum(Valorisation.[Valo par le prix]) AS [SommeDeValorisation par le prix], Sum(Valorisation.Remboursement) AS [SommeDeValorisation par le principal], Sum(Valorisation.[+ ou - Value]) AS [SommeDe+ ou - Value], Valorisation.nomSection, Sum(IIf([Valorisation].[Sensibilite] Is Not Null,[Valorisation].[Sensibilite]*[Valo par le prix]))/Sum(IIf([Valorisation].[Sensibilite] Is Not Null,[Valo par le prix])) AS Sensiblité, Sum(IIf([Valorisation].[Rendement] Is Not Null,[Valorisation].[Rendement]*[Valo par le prix]))/Sum(IIf([Valorisation].[Rendement] Is Not Null,[Valo par le prix])) AS Rendement, Sum(IIf([Valorisation].[Duration] Is Not Null,[Valorisation].[Duration]*[Valo par le prix]))/Sum(IIf([Valorisation].[Duration] Is Not Null,[Valo par le prix])) AS Duration \
                                                                                                  FROM RATING INNER JOIN Valorisation ON RATING.Rating = Valorisation.Rating \
                                                                                                  WHERE (((Valorisation.noPortefeuille)=" + self.strNoPort + ") AND ((Valorisation.DateDeMAJ)=#" + self.strDate + "#)) GROUP BY Valorisation.nomSection;"
            acc.Reports.Item(nomEtat).Controls.Item('Graphique').RowSource = "SELECT [Description pour la synthese], Sum([Remboursement]) AS Remb FROM Valorisation WHERE [noPortefeuille] = " + self.strNoPort + " AND DateDeMAJ = #" + self.strDate + "# GROUP BY [Description pour la synthese],[Ordre] ORDER BY [Ordre]"
            acc.Reports.Item(nomEtat).Controls.Item("titre").Caption = "VUE D'ENSEMBLE DU PORTEFEUILLE – " + self.legendePort.upper()
            acc.Reports.Item(nomEtat).Controls.Item("txt_nomportefeuille").Caption = self.legendePort
            acc.Reports.Item(nomEtat).Controls.Item("txt_datemaj").Caption = "Mise à jour du " + self.date.toString("dd/MM/yyyy")
            acc.Reports.Item(nomEtat).Controls.Item("txt_page").ControlSource = '=[Page] + {}'.format(nb_pages)

            acc.Reports.Item(nomEtat).Controls.Item("Note").Caption = str(round(noteESG))
            acc.Reports.Item(nomEtat).Controls.Item("PetiteFleche").Move((0.5 + (11.598 - 0.5) * noteESG / 100) * 567)

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
            detailed_message(self, QMessageBox.Critical, "Erreur Access", "Merci de vérifier que la base de données n'est pas ouverte.", str(error))
            self.error = True

    @pyqtSlot()
    def on_btn_titre_clicked(self):
        self.acc_titre(self.titre['nomEtat'], "Ouvrir")

    @pyqtSlot()
    def on_btn_titrePDF_clicked(self):
        self.acc_titre(self.titre['nomEtat'], "PDF")

    @pyqtSlot()
    def on_btn_avertissementPDF_clicked(self):
        os.startfile(self.file_avertissement)

    @pyqtSlot()
    def on_btn_synthese_clicked(self):
        self.acc_synthese(self.synthese['nomEtat'], "Ouvrir")

    @pyqtSlot()
    def on_btn_synthesePDF_clicked(self):
        self.acc_synthese(self.synthese['nomEtat'], "PDF")

    @pyqtSlot()
    def on_btn_ESG_clicked(self):
        self.acc_ESG(self.ESG['nomEtat'], "Ouvrir")

    @pyqtSlot()
    def on_btn_ESGPDF_clicked(self):
        self.acc_ESG(self.ESG['nomEtat'], "PDF")

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

    # Graphiques
    @pyqtSlot()
    def on_btn_histoType_clicked(self):
        action = "Ouvrir"
        self.acc_graphiqueDetail(self.histoType['nomEtat'], self.histoType['nomEtat2'], self.histoType['nomGraphique'], self.histoType['sourceSQL'], self.histoType['sourceSQL2'], self.histoType['titre1'], self.histoType['titre2'], action)

    @pyqtSlot()
    def on_btn_histoTypePDF_clicked(self):
        action = "PDF"
        self.acc_graphiqueDetail(self.histoType['nomEtat'], self.histoType['nomEtat2'], self.histoType['nomGraphique'], self.histoType['sourceSQL'], self.histoType['sourceSQL2'], self.histoType['titre1'], self.histoType['titre2'], action)

    @pyqtSlot()
    def on_btn_gType_clicked(self):
        action = "Ouvrir"
        self.acc_graphique(self.gType['nomEtat'], self.gType['nomGraphique'], self.gType['sourceSQL'], action)

    @pyqtSlot()
    def on_btn_gTypePDF_clicked(self):
        action = "PDF"
        self.acc_graphique(self.gType['nomEtat'], self.gType['nomGraphique'], self.gType['sourceSQL'], action)

    @pyqtSlot()
    def on_btn_gRating_clicked(self):
        action = "Ouvrir"
        self.acc_graphiqueDetail(self.gRating['nomEtat'], self.gRating['nomEtat2'], self.gRating['nomGraphique'], self.gRating['sourceSQL'], self.gRating['sourceSQL2'], self.gRating['titre1'], self.gRating['titre2'], action)

    @pyqtSlot()
    def on_btn_gRatingPDF_clicked(self):
        action = "PDF"
        self.acc_graphiqueDetail(self.gRating['nomEtat'], self.gRating['nomEtat2'], self.gRating['nomGraphique'], self.gRating['sourceSQL'], self.gRating['sourceSQL2'], self.gRating['titre1'], self.gRating['titre2'], action)

    @pyqtSlot()
    def on_btn_gSecteur_clicked(self):
        action = "Ouvrir"
        self.acc_graphiqueDetail(self.gSecteur['nomEtat'], self.gSecteur['nomEtat2'], self.gSecteur['nomGraphique'], self.gSecteur['sourceSQL'], self.gSecteur['sourceSQL2'], self.gSecteur['titre1'], self.gSecteur['titre2'], action)

    @pyqtSlot()
    def on_btn_gSecteurPDF_clicked(self):
        action = "PDF"
        self.acc_graphiqueDetail(self.gSecteur['nomEtat'], self.gSecteur['nomEtat2'], self.gSecteur['nomGraphique'], self.gSecteur['sourceSQL'], self.gSecteur['sourceSQL2'], self.gSecteur['titre1'], self.gSecteur['titre2'], action)

    @pyqtSlot()
    def on_btn_gCorp_clicked(self):
        action = "Ouvrir"
        self.acc_graphiqueDetail(self.gCorp['nomEtat'], self.gCorp['nomEtat2'], self.gCorp['nomGraphique'], self.gCorp['sourceSQL'], self.gCorp['sourceSQL2'], self.gCorp['titre1'], self.gCorp['titre2'], action)

    @pyqtSlot()
    def on_btn_gCorpPDF_clicked(self):
        action = "PDF"
        self.acc_graphiqueDetail(self.gCorp['nomEtat'], self.gCorp['nomEtat2'], self.gCorp['nomGraphique'], self.gCorp['sourceSQL'], self.gCorp['sourceSQL2'], self.gCorp['titre1'], self.gCorp['titre2'], action)

    @pyqtSlot()
    def on_btn_gFin_clicked(self):
        action = "Ouvrir"
        self.acc_graphiqueDetail(self.gFin['nomEtat'], self.gFin['nomEtat2'], self.gFin['nomGraphique'], self.gFin['sourceSQL'], self.gFin['sourceSQL2'], self.gFin['titre1'], self.gFin['titre2'], action)

    @pyqtSlot()
    def on_btn_gFinPDF_clicked(self):
        action = "PDF"
        self.acc_graphiqueDetail(self.gFin['nomEtat'], self.gFin['nomEtat2'], self.gFin['nomGraphique'], self.gFin['sourceSQL'], self.gFin['sourceSQL2'], self.gFin['titre1'], self.gFin['titre2'], action)

    @pyqtSlot()
    def on_btn_gGovnt_clicked(self):
        action = "Ouvrir"
        self.acc_graphiqueDetail(self.gGovnt['nomEtat'], self.gGovnt['nomEtat2'], self.gGovnt['nomGraphique'], self.gGovnt['sourceSQL'], self.gGovnt['sourceSQL2'], self.gGovnt['titre1'], self.gGovnt['titre2'], action)

    @pyqtSlot()
    def on_btn_gGovntPDF_clicked(self):
        action = "PDF"
        self.acc_graphiqueDetail(self.gGovnt['nomEtat'], self.gGovnt['nomEtat2'], self.gGovnt['nomGraphique'], self.gGovnt['sourceSQL'], self.gGovnt['sourceSQL2'], self.gGovnt['titre1'], self.gGovnt['titre2'], action)

    @pyqtSlot()
    def on_btn_emetteur_clicked(self):
        self.acc_etat(self.emetteur['nomEtat'], "Ouvrir")

    @pyqtSlot()
    def on_btn_emetteurPDF_clicked(self):
        self.acc_etat(self.emetteur['nomEtat'], "PDF")

    # Document complet
    @pyqtSlot()
    def on_btn_PDF_clicked(self):
        resultFileName = QFileDialog.getSaveFileName(self, "Save File", QDir(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)).filePath('exportation.pdf'),
                                                     "PDF (*.pdf)")[0]
        if resultFileName:
            list_cb_checked = [self.cb_titre.isChecked(), self.cb_avertissement.isChecked(), self.cb_sommaire.isChecked(), self.cb_synthese.isChecked(),
                               self.cb_ESG.isChecked(), self.cb_echeplus.isChecked(), self.cb_echeancier.isChecked(), self.cb_exigence.isChecked(),
                               self.cb_histoType.isChecked(), self.cb_gType.isChecked(), self.cb_gRating.isChecked(), self.cb_gSecteur.isChecked(),
                               self.cb_gCorp.isChecked(), self.cb_gFin.isChecked(), self.cb_gGovnt.isChecked(), self.cb_emetteur.isChecked()]
            nb_checked = sum(list_cb_checked)
            nb_pdfs = nb_checked
            if nb_checked == 0:
                nb_pdfs = len(list_cb_checked)

            progress = QProgressDialog("Exportation PDF", "Annuler", 0, nb_pdfs + 1, self)
            progress.setWindowTitle("Génération des états")
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            progress.setValue(0)

            tempdir = QTemporaryDir()
            # print(tempdir.path())

            self.error = False

            def file(i):
                return tempdir.filePath("{}.pdf".format(i)).replace("/", "\\")
            file_titre = tempdir.filePath("titre.pdf").replace("/", "\\")
            file_sommaire = tempdir.filePath("sommaire.pdf").replace("/", "\\")

            liste = [None] * 100

            if self.cb_synthese.isChecked() or nb_checked == 0:
                etat = self.synthese
                liste[etat['ordre']] = etat
            if self.cb_ESG.isChecked() or nb_checked == 0:
                etat = self.ESG
                liste[etat['ordre']] = etat
            if self.cb_echeplus.isChecked() or nb_checked == 0:
                etat = self.echeplus
                liste[etat['ordre']] = etat
            if self.cb_echeancier.isChecked() or nb_checked == 0:
                etat = self.echeancier
                liste[etat['ordre']] = etat
            if self.cb_exigence.isChecked() or nb_checked == 0:
                etat = self.exigence
                liste[etat['ordre']] = etat
            if self.cb_histoType.isChecked() or nb_checked == 0:
                etat = self.histoType
                liste[etat['ordre']] = etat
            if self.cb_gType.isChecked() or nb_checked == 0:
                etat = self.gType
                liste[etat['ordre']] = etat
            if self.cb_gRating.isChecked() or nb_checked == 0:
                etat = self.gRating
                liste[etat['ordre']] = etat
            if self.cb_gSecteur.isChecked() or nb_checked == 0:
                etat = self.gSecteur
                liste[etat['ordre']] = etat
            if self.cb_gCorp.isChecked() or nb_checked == 0:
                etat = self.gCorp
                liste[etat['ordre']] = etat
            if self.cb_gFin.isChecked() or nb_checked == 0:
                etat = self.gFin
                liste[etat['ordre']] = etat
            if self.cb_gGovnt.isChecked() or nb_checked == 0:
                etat = self.gGovnt
                liste[etat['ordre']] = etat
            if self.cb_emetteur.isChecked() or nb_checked == 0:
                etat = self.emetteur
                liste[etat['ordre']] = etat

            liste_generation = [item for index, item in enumerate(liste) if item]

            # titre
            # sommaire
            # avertissement

            nb_pages_total = 0
            break_bool = False
            if (self.cb_titre.isChecked() or nb_checked == 0) and not break_bool and not self.error:
                progress.setLabelText("Page de titre")
                QtCore.QCoreApplication.processEvents()
                etat = self.titre
                self.acc_titre(self.titre['nomEtat'], "PDF", file_titre)
                nb_pages_total += 1
                progress.setValue(progress.value() + 1)
                QtCore.QCoreApplication.processEvents()
                if progress.wasCanceled():
                    break_bool = True

            if self.cb_sommaire.isChecked() or nb_checked == 0:
                # Création plus tard
                nb_pages_total += 1

            if (self.cb_avertissement.isChecked() or nb_checked == 0) and not break_bool and not self.error:
                progress.setLabelText("Page d'avertissement")
                QtCore.QCoreApplication.processEvents()
                reader = PdfFileReader(self.file_avertissement)
                nb_pages = reader.getNumPages()
                nb_pages_total += nb_pages
                progress.setValue(progress.value() + 1)
                QtCore.QCoreApplication.processEvents()
                if progress.wasCanceled():
                    break_bool = True

            noteESG = False

            for i in range(len(liste_generation)):
                etat = liste_generation[i]
                print(etat['nomEtat'])
                progress.setLabelText(etat['nomEtat'])
                QtCore.QCoreApplication.processEvents()
                if progress.wasCanceled():
                    break_bool = True
                    break
                if etat['type'] == 'synthese':
                    self.acc_synthese(etat['nomEtat'], "PDF", fileName=file(i), nb_pages=nb_pages_total, noteESG=noteESG)
                if etat['type'] == 'ESG':
                    noteESG = self.acc_ESG(etat['nomEtat'], "PDF", fileName=file(i), nb_pages=nb_pages_total)
                    # Correction du problème de page blanche en trop
                    with open(file(i), 'rb') as infile:
                        reader = PdfFileReader(infile)
                        writer = PdfFileWriter()
                        writer.addPage(reader.getPage(0))
                        with open(file('output'), 'wb') as outfile:
                            writer.write(outfile)
                    os.remove(file(i))
                    os.rename(file('output'), file(i))
                if etat['type'] == 'etat':
                    self.acc_etat(etat['nomEtat'], "PDF", fileName=file(i), nb_pages=nb_pages_total)
                if etat['type'] == 'graphique':
                    self.acc_graphique(etat['nomEtat'], etat['nomGraphique'], etat['sourceSQL'], "PDF", fileName=file(i), nb_pages=nb_pages_total)
                if etat['type'] == 'graphiqueDetail':
                    self.acc_graphiqueDetail(etat['nomEtat'], etat['nomEtat2'], etat['nomGraphique'], etat['sourceSQL'], etat['sourceSQL2'], etat['titre1'], etat['titre2'], "PDF", fileName=file(i), nb_pages=nb_pages_total)
                if self.error:
                    break
                liste_generation[i]['first_page'] = nb_pages_total + 1
                reader = PdfFileReader(file(i))
                nb_pages = reader.getNumPages()
                nb_pages_total += nb_pages
                progress.setValue(progress.value() + 1)
                QtCore.QCoreApplication.processEvents()
                if progress.wasCanceled():
                    break_bool = True
                    break

            # CREATION DU SOMMAIRE
            liste_generation_sommaire = []
            bool_graph = False
            for i in range(len(liste_generation)):
                etat = liste_generation[i]
                if etat['type'] == 'graphiqueDetail' or etat['type'] == 'graphique':
                    if not bool_graph:
                        bool_graph = True
                        liste_generation_sommaire.append(liste_generation[i])
                else:
                    liste_generation_sommaire.append(liste_generation[i])

            if (self.cb_sommaire.isChecked() or nb_checked == 0) and not break_bool and not self.error:
                progress.setLabelText("Page de sommaire")
                QtCore.QCoreApplication.processEvents()
                # Ouverture de la base de données
                acc = win32.gencache.EnsureDispatch('Access.Application')
                acc.OpenCurrentDatabase(self.fileBDD, True)
                acc.DoCmd.OpenReport(self.sommaire['nomEtat'], win32.constants.acViewReport)
                imax = 0
                for i in range(len(liste_generation_sommaire)):
                    etat = liste_generation_sommaire[i]
                    acc.Reports.Item(self.sommaire['nomEtat']).Controls.Item("txt_titre{}".format(i + 1)).Caption = etat['titreSommaire'] + " ." * 200
                    acc.Reports.Item(self.sommaire['nomEtat']).Controls.Item("txt_page{}".format(i + 1)).Caption = "page " + str(etat['first_page'])
                    imax = i
                for i in range(imax + 1, 8):
                    acc.Reports.Item(self.sommaire['nomEtat']).Controls.Item("txt_titre{}".format(i + 1)).Caption = ""
                    acc.Reports.Item(self.sommaire['nomEtat']).Controls.Item("txt_page{}".format(i + 1)).Caption = ""
                acc.DoCmd.OutputTo(win32.constants.acOutputReport, self.sommaire['nomEtat'], win32.constants.acFormatPDF, file_sommaire)
                acc.Quit()
                progress.setValue(progress.value() + 1)
                QtCore.QCoreApplication.processEvents()
                if progress.wasCanceled():
                    break_bool = True

            # FUSION
            if not break_bool and not self.error:
                progress.setLabelText("Fusion")
                QtCore.QCoreApplication.processEvents()
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
                progress.setValue(progress.value() + 1)
                QtCore.QCoreApplication.processEvents()

                QMessageBox.information(self, "Exportation PDF", "Exportation terminée")
                os.startfile(resultFileName)
            else:
                progress.setValue(nb_pdfs + 1)
                tempdir.remove()
                QMessageBox.critical(self, "Exportation PDF", "Exportation annulée")
