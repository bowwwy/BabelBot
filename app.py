from __future__ import unicode_literals, print_function, division
from flask import Flask, render_template, request, redirect, url_for
import FrenchToEngModel as En
import EngToFrenchModel as Fr

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/translate')
def translate():
    return render_template('translate.html')

@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/translator', methods=['GET', 'POST'])
def translator():
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