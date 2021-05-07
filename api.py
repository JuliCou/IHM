import os
from copy import deepcopy
from flask import Flask, request, render_template, json
import pandas as pd
import pickle
import eli5
import seaborn as sns
import matplotlib.pyplot as plt
from pylab import *
import random
from sklearn.metrics import accuracy_score
import time


# Création de l'API Flask
app = Flask(__name__)

# Importation des données
studentInfo = pd.read_csv('moodle_files/studentInfo.csv', header=0, sep=",", encoding="ISO-8859-1")

# Importation des datasets complets selon le temps
time_range = range(0, 110, 10)
dic_c_df = {t:[] for t in time_range}
dic_c_df[time_range[0]] = pd.read_csv('complete_dataframes/df_t0.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time_range[1]] = pd.read_csv('complete_dataframes/df_t1.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time_range[2]] = pd.read_csv('complete_dataframes/df_t2.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time_range[3]] = pd.read_csv('complete_dataframes/df_t3.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time_range[4]] = pd.read_csv('complete_dataframes/df_t4.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time_range[5]] = pd.read_csv('complete_dataframes/df_t5.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time_range[6]] = pd.read_csv('complete_dataframes/df_t6.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time_range[7]] = pd.read_csv('complete_dataframes/df_t7.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time_range[8]] = pd.read_csv('complete_dataframes/df_t8.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time_range[9]] = pd.read_csv('complete_dataframes/df_t9.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time_range[10]] = pd.read_csv('complete_dataframes/df_t10.csv', header=0, sep=",", encoding="ISO-8859-1")

# Importation des 10 modèles
dic_models = {t:[] for t in time_range}
dic_models[time_range[0]] = pickle.load(open('models/model_t0.sav', 'rb'))
dic_models[time_range[1]] = pickle.load(open('models/model_t1.sav', 'rb'))
dic_models[time_range[2]] = pickle.load(open('models/model_t2.sav', 'rb'))
dic_models[time_range[3]] = pickle.load(open('models/model_t3.sav', 'rb'))
dic_models[time_range[4]] = pickle.load(open('models/model_t4.sav', 'rb'))
dic_models[time_range[5]] = pickle.load(open('models/model_t5.sav', 'rb'))
dic_models[time_range[6]] = pickle.load(open('models/model_t6.sav', 'rb'))
dic_models[time_range[7]] = pickle.load(open('models/model_t7.sav', 'rb'))
dic_models[time_range[8]] = pickle.load(open('models/model_t8.sav', 'rb'))
dic_models[time_range[9]] = pickle.load(open('models/model_t9.sav', 'rb'))
dic_models[time_range[10]] = pickle.load(open('models/model_t10.sav', 'rb'))



def traitement_eleve(identifiant_eleve, temps, code_module=None, code_presentation=None):
    # Récupération données pour affichage tableau de bord du prof
    if code_module == None and code_presentation == None:
        etudiant = studentInfo[(studentInfo.id_student==identifiant_eleve)]
    else:
        etudiant = studentInfo[(studentInfo.code_module==code_module)&(studentInfo.code_presentation==code_presentation)]
        etudiant = etudiant[(studentInfo.id_student==identifiant_eleve)]
    target_classes = dic_models[temps].classes_
    time_ranges = list(dic_models.keys())
    donnees_eleves_affichage = []
    # Nettoyage dossier images
    for filename in os.listdir("static/figures/"):
        if filename.startswith('pie'):  # not to remove other images
            os.remove("static/figures/" + filename)
    for filename in os.listdir("static/figures/"):
        if filename.startswith('evolution'):  # not to remove other images
            os.remove("static/figures/" + filename)
    # Pour chaque module
    for i in range(etudiant.shape[0]):            
        # Récupération données de l'étudiant pour prédire résultat
        dfStudents = dic_c_df[temps][(studentInfo.code_module==etudiant.iloc[i]["code_module"])&\
                            (studentInfo.code_presentation==etudiant.iloc[i]["code_presentation"])]
        dfStudents = dfStudents[dfStudents["id_student"]==identifiant_eleve]
        dic = {}
        dic["code_module"] = etudiant.iloc[i]["code_module"]
        dic["code_presentation"] = etudiant.iloc[i]["code_presentation"]
        # predictions = dic_models[temps].predict(dfStudents.drop(['final_result', '_id'], axis=1))
        proba = dic_models[temps].predict_proba(dfStudents.drop(['final_result', '_id'], axis=1))
        # Calcul taux de réussite et d'échec prédits
        reussite = proba[0][0] + proba[0][2]
        echec = proba[0][1] + proba[0][3]
        dic["reussite"] = round(reussite*100)
        dic["echec"] = round(echec*100)
        # Création du graphique à afficher
        fig = plt.figure(figsize=(4, 4))
        plt.pie([reussite, echec], explode=[0, 0.15], colors=["#ffc107", "#f1145c"], startangle=90)
        fig.set_facecolor("#00d994")
        # Enregistrement du graphique à afficher en local
        nom_image_pie = "pie" + str(time.time()) + ".jpeg"
        plt.savefig("static/figures/" + nom_image_pie, bbox_inches='tight')
        dic["img_pie"] = "../static/figures/" + nom_image_pie
        # Suivi du temps pour génération de graphique
        suivi_reussite_temps = []
        x = []
        for t in time_ranges:
            if t <= temps:
                dfStudents = dic_c_df[t][(studentInfo.code_module==etudiant.iloc[i]["code_module"])&\
                            (studentInfo.code_presentation==etudiant.iloc[i]["code_presentation"])]
                dfStudents = dfStudents[dfStudents["id_student"]==identifiant_eleve]
                proba_t = dic_models[t].predict_proba(dfStudents.drop(['final_result', '_id'], axis=1))
                reussite_t = 0
                for j in range(len(proba[0])):
                    if target_classes[j]!="Fail" and target_classes[j]!="Withdrawn":
                        reussite_t += proba_t[0][j]*100
                suivi_reussite_temps.append(reussite_t)
                x.append(t)
        # Sauvegarde du graphique - évolution prédiction dans le temps
        fig = plt.figure(figsize=(4, 4))
        plt.plot(x, suivi_reussite_temps, color="#00d994")
        xlim(0, 100)
        ylim(0, 100)
        xlabel("Evolution du module (% temps)")
        ylabel("Prédiction de réussite (%)")
        fig.set_facecolor("#00d994")
        nom_image = "evolution" + str(time.time()) + ".jpeg"
        plt.savefig("static/figures/" + nom_image, bbox_inches='tight')
        dic["img_evolution"] = "../static/figures/" + nom_image
        # Comprendre les prédictions - Conseils
        expl = eli5.explain_prediction_xgboost(dic_models[temps], dfStudents.drop(['final_result', '_id'], axis=1).iloc[0])
        facteurs_pos = []
        facteurs_neg = []
        for j in range(len(expl.targets)):
            if expl.targets[j].target == "Fail":
                for feature in expl.targets[j].feature_weights.pos:
                    if not "BIAS" in feature.feature and not "id_student" in feature.feature and not "date" in feature.feature:
                        facteurs_neg.append(feature.feature)
            if expl.targets[j].target == "Pass":
                for feature in expl.targets[j].feature_weights.pos:
                    if not "BIAS" in feature.feature and not "id_student" in feature.feature and not "date" in feature.feature:
                        facteurs_pos.append(feature.feature)
        dic["conseil_pos"] = facteurs_pos[:2]
        dic["conseil_neg"] = facteurs_neg[:2]
        #
        donnees_eleves_affichage.append(dic)
    return donnees_eleves_affichage


@app.route('/index', methods=['POST', 'GET'])
def routage():
    """Routing function"""
    if request.method == 'POST':
        route = request.form.getlist("choix")

        if route[0] == 'profil_prof':
            # Récupération données formulaire
            code_module = request.form["code_module"]
            code_presentation = request.form["code_presentation"]
            temps = int(request.form["temps"])
            dic = {"code_module": code_module, "code_presentation": code_presentation, "temps": temps}

            # Récupération données pour affichage tableau de bord du prof
            students = studentInfo[(studentInfo.code_module==code_module)&(studentInfo.code_presentation==code_presentation)]
            dfStudents = dic_c_df[temps][(studentInfo.code_module==code_module)&(studentInfo.code_presentation==code_presentation)]
            # dfStudents = dic_c_df[temps][dic_df[temps]["_id"].isin(list(dfStudents["_id"]))]
            # Si pas d'étudiants
            if dfStudents.shape[0] == 0:
                return render_template("page_erreur_prof.html")

            # Si étudiants trouvés :
            # Prédictions
            target_classes = dic_models[temps].classes_
            predictions = dic_models[temps].predict(dfStudents.drop(['final_result', '_id'], axis=1))
            accuracy = accuracy_score(predictions, list(dfStudents['final_result']))
            proba = dic_models[temps].predict_proba(dfStudents.drop(['final_result', '_id'], axis=1))
            dic["precision"] = round(accuracy*100)
            data_OK = []
            data_alerte = []
            for i in range(dfStudents.shape[0]):
                dt = {}
                dt["id_student"] = students.iloc[i].id_student
                reussite = proba[i][0] + proba[i][2]
                echec = proba[i][1] + proba[i][3]
                if echec > reussite:
                    dt["predicted_result"] = "Echec"
                    data_alerte.append(dt)
                else:
                    dt["predicted_result"] = "Réussite"
                    data_OK.append(dt)
            dic["nb_students"] = dfStudents.shape[0]
            dic["nb_students_reussite"] = len(data_OK)
            dic["nb_students_alerte"] = len(data_alerte)

            # Caractéristiques importantes
            # Feature Importance - modèle général
            importance = dic_models[temps].get_booster().get_score(importance_type='weight')
            features_importance_df2 = pd.DataFrame({"Features":list(importance.keys()), "Importance":list(importance.values())})
            features_importance_df2 = features_importance_df2.sort_values(by="Importance", ascending=False)
            # fi_df2 = features_importance_df2.iloc[range(10)]
            feature = features_importance_df2["Features"].iloc[0]
            i = 1
            while feature == "" or "bias" in feature.lower() or "id_student" in feature.lower():
                feature = features_importance_df2["Features"].iloc[i]
                i += 1
            dic["importance"] = feature
            return render_template('dashboard_prof.html', dic_renseignement=dic, data_OK=data_OK, data_alerte=data_alerte)

        if route[0] == 'profil_eleve':
            identifiant_eleve = int(request.form["identifiant"])
            temps = int(request.form["temps"])
            donnees_eleves_affichage = traitement_eleve(identifiant_eleve, temps)
            return render_template('dashboard_eleve.html', data=donnees_eleves_affichage)

    return render_template("index.html")


@app.route('/prof_voir_eleve', methods=['POST', 'GET'])
def prof_voir_eleve():
    """Index function"""
    if request.method == 'POST':
        # Récupération des données du formulaire
        donnees_cours = eval(request.form.getlist("data_general")[0])
        donnees_eleves = eval(request.form.getlist("data_eleve")[0])
        identifiant_eleve = donnees_eleves["id_student"]
        temps = donnees_cours["temps"]
        code_module = donnees_cours["code_module"]
        code_presentation = donnees_cours["code_presentation"]
        donnees_eleves_affichage = traitement_eleve(identifiant_eleve, temps, code_module, code_presentation)
        return render_template('dashboard_eleve.html', data=donnees_eleves_affichage)

    return render_template('index.html')



@app.route('/')
def index():
    """Index function"""
    if request.method == 'GET':
        # Liste des élèves
        identifiant_student = list(dic_c_df[time_range[0]].id_student.unique())
        code_module = list(studentInfo.code_module.unique())
        code_presentation = list(studentInfo.code_presentation.unique())
        dic_prof = {"code_module": code_module, "code_presentation":code_presentation}
        dic_eleve = {"id_student" : identifiant_student[:100]}
        
        return render_template('index.html', dic_prof=dic_prof, dic_eleve = dic_eleve)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
