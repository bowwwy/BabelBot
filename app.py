from __future__ import unicode_literals, print_function, division
from flask import Flask, render_template, request, redirect, url_for
from cryptography.fernet import Fernet
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
            return render_template('register.html')

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