from __future__ import unicode_literals, print_function, division
from flask import Flask, render_template, request, redirect, url_for,session
from cryptography.fernet import Fernet
from requests.exceptions import HTTPError
import re
import pyrebase as db
import FrenchToEngModel as En
import EngToFrenchModel as Fr
app = Flask(__name__)


config = {"apiKey": "AIzaSyDkiF2t9twh5qfFMziliS7b9nI6pX2c_ag",
          "authDomain": "babelbot-f8aaf.firebaseapp.com",
          "databaseURL": "https://babelbot-f8aaf-default-rtdb.asia-southeast1.firebasedatabase.app",
          "projectId": "babelbot-f8aaf",
          "storageBucket": "babelbot-f8aaf.appspot.com",
          "messagingSenderId": "761927119070",
          "appId": "1:761927119070:web:fb8be847d84d3d58f8524f",
          "measurementId": "G-ZEDQLD365N"
}

firebase = db.initialize_app(config)
auth = firebase.auth()

def check_user_logged_in():
    if 'user_id' in session:
        return True
    else:
        return False


key = Fernet.generate_key()
fernet = Fernet(key)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        
        

    return render_template('login.html')

@app.route('/translate')
def translate():
    return render_template('translate.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('uname')
        password = request.form.get('psw')
        c_password = request.form.get('cpsw')
        enc_pass = fernet.encrypt(password.encode(), c_password.encode())
        
        if not username or not email or not password or not c_password:
            error = "please fill in all the required fields."
            #return render_template('register.html', error = error) implement this when modal is added in html
            return render_template('register.html')
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_pattern, email):
            error = 'Invalid email format.'
            #
            #return render_template('register_screen.html', error=error) implement in front-end
            return render_template('register_screen.html')

        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"

        if not re.match(password_pattern, password):
            error = 'Password should contain at least 1 uppercase letter, 1 lowercase letter, 1 special character, and 1 number.'
            #return render_template('register_screen.html', error=error) implement front end
            return render_template('register_screen.html')
        try:
            user = auth.create_user_with_email_and_password(username, password)
            return render_template('login')
        except HTTPError as e:
            if e.response is not None and e.response.content:
                error = e.response.json()['error']['message']
            else:
                error = 'An error occurred during registration.'
            #return render_template('register.html', error=error) implement modal
            return render_template('register.html', error=error)

    return render_template('register.html')



@app.route('/translator', methods=['GET', 'POST'])
def translator():
    try:
        sentence = request.form['text']
        opt = request.form['options']
        if opt == 'French':
            sentence = Fr.normalizeStringFra(sentence)
            output_words, _ = Fr.evaluateToFra(Fr.encoderEng, Fr.decoderFra, sentence, Fr.input_lang_eng, Fr.output_lang_fra)
        elif opt == 'English':
            sentence = En.normalizeString(sentence)
            output_words, _ = En.evaluateEng(En.encoder, En.decoder, sentence, En.input_lang, En.output_lang)
        output_sentence = ' '.join(output_words)
        return render_template('translate.html', in_sentence = sentence, translated_text = output_sentence)
    except KeyError:
       # Edit this and make it as a pop up form 
       return render_template('translate.html')
    

if __name__ == '__main__':
    app.run(debug=True)
    
'''    if request.form['options'] == 'French':
        fra_sentence = request.form['text']
        fra_sentence = Fr.normalizeStringFra(fra_sentence)
        output_words, _ = Fr.evaluateToFra(Fr.encoderEng, Fr.decoderFra, fra_sentence, Fr.input_lang_eng, Fr.output_lang_fra)
        output_sentence = ' '.join(output_words)
    
    #fra_sentence = En.normalizeString(fra_sentence)
    #output_words, _ = En.evaluateEng(En.encoder, En.decoder, fra_sentence, En.input_lang, En.output_lang)
    #output_sentence = ' '.join(output_words)
    
    return render_template('translate.html', fran_sentence = fra_sentence, translated_text = output_sentence )'''