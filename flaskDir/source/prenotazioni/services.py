import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

from flaskDir import db
from flaskDir.MediCare.model.entity.DocumentoSanitario import DocumentoSanitario
from flaskDir.MediCare.model.entity.EnteSanitario import EnteSanitario
from flaskDir.MediCare.model.entity.Medici import Medico
from flaskDir.MediCare.model.entity.Paziente import Paziente
from flaskDir.MediCare.model.entity.Prenotazione import Prenotazione




class MedicoService:
    """

    """
    #Invece di fare operazioni di input output ad ogni richiesta, memorizzo listamedici
    _listaMedici = None

    @staticmethod
    def getMedico(idMedico):
        return Medico.query.filter_by(email=idMedico).first()


    @staticmethod
    def retrieveMedico(email, password):
        medico = db.session.scalar(sqlalchemy.select(Medico).where(Medico.email == email))
        if medico is None or not medico.check_password(password):
            return None
        return medico

    @classmethod
    def getListaMedici(cls):
        if cls._listaMedici is None:
            cls._listaMedici = Medico.query.all()
        return cls._listaMedici

    def filtraMedici(cls, specializzazione = None, citta = None):
        cls._listaMedici = cls.getListaMedici()

        if specializzazione is None and citta is None:
            return cls._listaMedici

        newList = []
        if specializzazione is not None and citta is not None:
            newList = [medico for medico in cls._listaMedici if medico.città == citta and specializzazione == specializzazione]

        elif citta is not None:
            newList = [medico for medico in cls._listaMedici if medico.città == citta]

        elif specializzazione is not None:
            newList = [medico for medico in cls._listaMedici if medico.specializzazione == specializzazione]

        return newList

    def filtraMediciv2(cls, specializzazione = None, citta = None):
        cls._listaMedici = cls.getListaMedici()

        if specializzazione is None and citta is None:
            return cls._listaMedici

        listaFiltrata = []
        condizioniDaVerificare = []

        if specializzazione is not None:
            condizioniDaVerificare.append(lambda medico: medico.specializzazione == specializzazione)
        if citta is not None:
            condizioniDaVerificare.append(lambda medico: medico.città == citta)

        listaFiltrata = [medico for medico in cls._listaMedici if all(condition(medico) for condition in condizioniDaVerificare)]

        return listaFiltrata

    @classmethod
    def addMedicotoLista(cls, medico):
        cls._listaMedici = cls.getListaMedici()
        cls._listaMedici.append(medico)

class UserService:

    @classmethod
    def getListaVaccini(cls, user):
        return DocumentoSanitario.query.filter_by(titolare=user.CF, tipo="vaccino")

    @classmethod
    def getListaPrenotazioni(cls, user):
        return db.session.scalar(sqlalchemy.select(Prenotazione).where(Prenotazione.pazienteCF == user.CF))

class PrenotazioneService:

    @classmethod
    def getListaMedici(cls,specializzazione = None, citta= None):
        return MedicoService().filtraMedici(specializzazione,citta)
    @classmethod
    def getListaVaccini(cls,user):
        return UserService.getListaVaccini(user)

    @classmethod
    def getListaPrenotazioni(cls, user):
        return UserService.getListaPrenotazioni(user)
    @classmethod
    def confirmIsFree(cls, idmedico, data, ora):
        prenotazioni = Prenotazione.query.filter_by(medico=idmedico, oraVisita=ora, dataVisita=data).first()
        if prenotazioni: #Se ci sono prenotazioni per quella data allora non è free
            return False
        return True

    @staticmethod
    def savePrenotazione (idmedico, data, ora, tipo, CF):

        try:
            medico=MedicoService().getMedico(idmedico)

            prenotazione = Prenotazione()
            prenotazione.medico = idmedico
            prenotazione.pazienteCF = CF
            prenotazione.tipoVisita = tipo
            prenotazione.dataVisita = data
            prenotazione.oraVisita = ora

            db.session.add(prenotazione)

            db.session.commit()

        except SQLAlchemyError as e:
            print("Errore mentre salvavo la prenotazione: {}".format(e))

            db.session.rollback()

            return False



class EnteService:
    @staticmethod
    def retrieveEnte(email, password):
        ente = db.session.scalar(sqlalchemy.select(EnteSanitario).where(EnteSanitario.email == email))
        if ente is None or not ente.check_password(password):
            return None
        return ente



class FascicoloService:

    @classmethod
    def getDocumentiSanitari(cls, cf):
        return DocumentoSanitario.query.filter_by(titolare=cf)















