from flask import Blueprint, render_template, send_from_directory, session

crud_bp = Blueprint('crud', __name__, template_folder='../templates')


@crud_bp.route('/menu')
def menu():
    return render_template('crud/menu.html')

#url homepage
homepage_bp = Blueprint('homepage', __name__, template_folder='templates')

@homepage_bp.route('/homepage')
def homepage():
    return render_template('user/homepage.html')

#url good
good_bp = Blueprint('good', __name__, template_folder='templates')

@good_bp.route('/good')
def good():
    return render_template('user/god.html')

#url pdf
send_bp = Blueprint('terminos_y_condiciones', __name__, template_folder='templates')
@send_bp.route('/terminos_y_condiciones')
def send_pdf():
    print("Enviando PDF...")
    return send_from_directory('static/Document', 'terminos_y_condiciones_gesde.pdf')

@send_bp.route('/politica_privacidad')
def sendp_pdf():
    print("Enviando PDF...")
    return send_from_directory('static/Document', 'politica_privacidad_gesde_3_paginas.pdf')

reporturl_bp = Blueprint('reporturl', __name__, template_folder='templates')
@reporturl_bp.route('/reporturl')
def reporturl():
    return render_template('crud/report.html')

