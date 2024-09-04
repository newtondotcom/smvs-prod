from libretranslatepy import LibreTranslateAPI
import platform

url = "http://89.168.33.166:5000/"
if platform.processor() == 'x86_64':
    lt = LibreTranslateAPI(url)
else:
    lt = LibreTranslateAPI(url)

def translate(text,from_code):
    to_code = "en"
    if from_code != "en":
        translatedText = lt.translate(text, from_code, to_code)
        return translatedText
    return text