from flask import Flask, render_template, request, redirect
import requests
import json


app = Flask(__name__)

@app.route('/', methods=["GET"])
def index_():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def login_():

    if request.form.get('formu') == '1':

        web_user = request.form.get('usuario')
        web_pass = request.form.get('contrasena')

        url = 'http://127.0.0.1:3000/api/login/' + web_user + '/' + web_pass
        response = requests.get(url)

        data = response.json()

        if response.status_code == 200:

            if list(data.keys())[0] == 'message_error':
                return render_template('index.html')
            rol_id = data['idRole']
            if rol_id == 1:
                return redirect("http://127.0.0.1:5000/home_admin")
            elif rol_id == 2:
                return redirect("http://127.0.0.1:5000/home_basic")
            elif rol_id == 3:
                return redirect("http://127.0.0.1:5000/home_premium")
        else:
            print(f'Error: {response.status_code}')

    elif request.form.get('formu') == '2':

        new_user = request.form.get('usuario_new')
        new_pass = request.form.get('contrasena_new')

        url = 'http://127.0.0.1:3000/api/user'
        data = {"username": new_user, "password": new_pass}
        headers = {'Content-Type': 'application/json'}

        requests.post(url=url,data=json.dumps(data), headers=headers)

        return redirect("http://127.0.0.1:5000/home_basic")

@app.route('/home_admin', methods=["GET"])
def home_admin():
    return render_template('home_admin.html')

@app.route('/home_basic', methods=["GET"])
def home_basic():
    return render_template('home_basic.html')

@app.route('/home_premium', methods=["GET"])
def home_premium():
    return render_template('home_premium.html')



if __name__ == "__main__":
    app.run('0.0.0.0',port=5000,debug=True)