from flask import Flask, render_template, request, redirect, session
import requests
import json
import plotly.express as px

app = Flask(__name__)

app.secret_key = 'clave_secreta_temporal'

global web_rol_id
global web_id_user
global web_user
global web_pass
global web_name_profile

@app.route('/', methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        if request.form.get('formu') == '1':

            web_user = request.form.get('usuario')
            web_pass = request.form.get('contrasena')

            url = 'http://127.0.0.1:3000/api/login/' + web_user + '/' + web_pass
            response = requests.get(url)

            data = response.json()
            web_rol_id = data['idRole']
            web_name_profile = data['name_profile']
            web_id_user = data['idUser']

            if response.status_code == 200:

                if list(data.keys())[0] == 'message_error':
                    return render_template('index.html')

                if web_rol_id == 1:
                    session['user'] = web_user
                    session['profile'] = web_name_profile
                    return redirect("/home_admin")
                elif web_rol_id == 2:
                    session['user'] = web_user
                    session['profile'] = web_name_profile
                    session['id_user'] = web_id_user
                    return redirect("/home_basic")
                elif web_rol_id == 3:
                    session['user'] = web_user
                    session['profile'] = web_name_profile
                    return redirect("/home_premium")
            else:
                print(f'Error: {response.status_code}')

        elif request.form.get('formu') == '2':

            new_user = request.form.get('usuario_new')
            new_name = request.form.get('nombre_new')
            new_lastname = request.form.get('apellido_new')
            new_birthday = request.form.get('cumple_new')
            new_pass = request.form.get('contrasena_new')

            url = 'http://127.0.0.1:3000/api/user'
            body = {"username": new_user, "password": new_pass, "name_profile": new_name, "lastname": new_lastname,
                    "birthdate": new_birthday}
            headers = {'Content-Type': 'application/json'}

            requests.post(url=url, data=json.dumps(body), headers=headers)

            return redirect("http://127.0.0.1:5000/home_basic")

@app.route('/home_admin', methods=["GET","POST"])
def home_admin():
    if request.method == "GET":
        user = session.get('profile')
        return render_template('home_admin.html', user=user)
    elif request.method == "POST":
        user = session.get('profile')
        web_id_user_home = request.form.get('id_user_home')
        web_id_tweet_home = request.form.get('id_tweet_home')
        web_name_tweet_home = request.form.get('name_tweet_home')

        url = 'http://127.0.0.1:3000/api/search'
        body = {"idUser": web_id_user_home, "identifier": web_id_tweet_home, "name_tweet": web_name_tweet_home}
        headers = {'Content-Type': 'application/json'}

        data = requests.post(url=url, data=json.dumps(body), headers=headers).json()

        if list(data.keys())[0] == 'message_error':
            return redirect('/home_admin')
        else:
            porc_neg = data["negative_percentage"]
            porc_neutro = data["neutral_percentage"]
            porc_pos = data["positive_percentage"]

            grafico_html = mostrar_grafico(porc_neg, porc_neutro, porc_pos)
            grafico_html1 = mostrar_grafico(porc_neg, porc_neutro, porc_pos)
            grafico_html2 = mostrar_grafico(porc_neg, porc_neutro, porc_pos)
            grafico_html3 = mostrar_grafico(porc_neg, porc_neutro, porc_pos)
            grafico_html4 = mostrar_grafico(porc_neg, porc_neutro, porc_pos)
            grafico_html5 = mostrar_grafico(porc_neg, porc_neutro, porc_pos)
            return render_template('home_admin.html', user=user,
                                   grafico_html=grafico_html,
                                   grafico_html1=grafico_html1,
                                   grafico_html2=grafico_html2,
                                   grafico_html3=grafico_html3,
                                   grafico_html4=grafico_html4,
                                   grafico_html5=grafico_html5,
                                   tweet_cont=data["tweet_text"],
                                   polaridad=data["polarity"],
                                   resumen=data["summary"],
                                   top_pos=data["top_3_positives"],
                                   top_neg=data["top_3_negatives"]
                                   )

@app.route('/home_basic', methods=["GET","POST"])
def home_basic():
    if request.method == "GET":
        user = session.get('profile')
        return render_template('home_basic.html', user=user)
    elif request.method == "POST":
        user = session.get('profile')
        web_id_user_home = session.get('id_user')
        web_id_tweet_home = request.form.get('id_tweet_home')
        web_name_tweet_home = request.form.get('name_tweet_home')

        url = 'http://127.0.0.1:3000/api/search'
        body = {"idUser": web_id_user_home, "identifier": web_id_tweet_home, "name_tweet": web_name_tweet_home}
        headers = {'Content-Type': 'application/json'}

        data = requests.post(url=url, data=json.dumps(body), headers=headers).json()

        if list(data.keys())[0] == 'message_error':
            return redirect('/home_basic')
        else:
            porc_neg = data["negative_percentage"]
            porc_neutro = data["neutral_percentage"]
            porc_pos = data["positive_percentage"]

            grafico_html = mostrar_grafico(porc_neg, porc_neutro, porc_pos)

            return render_template('home_basic.html', user=user, grafico_html=grafico_html,
                                   tweet_cont=data["tweet_text"],
                                   polaridad=data["polarity"],
                                   resumen=data["summary"],
                                   top_pos=data["top_3_positives"],
                                   top_neg=data["top_3_negatives"]
                                   )

@app.route('/home_premium', methods=["GET","POST"])
def home_premium():
    if request.method == "GET":
        user = session.get('profile')
        return render_template('home_premium.html', user=user)
    elif request.method == "POST":
        user = session.get('profile')
        web_id_user_home = session.get('id_user')
        web_id_tweet_home = request.form.get('id_tweet_home')
        web_name_tweet_home = request.form.get('name_tweet_home')

        url = 'http://127.0.0.1:3000/api/search'
        body = {"idUser": web_id_user_home, "identifier": web_id_tweet_home, "name_tweet": web_name_tweet_home}
        headers = {'Content-Type': 'application/json'}

        data = requests.post(url=url, data=json.dumps(body), headers=headers).json()

        if list(data.keys())[0] == 'message_error':
            return redirect('/home_premium')
        else:
            porc_neg = data["negative_percentage"]
            porc_neutro = data["neutral_percentage"]
            porc_pos = data["positive_percentage"]

            grafico_html = mostrar_grafico(porc_neg, porc_neutro, porc_pos)

            return render_template('home_premium.html', user=user, grafico_html=grafico_html,
                                   tweet_cont=data["tweet_text"],
                                   polaridad=data["polarity"],
                                   resumen=data["summary"],
                                   top_pos=data["top_3_positives"],
                                   top_neg=data["top_3_negatives"]
                                   )




def mostrar_grafico(neg,neu,pos):
    if neu >= 70:
        data = {'Polaridad':['Negativo','Positivo'],
                'Porcentaje':[neg,pos]}
    else:
        data = {'Polaridad': ['Negativo', 'Neutro', 'Positivo'],
                'Porcentaje': [neg, neu, pos]}

    fig = px.bar(data, x='Polaridad', y='Porcentaje')
    grafico_html = fig.to_html(full_html=False)
    return grafico_html




if __name__ == "__main__":
    app.run('0.0.0.0',port=5000,debug=True)