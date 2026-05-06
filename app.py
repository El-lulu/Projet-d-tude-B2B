from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    bdd = sqlite3.connect('BDD/agri.db')
    bdd.row_factory = sqlite3.Row
    return bdd

@app.route('/')
def index():
    bdd = get_db_connection()
    meteo = bdd.execute('SELECT * FROM meteo ORDER BY date DESC LIMIT 1').fetchone()
    parcelles = bdd.execute('SELECT * FROM parcelles').fetchall()
    alertes_critiques = bdd.execute('SELECT * FROM alertes WHERE niveau = 3').fetchall()


    bdd.close()

    return render_template('main.html', meteo=meteo, parcelles=parcelles, alertes_critiques=alertes_critiques)


@app.route('/parcelles')
def page_parcelles():
    bdd = get_db_connection()
    # On récupère les parcelles
    parcelles = bdd.execute('SELECT * FROM parcelles').fetchall()
    
    # On récupère toutes les observations
    # J'assume que ta table a les colonnes 'parcelle_id' et 'texte'
    observations = bdd.execute('SELECT * FROM observations').fetchall()
    bdd.close()
    
    return render_template('parcelles.html', parcelles=parcelles, observations=observations)

@app.route('/alerte')
def page_alerte():
    bdd = get_db_connection()
    toutes_alertes = bdd.execute('SELECT * FROM alertes ORDER BY date DESC').fetchall()
    bdd.close()
    return render_template('alerte.html', alertes=toutes_alertes)

@app.route('/meteo')
def page_meteo():
    bdd = get_db_connection()
    historique = bdd.execute('SELECT * FROM meteo ORDER BY date DESC').fetchall()
    bdd.close()
    return render_template('meteo.html', historique=historique)


if __name__ == '__main__':
    app.run(debug=True)