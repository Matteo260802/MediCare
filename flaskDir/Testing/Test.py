import pytest
import sqlalchemy

from flaskDir import app, db
from flaskDir.MediCare.model.entity.EnteSanitario import EnteSanitario
from flaskDir.MediCare.model.entity.Medici import Medico
from flaskDir.source.prenotazioni.services import PrenotazioneService


@pytest.fixture
def client():
    app.config.update({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
def test_paginaPrenotazioni(client):
    response = client.get("/prenotazione")
    assert response.status_code == 200

def test_paginaLogin(client):
    response = client.get('/auth/login')
    assert response.status_code == 200

def test_paginaRegistrazione(client):
    response = client.get('/registrazione')
    assert response.status_code == 200

def test_paginaVaccini(client):
    response = client.get('/vaccini')
    assert response.status_code == 200

def test_paginaFarmaci(client):
    response = client.get('/farmaci')
    assert response.status_code == 200

def test_dettagliFarmaco(client):
    response = client.get('/dettagliFarmaco')
    assert response.status_code == 200


#Controllare che solo l'ente possa accedervi!
def test_area_ente(client):
    response = client.get('/ente')
    assert response.status_code == 200

#Testare che solo l'ente possa accedervi!
def test_crea_medico(client):
    response = client.get('/creaMedico')
    assert response.status_code == 200


#Testare che solo l'utente possa accedervi!
def test_area_utente(client):
    response = client.get('/areaUtente')
    assert response.status_code == 200

def test_dati_sanitari(client):
    response = client.get('/datiSanitari')
    assert response.status_code == 200

def test_area_diagnostica(client):
    response = client.get('/areaDiagnostica')
    assert response.status_code == 200

def test_modifica_dati_utente(client):
    response = client.get('/modificaDatiUtente')
    assert response.status_code == 200

def test_lista_medici(client):
    response = client.get('/listamedici')
    assert response.status_code == 200


def test_prenotazioni_lista_medici_filtro(client):
    citta ="Napoli"
    specializzazione="chirurgia"
    parametri={"citta":citta,"specializzazione":specializzazione}
    response = client.get('/prenotazione/listamedici', query_string=parametri) #query string mette i parametri nella get

    listamedici = PrenotazioneService.getListaMedici("chirurgia", "Napoli")
    #Controllo che tutti i medici risultanti abbiano le caratteristiche scelte
    assert all(medico.città==citta and medico.specializzazione==specializzazione for medico in listamedici)
    #Controllo che i medici risultanti siano uguali all'oracolo
    oracolo = Medico.query.filter_by(città=citta, specializzazione=specializzazione).all()
    attributi_oracolo = {(medico.email) for medico in oracolo}
    attributi_attuali = {(medico.email) for medico in listamedici}
    assert attributi_oracolo == attributi_attuali


def test_login_MedicoService():
    new_user = Medico(
        email='test@example.com',
        password_hash='password123',
        nome='John',
        cognome='Doe',
        iscrizione_albo= 123242,
        specializzazione = "chirurgia",
        città = "Napoli"
    )
    with app.app_context():
        user_in_db = db.session.scalar(sqlalchemy.select(Medico).where(Medico.email == 'test@example.com'))
        if user_in_db is not None:
            db.session.delete(user_in_db)
            db.session.commit()
        db.session.add(new_user)
        db.session.commit()

        user_in_db = Medico.query.filter_by(email='test@example.com').first()
        assert user_in_db

        user_in_db.set_password('newpassword123')
        db.session.commit()
        assert user_in_db.check_password('newpassword123')
        assert user_in_db.check_password('password123') is False


def test_login_Medico(client):
    credenzialiTest = {"email":"test@example.com", "password":"newpassword123"}
    response = client.post('/auth/login', data=credenzialiTest)
    assert response.status_code==302
    assert not response.location.endswith('/login')
    ##Controlla che il path sia relativo

def test_login_Medico2(client):
    credenzialiTest = {"email":"test@example.com", "password":"sbagliata"}
    response = client.post('/auth/login', data=credenzialiTest)
    assert response.status_code==302
    assert response.location.endswith('/login')
    ##Controlla che il path sia relativo



def test_login_EnteSanitario():
    new_user = EnteSanitario(
        nome='Ente Test',
        email='test@example.com',
        password_hash='sfjfsgs',
    )
    with app.app_context():
        user_in_db = db.session.scalar(sqlalchemy.select(EnteSanitario).where(EnteSanitario.email == 'test@example.com'))
        if user_in_db is not None:
            db.session.delete(user_in_db)
            db.session.commit()

        db.session.add(new_user)
        db.session.commit()

        user_in_db = db.session.scalar(sqlalchemy.select(EnteSanitario).where(EnteSanitario.email == 'test@example.com'))
        assert user_in_db

        user_in_db.set_password('corretta')
        db.session.commit()
        assert user_in_db.check_password('corretta')
        assert user_in_db.check_password('password123') is False


def test_login_Ente(client):
    credenzialiTest = {"email": "test@example.com", "password": "corretta"}
    response = client.post('/auth/loginente', data=credenzialiTest)
    assert response.status_code == 302
    assert not response.location.endswith('/loginente')#Login con Successo



def test_login_Ente2(client):
    credenzialiTest = {"email": "test@example.com", "password": "sbagliata"}
    response = client.post('/auth/loginente', data=credenzialiTest)
    assert response.status_code == 302
    assert response.location.endswith('/loginente')  # Email o password errate

    ##Controlla che il path sia relativo

def test_registrazioneMedico(client):
    credenzialiTest = {"email": "test2@example.com", "password": "sbagliata", "nome":"Giovanni", "cognome":"casaburi", "specializzazione":"chirurgia", "citta":"Piccola Svizzera", "code":123212}
    response = client.post('/auth/registrazione', data=credenzialiTest)
    assert response.status_code == 302
    assert not response.location.endswith('/registrazione')


"""
def test_prenotazione():
    dataprenotazione ='2988-01-12 00:00:00'
    with app.app_context():
        if PrenotazioneService.confirmIsFree("test@example.com",dataprenotazione,"9"):
            PrenotazioneService.savePrenotazione("test@example.com",dataprenotazione,"9", "dfsh", 2323)

"""
