from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    bdd = sqlite3.connect('BDD/agri.db')
    bdd.row_factory = sqlite3.Row
    return bdd

# ROUTES PAGES 

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
    parcelles = bdd.execute('SELECT * FROM parcelles').fetchall()
    observations = bdd.execute('SELECT * FROM observations').fetchall()
    bdd.close()
    return render_template('parcelles.html', parcelles=parcelles, observations=observations)

@app.route('/alerte')
def page_alerte():
    bdd = get_db_connection()
    query = '''
        SELECT a.*, p.nom AS parcelle_nom 
        FROM alertes a 
        JOIN parcelles p ON a.parcelle_id = p.id 
        ORDER BY a.date DESC
    '''
    historique = bdd.execute(query).fetchall()
    parcelles = bdd.execute('SELECT * FROM parcelles').fetchall()
    bdd.close()
    return render_template('alerte.html', historique=historique, parcelles=parcelles)

@app.route('/meteo')
def page_meteo():
    bdd = get_db_connection()
    historique = bdd.execute('SELECT * FROM meteo ORDER BY date DESC').fetchall()
    bdd.close()
    return render_template('meteo.html', historique=historique)

# API PARCELLES 

@app.route('/api/parcelles', methods=['POST'])
def ajouter_parcelle():
    try:
        data = request.get_json()
        nom = data.get('nom')
        localisation = data.get('localisation')
        surface_ha = data.get('surface_ha')
        
        if not all([nom, localisation, surface_ha]):
            return jsonify({'success': False, 'message': 'Tous les champs sont obligatoires'}), 400
        
        bdd = get_db_connection()
        dernier_id = bdd.execute('SELECT MAX(id) as max_id FROM parcelles').fetchone()
        nouvel_id = (dernier_id['max_id'] or 0) + 1
        
        bdd.execute(
            'INSERT INTO parcelles (id, nom, localisation, surface_ha) VALUES (?, ?, ?, ?)',
            (nouvel_id, nom, localisation, float(surface_ha))
        )
        bdd.commit()
        bdd.close()
        
        return jsonify({'success': True, 'message': 'Parcelle ajoutée avec succès', 'id': nouvel_id})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/parcelles/<int:parcelle_id>', methods=['PUT'])
def modifier_parcelle(parcelle_id):
    try:
        data = request.get_json()
        nom = data.get('nom')
        localisation = data.get('localisation')
        surface_ha = data.get('surface_ha')
        
        if not all([nom, localisation, surface_ha]):
            return jsonify({'success': False, 'message': 'Tous les champs sont obligatoires'}), 400
        
        bdd = get_db_connection()
        parcelle = bdd.execute('SELECT * FROM parcelles WHERE id = ?', (parcelle_id,)).fetchone()
        if not parcelle:
            bdd.close()
            return jsonify({'success': False, 'message': 'Parcelle non trouvée'}), 404
        
        bdd.execute(
            'UPDATE parcelles SET nom = ?, localisation = ?, surface_ha = ? WHERE id = ?',
            (nom, localisation, float(surface_ha), parcelle_id)
        )
        bdd.commit()
        bdd.close()
        
        return jsonify({'success': True, 'message': 'Parcelle modifiée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/parcelles/<int:parcelle_id>', methods=['DELETE'])
def supprimer_parcelle(parcelle_id):
    try:
        bdd = get_db_connection()
        parcelle = bdd.execute('SELECT * FROM parcelles WHERE id = ?', (parcelle_id,)).fetchone()
        if not parcelle:
            bdd.close()
            return jsonify({'success': False, 'message': 'Parcelle non trouvée'}), 404
        
        bdd.execute('DELETE FROM cultures WHERE parcelle_id = ?', (parcelle_id,))
        bdd.execute('DELETE FROM observations WHERE parcelle_id = ?', (parcelle_id,))
        bdd.execute('DELETE FROM alertes WHERE parcelle_id = ?', (parcelle_id,))
        bdd.execute('DELETE FROM parcelles WHERE id = ?', (parcelle_id,))
        bdd.commit()
        bdd.close()
        
        return jsonify({'success': True, 'message': 'Parcelle supprimée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API MÉTÉO 

@app.route('/api/meteo', methods=['POST'])
def ajouter_meteo():
    try:
        data = request.get_json()
        date = data.get('date')
        temperature = data.get('temperature')
        humidite = data.get('humidite')
        pluie_mm = data.get('pluie_mm')
        
        if not all([date, temperature is not None, humidite is not None, pluie_mm is not None]):
            return jsonify({'success': False, 'message': 'Tous les champs sont obligatoires'}), 400
        
        bdd = get_db_connection()
        existe = bdd.execute('SELECT date FROM meteo WHERE date = ?', (date,)).fetchone()
        if existe:
            bdd.close()
            return jsonify({'success': False, 'message': 'Une entrée existe déjà pour cette date'}), 400
        
        bdd.execute(
            'INSERT INTO meteo (date, temperature, humidite, pluie_mm) VALUES (?, ?, ?, ?)',
            (date, int(temperature), int(humidite), int(pluie_mm))
        )
        bdd.commit()
        bdd.close()
        
        return jsonify({'success': True, 'message': 'Donnée météo ajoutée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/meteo/<date>', methods=['PUT'])
def modifier_meteo(date):
    try:
        data = request.get_json()
        temperature = data.get('temperature')
        humidite = data.get('humidite')
        pluie_mm = data.get('pluie_mm')
        
        if not all([temperature is not None, humidite is not None, pluie_mm is not None]):
            return jsonify({'success': False, 'message': 'Tous les champs sont obligatoires'}), 400
        
        bdd = get_db_connection()
        meteo = bdd.execute('SELECT * FROM meteo WHERE date = ?', (date,)).fetchone()
        if not meteo:
            bdd.close()
            return jsonify({'success': False, 'message': 'Date non trouvée'}), 404
        
        bdd.execute(
            'UPDATE meteo SET temperature = ?, humidite = ?, pluie_mm = ? WHERE date = ?',
            (int(temperature), int(humidite), int(pluie_mm), date)
        )
        bdd.commit()
        bdd.close()
        
        return jsonify({'success': True, 'message': 'Donnée météo modifiée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/meteo/<date>', methods=['DELETE'])
def supprimer_meteo(date):
    try:
        bdd = get_db_connection()
        meteo = bdd.execute('SELECT * FROM meteo WHERE date = ?', (date,)).fetchone()
        if not meteo:
            bdd.close()
            return jsonify({'success': False, 'message': 'Date non trouvée'}), 404
        
        bdd.execute('DELETE FROM meteo WHERE date = ?', (date,))
        bdd.commit()
        bdd.close()
        
        return jsonify({'success': True, 'message': 'Donnée météo supprimée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API ALERTES 

@app.route('/api/alertes', methods=['POST'])
def ajouter_alerte():
    try:
        data = request.get_json()
        date = data.get('date')
        type_alerte = data.get('type')
        parcelle_id = data.get('parcelle_id')
        niveau = data.get('niveau')
        
        if not all([date, type_alerte, parcelle_id, niveau]):
            return jsonify({'success': False, 'message': 'Tous les champs sont obligatoires'}), 400
        
        if int(niveau) not in [1, 2, 3]:
            return jsonify({'success': False, 'message': 'Le niveau doit être 1, 2 ou 3'}), 400
        
        bdd = get_db_connection()
        parcelle = bdd.execute('SELECT id FROM parcelles WHERE id = ?', (parcelle_id,)).fetchone()
        if not parcelle:
            bdd.close()
            return jsonify({'success': False, 'message': 'Parcelle non trouvée'}), 404
        
        bdd.execute(
            'INSERT INTO alertes (date, type, parcelle_id, niveau) VALUES (?, ?, ?, ?)',
            (date, type_alerte, int(parcelle_id), int(niveau))
        )
        bdd.commit()
        bdd.close()
        
        return jsonify({'success': True, 'message': 'Alerte ajoutée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/alertes/<int:alerte_id>', methods=['PUT'])
def modifier_alerte(alerte_id):
    try:
        data = request.get_json()
        date = data.get('date')
        type_alerte = data.get('type')
        parcelle_id = data.get('parcelle_id')
        niveau = data.get('niveau')
        
        if not all([date, type_alerte, parcelle_id, niveau]):
            return jsonify({'success': False, 'message': 'Tous les champs sont obligatoires'}), 400
        
        if int(niveau) not in [1, 2, 3]:
            return jsonify({'success': False, 'message': 'Le niveau doit être 1, 2 ou 3'}), 400
        
        bdd = get_db_connection()
        alerte = bdd.execute('SELECT * FROM alertes WHERE id = ?', (alerte_id,)).fetchone()
        if not alerte:
            bdd.close()
            return jsonify({'success': False, 'message': 'Alerte non trouvée'}), 404
        
        parcelle = bdd.execute('SELECT id FROM parcelles WHERE id = ?', (parcelle_id,)).fetchone()
        if not parcelle:
            bdd.close()
            return jsonify({'success': False, 'message': 'Parcelle non trouvée'}), 404
        
        bdd.execute(
            'UPDATE alertes SET date = ?, type = ?, parcelle_id = ?, niveau = ? WHERE id = ?',
            (date, type_alerte, int(parcelle_id), int(niveau), alerte_id)
        )
        bdd.commit()
        bdd.close()
        
        return jsonify({'success': True, 'message': 'Alerte modifiée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/alertes/<int:alerte_id>', methods=['DELETE'])
def supprimer_alerte(alerte_id):
    try:
        bdd = get_db_connection()
        alerte = bdd.execute('SELECT * FROM alertes WHERE id = ?', (alerte_id,)).fetchone()
        if not alerte:
            bdd.close()
            return jsonify({'success': False, 'message': 'Alerte non trouvée'}), 404
        
        bdd.execute('DELETE FROM alertes WHERE id = ?', (alerte_id,))
        bdd.commit()
        bdd.close()
        
        return jsonify({'success': True, 'message': 'Alerte supprimée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

#  API OBSERVATIONS 

@app.route('/api/observations', methods=['POST'])
def ajouter_observation():
    try:
        data = request.get_json()
        date = data.get('date')
        etat = data.get('etat')
        parcelle_id = data.get('parcelle_id')
        commentaire = data.get('commentaire')
        
        if not all([date, etat, parcelle_id, commentaire]):
            return jsonify({'success': False, 'message': 'Tous les champs sont obligatoires'}), 400
        
        bdd = get_db_connection()
        
        parcelle = bdd.execute('SELECT id FROM parcelles WHERE id = ?', (parcelle_id,)).fetchone()
        if not parcelle:
            bdd.close()
            return jsonify({'success': False, 'message': 'Parcelle non trouvée'}), 404
        
        bdd.execute(
            'INSERT INTO observations (date, etat, parcelle_id, commentaire) VALUES (?, ?, ?, ?)',
            (date, etat, int(parcelle_id), commentaire)
        )
        bdd.commit()
        bdd.close()
        
        return jsonify({'success': True, 'message': 'Observation ajoutée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/observations/<int:obs_id>', methods=['DELETE'])
def supprimer_observation(obs_id):
    try:
        bdd = get_db_connection()
        
        observation = bdd.execute('SELECT * FROM observations WHERE id = ?', (obs_id,)).fetchone()
        if not observation:
            bdd.close()
            return jsonify({'success': False, 'message': 'Observation non trouvée'}), 404
        
        bdd.execute('DELETE FROM observations WHERE id = ?', (obs_id,))
        bdd.commit()
        bdd.close()
        
        return jsonify({'success': True, 'message': 'Observation supprimée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)