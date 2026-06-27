# api.py
from flask import Flask, request, jsonify, session
import os
import traceback
from dotenv import load_dotenv
from database import (
    get_formations, get_bourses,
    get_user_par_email, get_client, get_user_par_id,
    creer_user, email_exist, sauvegarder_recommendations, modifier_user_db
)
from model_nlp import recommender
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "edureco2-secret")

NIVEAUX = ['lycee', 'bac', 'licence', 'master', 'doctorat']
DOMAINES = ['informatique', 'medecine', 'droit', 'economie', 'ingenierie', 'science', 'arts', 'education']

# ─────────────────────────────────────────────
# GET /api/health
# ─────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'statut': 'ok', 'message': 'API EduReco fonctionne !'}), 200


# ─────────────────────────────────────────────
# POST /api/users
# ─────────────────────────────────────────────
@app.route('/api/users', methods=['POST'])
def creer_utilisateur():
    donnees = request.get_json()
    for champ in ['nom', 'prenom', 'email', 'pays', 'niveau_etudes', 'domaine']:
        if not donnees.get(champ):
            return jsonify({'succes': False, 'erreur': f"Champ obligatoire manquant : '{champ}'"}), 400
    if donnees['niveau_etudes'] not in NIVEAUX:
        return jsonify({'succes': False, 'erreur': f"Niveau invalide. Valeurs : {NIVEAUX}"}), 400
    if donnees['domaine'] not in DOMAINES:
        return jsonify({'succes': False, 'erreur': f"Domaine invalide. Valeurs : {DOMAINES}"}), 400
    if email_exist(donnees['email']):
        return jsonify({'succes': False, 'erreur': "Cet email est déjà utilisé"}), 409
    donnees['email'] = donnees['email'].lower().strip()
    try:
        user = creer_user(donnees)
        return jsonify({'succes': True, 'message': f"Bienvenue {user['prenom']} !", 'utilisateur': user}), 201
    except Exception as e:
        return jsonify({'succes': False, 'erreur': str(e)}), 500


# ─────────────────────────────────────────────
# POST /api/users/connexion
# ─────────────────────────────────────────────
@app.route('/api/users/connexion', methods=['POST'])
def connexion():
    donnees = request.get_json()
    email = donnees.get('email', '').lower().strip()
    if not email:
        return jsonify({'succes': False, 'erreur': "Email requis"}), 400
    user = get_user_par_email(email)
    if not user:
        return jsonify({'succes': False, 'erreur': "Email introuvable. Créez d'abord votre profil."}), 404
    return jsonify({'succes': True, 'message': f"Bienvenue {user['prenom']} ", 'utilisateur': user}), 200


# ─────────────────────────────────────────────
# GET /api/users/<user_id>
# ─────────────────────────────────────────────
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_par_id(user_id)
    if not user:
        return jsonify({'succes': False, 'erreur': "Utilisateur introuvable"}), 404
    return jsonify({'succes': True, 'utilisateur': user}), 200


# ─────────────────────────────────────────────
# PUT /api/users/<user_id>
# ─────────────────────────────────────────────
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def modifier_user(user_id):
    user = get_user_par_id(user_id)
    if not user:
        return jsonify({'succes': False, 'erreur': "Utilisateur introuvable."}), 404
    donnees = request.get_json()
    if 'niveau_etudes' in donnees and donnees['niveau_etudes'] not in NIVEAUX:
        return jsonify({'succes': False, 'erreur': f"Niveau invalide. Valeurs acceptées : {NIVEAUX}"}), 400
    if 'domaine' in donnees and donnees['domaine'] not in DOMAINES:
        return jsonify({'succes': False, 'erreur': f"Domaine invalide. Valeurs acceptées : {DOMAINES}"}), 400
    champs_autorises = ['nom', 'prenom', 'pays', 'niveau_etudes', 'domaine', 'objectif', 'langue']
    mise_a_jour = {cle: valeur for cle, valeur in donnees.items() if cle in champs_autorises and valeur is not None}
    if not mise_a_jour:
        return jsonify({'succes': False, 'erreur': "Aucun champ valide à modifier."}), 400
    try:
        user_modifie = modifier_user_db(user_id, mise_a_jour)
        return jsonify({'succes': True, 'message': "Profil mis à jour avec succès.", 'utilisateur': user_modifie}), 200
    except Exception as e:
        return jsonify({'succes': False, 'erreur': str(e)}), 500


# ─────────────────────────────────────────────
# GET /api/recommendations/<user_id>
# ─────────────────────────────────────────────
@app.route('/api/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    user = get_user_par_id(user_id)
    if not user:
        return jsonify({'succes': False, 'erreur': "Utilisateur introuvable"}), 404
    formations = get_formations()
    bourses = get_bourses()
    try:
        resultats = recommender(user, formations, bourses, nb=5)
    except Exception as e:
        return jsonify({'succes': False, 'erreur': f"Erreur NLP : {str(e)}", 'detail': traceback.format_exc()}), 500
    items = []
    for f in resultats['formations']:
        items.append({'user_id': user_id, 'item_id': f['id'], 'type_item': 'formation', 'score': int(f['pct']), 'raisons': f'Score NLP : {f["pct"]}%'})
    for b in resultats['bourses']:
        items.append({'user_id': user_id, 'item_id': b['id'], 'type_item': 'bourse', 'score': int(b['pct']), 'raisons': f'Score NLP : {b["pct"]}%'})
    sauvegarder_recommendations(user_id, items)
    return jsonify({'succes': True, 'utilisateur': user, 'formations': resultats['formations'], 'bourses': resultats['bourses'], 'texte_profil': resultats['texte_profil']})


# ─────────────────────────────────────────────
# GET /api/admin/stats
# ─────────────────────────────────────────────
@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    try:
        db = get_client()
        users = db.table('utilisateurs').select('*').execute().data or []
        reco  = db.table('recommendations').select('*').execute().data or []

        # Répartition par domaine
        par_domaine = {}
        for u in users:
            d = u.get('domaine', 'inconnu')
            par_domaine[d] = par_domaine.get(d, 0) + 1

        # Répartition par niveau
        par_niveau = {}
        for u in users:
            n = u.get('niveau_etudes', 'inconnu')
            par_niveau[n] = par_niveau.get(n, 0) + 1

        # Répartition par pays
        par_pays = {}
        for u in users:
            p = u.get('pays', 'inconnu')
            par_pays[p] = par_pays.get(p, 0) + 1

        # Score moyen
        scores = [r.get('score', 0) for r in reco if r.get('score') is not None]
        score_moyen = round(sum(scores) / len(scores), 1) if scores else 0

        # Nb formations et bourses recommandées
        nb_formations_reco = sum(1 for r in reco if r.get('type_item') == 'formation')
        nb_bourses_reco    = sum(1 for r in reco if r.get('type_item') == 'bourse')

        return jsonify({
            'succes': True,
            'stats': {
                'total_users':        len(users),
                'total_recos':        len(reco),
                'nb_formations_reco': nb_formations_reco,
                'nb_bourses_reco':    nb_bourses_reco,
                'score_moyen':        score_moyen,
                'par_domaine':        par_domaine,
                'par_niveau':         par_niveau,
                'par_pays':           par_pays,
            }
        }), 200

    except Exception as e:
        return jsonify({'succes': False, 'erreur': str(e), 'detail': traceback.format_exc()}), 500


# ─────────────────────────────────────────────
# GET /api/admin/users
# ─────────────────────────────────────────────
@app.route('/api/admin/users', methods=['GET'])
def admin_users():
    try:
        db = get_client()
        users = db.table('utilisateurs').select('*').execute().data or []
        return jsonify({'succes': True, 'users': users}), 200
    except Exception as e:
        return jsonify({'succes': False, 'erreur': str(e), 'detail': traceback.format_exc()}), 500


# ─────────────────────────────────────────────
# GET /api/admin/recommendations
# ─────────────────────────────────────────────
@app.route('/api/admin/recommendations', methods=['GET'])
def admin_recommendations():
    try:
        db = get_client()
        recos = db.table('recommendations').select('*').execute().data or []
        return jsonify({'succes': True, 'recommendations': recos}), 200
    except Exception as e:
        return jsonify({'succes': False, 'erreur': str(e), 'detail': traceback.format_exc()}), 500


# Démarrage du serveur
if __name__ == '__main__':
    print("API EduReco → http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
