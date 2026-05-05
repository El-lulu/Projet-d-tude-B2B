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

if __name__ == '__main__':
    app.run(debug=True)