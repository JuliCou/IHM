import os
from copy import deepcopy
from flask import Flask, request, render_template, json
import pandas as pd
import pickle
import eli5
import seaborn as sns
from matplotlib import pyplot
import random
from sklearn.metrics import accuracy_score


app = Flask(__name__)

# Importation des données
studentInfo = pd.read_csv('moodle_files/studentInfo.csv', header=0, sep=",", encoding="ISO-8859-1")
# assessments = pd.read_csv('moodle_files/assessments.csv', header=0, sep=",", encoding="ISO-8859-1")
# courses = pd.read_csv('moodle_files/courses.csv', header=0, sep=",", encoding="ISO-8859-1")
# studentAssessment = pd.read_csv('moodle_files/studentAssessment.csv', header=0, sep=",", encoding="ISO-8859-1")
# studentRegistration = pd.read_csv('moodle_files/studentRegistration.csv', header=0, sep=",", encoding="ISO-8859-1")
# studentVle = pd.read_csv('moodle_files/studentVle.csv', header=0, sep=",", encoding="ISO-8859-1")
# vle = pd.read_csv('moodle_files/vle.csv', header=0, sep=",", encoding="ISO-8859-1")

# Importation des dataset selon le temps
time = range(0, 110, 10)
dic_df = {t:[] for t in time}
dic_df[time[0]] = pd.read_csv('dataframes/df_t0.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_df[time[1]] = pd.read_csv('dataframes/df_t1.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_df[time[2]] = pd.read_csv('dataframes/df_t2.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_df[time[3]] = pd.read_csv('dataframes/df_t3.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_df[time[4]] = pd.read_csv('dataframes/df_t4.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_df[time[5]] = pd.read_csv('dataframes/df_t5.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_df[time[6]] = pd.read_csv('dataframes/df_t6.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_df[time[7]] = pd.read_csv('dataframes/df_t7.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_df[time[8]] = pd.read_csv('dataframes/df_t8.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_df[time[9]] = pd.read_csv('dataframes/df_t9.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_df[time[10]] = pd.read_csv('dataframes/df_t10.csv', header=0, sep=",", encoding="ISO-8859-1")

# Importation des datasets complets selon le temps
time = range(0, 110, 10)
dic_c_df = {t:[] for t in time}
dic_c_df[time[0]] = pd.read_csv('complete_dataframes/df_t0.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time[1]] = pd.read_csv('complete_dataframes/df_t1.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time[2]] = pd.read_csv('complete_dataframes/df_t2.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time[3]] = pd.read_csv('complete_dataframes/df_t3.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time[4]] = pd.read_csv('complete_dataframes/df_t4.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time[5]] = pd.read_csv('complete_dataframes/df_t5.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time[6]] = pd.read_csv('complete_dataframes/df_t6.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time[7]] = pd.read_csv('complete_dataframes/df_t7.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time[8]] = pd.read_csv('complete_dataframes/df_t8.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time[9]] = pd.read_csv('complete_dataframes/df_t9.csv', header=0, sep=",", encoding="ISO-8859-1")
dic_c_df[time[10]] = pd.read_csv('complete_dataframes/df_t10.csv', header=0, sep=",", encoding="ISO-8859-1")

# Importation des 10 modèles
dic_models = {t:[] for t in time}
dic_models[time[0]] = pickle.load(open('models/model_t0.sav', 'rb'))
dic_models[time[1]] = pickle.load(open('models/model_t1.sav', 'rb'))
dic_models[time[2]] = pickle.load(open('models/model_t2.sav', 'rb'))
dic_models[time[3]] = pickle.load(open('models/model_t3.sav', 'rb'))
dic_models[time[4]] = pickle.load(open('models/model_t4.sav', 'rb'))
dic_models[time[5]] = pickle.load(open('models/model_t5.sav', 'rb'))
dic_models[time[6]] = pickle.load(open('models/model_t6.sav', 'rb'))
dic_models[time[7]] = pickle.load(open('models/model_t7.sav', 'rb'))
dic_models[time[8]] = pickle.load(open('models/model_t8.sav', 'rb'))
dic_models[time[9]] = pickle.load(open('models/model_t9.sav', 'rb'))
dic_models[time[10]] = pickle.load(open('models/model_t10.sav', 'rb'))

# Liste des élèves
identifiant_student = list(dic_df[time[0]].id_student.unique())
code_module = list(studentInfo.code_module.unique())
code_presentation = list(studentInfo.code_presentation.unique())


@app.route('/index', methods=['POST', 'GET'])
def routage():
    """Routing function"""
    if request.method == 'POST':
        route = request.form.getlist("choix")

        if route[0] == 'profil_prof':
            code_module = request.form["code_module"]
            code_presentation = request.form["code_presentation"]
            temps = request.form["temps"]
            print(code_module, code_presentation, temps)
            dic = {"code_module": code_module, "code_presentation":code_presentation, "date_perc": list(range(0, 110, 10))}
            return render_template('dashboard_prof.html', dic=dic)

        if route[0] == 'profil_eleve':
            identifiant_student = request.form["identifiant"]
            temps = request.form["temps"]
            print(identifiant_student, temps)
            dic = {"id_student" : identifiant_student, "date_perc": list(range(0, 110, 10))}
            return render_template('dashboard_eleve.html', dic=dic)

    return render_template("index.html")


@app.route('/')
def index():
    """Index function"""
    if request.method == 'GET':

        dic_prof = {"code_module": code_module, "code_presentation":code_presentation}
        dic_eleve = {"id_student" : identifiant_student[:100]}
        return render_template('index.html', dic_prof=dic_prof, dic_eleve = dic_eleve)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
