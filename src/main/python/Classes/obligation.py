class Obligation:
    def __init__(self):
        self.ISIN = None
        self.Libelle = None


class ObligationContenir(Obligation):
    def __init__(self):
        Obligation.__init__(self)
        self.nombre = None
        self.prixAchat = None
        self.Valorisation = None
        self.ValorisationAC = None
