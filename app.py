from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json
import sys
from flask import Flask, render_template, url_for, request, session, redirect
from config import app, mysql, cursor, conn
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm


def queryprodutos():
    query = '''SELECT * FROM tb_produto'''
    cursor.execute(query)
    res = cursor.fetchall()
    produtos = []
    content = {}
    for result in res:
        content = {'ID': result[0], 'id_tipo': result[1],'nome': result[2], 'descricao': result[3],'qtd_estoque': result[4], 'qtd_minima': result[5],'valor_compra': result[6], 'valor_venda': result[7], 'ativo': result[8]}
        produtos.append(content)
        content={}
    return produtos

@app.route('/')
@app.route('/index')
def index():
    produtos = queryprodutos()
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html', username=session['email'], produtos=produtos)
    # User is not loggedin redirect to login page
    return render_template('index.html',produtos=produtos)


@app.route('/login')
def login():
    if 'loggedin' in session:
        # User is loggedin show them the home page       
        return render_template('index.html')
    # User is not loggedin redirect to login page
    return render_template('login.html')


@app.route('/logar', methods=['GET','POST'])
def logar():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        #query=f'''SELECT * FROM tb_cliente WHERE email = {email} AND password {password}'''
        cursor.execute('SELECT * FROM tb_cliente WHERE email = %s AND senha = %s', (email, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            print(session)
            print(account)
            session['id'] = account[0]
            session['email'] = account[6]
            # Redirect to home page
            return redirect(url_for('index'))
            
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            
            
    
    return render_template('index.html', msg=msg)


@app.route('/cadastro')
def cadastro():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('cadastro.html', username=session['email'])
    return render_template('cadastro.html')
    


@app.route('/cadastrar',methods=['GET','POST'])
def cadastrar():
    msg = ''
    # Output message if something goes wrong...
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        nome= request.form['nomecompleto']
        cpf= request.form['cpf']
        sexo= request.form['sexo']
        birthdate= request.form['birthdate']
        number= request.form['number']
        email = request.form['email']
        password = request.form['password']
        
        # Check if account exists using MySQL
        
        cursor.execute('SELECT * FROM tb_cliente WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO tb_cliente VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)', (nome, cpf, sexo, birthdate, number, email, password,))            
            conn.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('index'))


@app.route('/sobre')
def sobre():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('sobre.html', username=session['email'])
    return render_template('sobre.html')

@app.route('/carrinho')
def carrinho():
    return redirect(url_for('index'))

@app.route('/atendimento')
def atendimento():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('atendimento.html', username=session['email'])
    return render_template("atendimento.html")

@app.route('/finalizar')
def finalizar():
    return render_template("finalizar.html")

@app.route('/endereco')
def endereco():
    return render_template("endereco.html")

@app.route('/pagamento')
def pagamento():
    return render_template("pagamento.html")

if __name__ == '__main__':  
    app.run(debug=True)


@app.route('/teste')
def teste():
    query = '''SELECT * FROM tb_cliente ORDER BY nome'''
    a=cursor.execute(query)
    print(a)
    return render_template('cadastro.html')


sys.stdout = open('declare.js','w')

jsonobj = json.dumps(queryprodutos())
print("var jsonstr = '{}'".format(jsonobj))

