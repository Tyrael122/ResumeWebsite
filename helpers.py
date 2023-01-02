from deep_translator import GoogleTranslator

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

def fetch_lang_list():
    return GoogleTranslator().get_supported_languages()
