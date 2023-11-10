from flask import Flask, render_template, request, redirect, session
import requests
import json
import plotly.express as px
import matplotlib.pyplot as plt

app = Flask(__name__)

app.secret_key = 'clave_secreta_temporal'

global web_rol_id
global web_id_user
global web_user
global web_pass
global web_name_profile


@app.route('/', methods=["GET", "POST"])
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

            if response.status_code == 200:

                if list(data.keys())[0] == 'message_error':
                    return render_template('index.html')

                else:

                    web_rol_id = data['idRole']
                    web_name_profile = data['name_profile']
                    web_id_user = data['idUser']

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


@app.route('/home_admin', methods=["GET", "POST"])
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

            grafico_html = grafico_porcentaje(porc_pos, "% Positivo", "green")
            grafico_html1 = grafico_porcentaje(porc_neg, "% Negativo", "red")
            grafico_html2 = grafico_porcentaje(porc_neutro, "% Neutro", "royalblue")
            grafico_html3 = grafico_pastel(porc_pos, porc_neutro, porc_neg)
            grafico_html4 = mostrar_grafico(porc_neg, porc_neutro, porc_pos)
            grafico_html5 = mostrar_grafico(porc_neg, porc_neutro, porc_pos)
            grafico_html6 = mostrar_grafico(porc_neg, porc_neutro, porc_pos)
            return render_template('home_admin.html', user=user,
                                   grafico_html=grafico_html,
                                   grafico_html1=grafico_html1,
                                   grafico_html2=grafico_html2,
                                   grafico_html3=grafico_html3,
                                   grafico_html4=grafico_html4,
                                   grafico_html5=grafico_html5,
                                   grafico_html6=grafico_html6,
                                   tweet_cont=data["tweet_text"],
                                   polaridad=card_polaridad2(data["polarity"]),
                                   resumen=car_resumen(data["summary"]),
                                   top_pos=comentarios_positivos(data["top_3_positives"]),
                                   top_neg=comentarios_negativos(data["top_3_negatives"])
                                   )


@app.route('/home_basic', methods=["GET", "POST"])
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


@app.route('/home_premium', methods=["GET", "POST"])
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


def mostrar_grafico(neg, neu, pos):
    if neu >= 70:
        data = {'Polaridad': ['Negativo', 'Positivo'],
                'Porcentaje': [neg, pos]}
    else:
        data = {'Polaridad': ['Negativo', 'Neutro', 'Positivo'],
                'Porcentaje': [neg, neu, pos]}

    fig = px.bar(data, x='Polaridad', y='Porcentaje')
    grafico_html = fig.to_html(full_html=False)
    return grafico_html


def grafico_porcentaje(indice, title, color):
    # Valor porcentual
    porcentaje = round(indice, 2)

    # Crear un gráfico de medio aro
    fig = px.pie(names=['', ''], values=[porcentaje, 100 - porcentaje],
                 hole=0.7, color_discrete_sequence=['white', color],
                 title=title)

    # Configurar el diseño del gráfico
    fig.update_layout(
        showlegend=False,
        annotations=[
            dict(text=f'{porcentaje}%', x=0.5, y=0.5, font_size=20, showarrow=False)
        ],
        hovermode=False,
        title_x=0.5, title_y=0.1,
        title_font_size=20
    )

    fig.update_traces(textinfo='none', marker_line=dict(color='black', width=1.5))

    grafico_html = fig.to_html(full_html=False)
    return grafico_html


def grafico_pastel(pos, neu, neg):
    labels = ['% Positivo', '% Neutro', '% Negativo']
    values = [pos, neu, neg]

    fig = px.pie(names=labels, values=values, hole=0.7, color_discrete_sequence=['green', "royalblue", "red"],
                 title="Porcentaje de polaridad")

    fig.update_layout(
        hovermode=False,
        title_x=0.5, title_y=0.1,
        title_font_size=20,
        legend_x=0.375, legend_y=0.5,
        legend_itemclick=False,
        legend_itemdoubleclick=False
    )

    grafico_html = fig.to_html(full_html=False)
    return grafico_html


def card_polaridad(polarity):
    if polarity == "positive" or polarity == "positivo":
        polaridad = "Positivo"
    elif polarity == "negative" or polarity == "negativo":
        polaridad = "Negativo"
    elif polarity == "neutral" or polarity == "neutro":
        polaridad = "Neutro"

    return """<div class="card" style="height: 45%; margin: 10px">
                <div class="card-body">
                    <h5 class="card-title">Polaridad</h5>
                    <p class="card-text">""" + polaridad + """</p>
                    
                    <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#collapseWidthExample" aria-expanded="false" aria-controls="collapseWidthExample">
                        Información
                    </button>
                    
                    <span style="min-height: 120px; height: 100%">
                      <div class="collapse collapse-horizontal" id="collapseWidthExample">
                        <div class="card card-body" style="width: 300px;">
                          El sistema considera un porcentaje como 'neutro' solo cuando es menor al 70%; en otros casos, evalúa los porcentajes positivos y negativos.
                        </div>
                      </div>
                    </span>
                </div>
            </div>"""


def card_polaridad2(polarity):
    if polarity == "positive" or polarity == "positivo":
        polaridad = "Positivo"
    elif polarity == "negative" or polarity == "negativo":
        polaridad = "Negativo"
    elif polarity == "neutral" or polarity == "neutro":
        polaridad = "Neutro"

    return """<div class="card" style="margin: 10px; text-align: center;">
                <div class="card-body">
                    <h5 class="card-title">Polaridad</h5>
                    <p class="card-text">""" + polaridad + """</p>

                    <p class="d-inline-flex gap-1">
                      <a class="btn btn-primary" data-bs-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false" aria-controls="collapseExample">
                        Información
                      </a>
                    </p>
                    <div class="collapse" id="collapseExample">
                      <div class="card card-body">
                        El sistema considera un porcentaje como 'neutro' solo cuando es menor al 70%; en otros casos, evalúa los porcentajes positivos y negativos.
                      </div>
                    </div>
                </div>
            </div>"""


def car_resumen(resumen):
    return """<div class="card" style="margin: 10px; text-align: center;">
                    <div class="card-body">
                        <h5 class="card-title">Resumen de los comentarios</h5>
                        <textarea style="width: 100%; height: 150px; resize: none; border: 0px" readonly>""" + resumen + """</textarea>
                    </div>
                </div>"""


def comentarios_positivos(list_comentarios):
    return """<div class="col-4">
                    <h5 class="card-title" style="margin-bottom: 10px; margin-top: 20px">TOP 3 - Comentarios
                        positivos</h5>
                    <div id="list-example" class="list-group" style="margin-bottom: 20px; margin-top: 20px">
                        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" role="button"
                           aria-expanded="false">Comentarios</a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#list-item-1">Comentario 1</a></li>
                            <li><a class="dropdown-item" href="#list-item-2">Comentario 2</a></li>
                            <li><a class="dropdown-item" href="#list-item-3">Comentario 3</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col-8">
                    <div data-bs-spy="scroll" data-bs-target="#list-example" data-bs-smooth-scroll="True"
                         class="scrollspy-example" tabindex="0"
                         style="height: 150px; overflow-y: scroll; margin-bottom: 20px; margin-top: 20px">
                        <h4 id="list-item-1">Comentario 1</h4>
                        <p>"""+list_comentarios[0]+"""</p>
                        <h4 id="list-item-2">Comentario 2</h4>
                        <p>"""+list_comentarios[1]+"""</p>
                        <h4 id="list-item-3">Comentario 3</h4>
                        <p>"""+list_comentarios[2]+"""</p>
                    </div>
                </div>"""


def comentarios_negativos(list_comentarios):
    return """<div class="col-4">
                    <h5 class="card-title" style="margin-bottom: 10px; margin-top: 30px">TOP 3 - Comentarios negativos</h5>
                    <div id="list-example" class="list-group" style="margin-bottom: 20px; margin-top: 30px">
                        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" role="button"
                           aria-expanded="false">Comentarios</a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#list-item-4">Comentario 1</a></li>
                            <li><a class="dropdown-item" href="#list-item-5">Comentario 2</a></li>
                            <li><a class="dropdown-item" href="#list-item-6">Comentario 3</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col-8">
                    <div data-bs-spy="scroll" data-bs-target="#list-example" data-bs-smooth-scroll="True"
                         class="scrollspy-example" tabindex="0"
                         style="height: 150px; overflow-y: scroll; margin-bottom: 20px; margin-top: 30px">
                        <h4 id="list-item-4">Comentario 1</h4>
                        <p>"""+list_comentarios[0]+"""</p>
                        <h4 id="list-item-5">Comentario 2</h4>
                        <p>"""+list_comentarios[1]+"""</p>
                        <h4 id="list-item-6">Comentario 3</h4>
                        <p>"""+list_comentarios[2]+"""</p>
                    </div>
                </div>"""


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)
