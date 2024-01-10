from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import current_user, login_required

from flaskDir.source.prenotazioni.services import PrenotazioneService, FascicoloService

areautente_blueprint = Blueprint('areautente', __name__)

@areautente_blueprint.route('/storico')
@login_required
def storico():

    return render_template("Storico.html", lista=PrenotazioneService.getListaPrenotazioni(current_user))



@areautente_blueprint.route('/fascicolo',methods=['GET','POST'])
@login_required
def getFascicolobyUtente(paziente=None):
    if paziente is None:
        paziente = request.args.get('paziente')
    return render_template("FascicoloElettronico.html",listaDOC= FascicoloService.getDocumentiSanitari(paziente).all(),cfPaziente=paziente)



@areautente_blueprint.route('/addDocumento',methods=['GET','POST'])
@login_required
def addDocumento():
    if request.method == 'POST':
        num=request.form.get('num')
        tipo=request.form.get('tipo')
        data = request.form.get('data')
        descrizione = request.form.get('descrizione')
        paziente = request.form.get('cf')
        FascicoloService.addDocumento(num,tipo,data,descrizione,paziente)
    return redirect(url_for('areautente.getFascicolobyUtente', paziente=paziente))