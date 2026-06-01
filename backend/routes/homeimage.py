from flask import Blueprint, jsonify, url_for

home_bp = Blueprint('home', __name__)

@home_bp.route('/api/home/welcome')
def get_welcome_image():
    img_url = url_for('static', filename='images/welcome-image.png', _external=True)
    return jsonify({'imageUrl': img_url})

@home_bp.route('/api/home/logo')
def get_logo():
    logo_url = url_for('static', filename='images/bons-burgers-logo-removebg.png', _external=True)
    return jsonify({'imageUrl': logo_url})

@home_bp.route('/api/home/login-icon')
def get_login_icon():
    icon_url = url_for('static', filename='images/user-icon.png', _external=True)
    return jsonify({'imageUrl': icon_url})

@home_bp.route('/api/home/login-page-image')
def get_login_page_image():
    from flask import url_for
    img_url = url_for('static', filename='images/Bons.webp', _external=True)
    return jsonify({'imageUrl': img_url})

@home_bp.route('/api/home/register-page-image')
def get_register_page_image():
    from flask import url_for
    img_url = url_for('static', filename='images/Bons.webp', _external=True)
    return jsonify({'imageUrl': img_url})