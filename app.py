"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from deep_translator import GoogleTranslator
from flask import Flask, render_template, request
import json
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

texts_path = 'static/texts/'

text_EN = json.load(open(texts_path + 'text.json', 'r', encoding="utf-8"))
text_PT_BR = json.load(open(texts_path + 'text_pt_br.json', 'r', encoding="utf-8"))
translator_text = json.load(open(texts_path + 'text_translator.json', 'r', encoding="utf-8"))
translator_text_PT_BR = json.load(open(texts_path + 'text_translator_pt_br.json', 'r', encoding="utf-8"))


@app.route('/')
@app.route('/pt-br')
def index():
    if request.path == '/':
        text = text_EN
    else:
        # Had to write the whole html without using a template, because jinja messes up the accented chars.
        text = text_PT_BR

    return render_template("index.html", headerType="ds-header", text=text)


@app.route('/fiapPython')
def fiapPython():
    return render_template("fiapPython.html")


@app.route('/translator', methods=['GET', 'POST'])
@app.route('/pt-br/translator', methods=['GET', 'POST'])
def renderTranslator():
    langList = GoogleTranslator().get_supported_languages()

    if request.method == 'POST':
        data = request.json
        return translate(data)

    if request.path == '/translator':
        text = translator_text
    else:
        text = translator_text_PT_BR

    return render_template("translator.html", langList=langList, headerType="ds-header-inner", text=text)


def translate(data):
    text = data['text']

    langList = GoogleTranslator().get_supported_languages(as_dict=True)

    selectedLangFrom = data['lang_from']
    lang_from_abreviation = langList.get(selectedLangFrom)

    selectedLangTo = data['lang_to']
    lang_to_abreviation = langList.get(selectedLangTo)
    translation = GoogleTranslator(
        source=lang_from_abreviation, target=lang_to_abreviation).translate(text)

    return translation


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
