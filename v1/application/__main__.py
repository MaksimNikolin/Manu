from application import ocr
from application import translate
import easyocr
from flask import Flask, render_template, request

app: Flask = Flask(__name__)
reader = easyocr.Reader(["ru", "rs_cyrillic", "be", "bg", "uk", "mn"])

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/", methods=["POST"])
def upload_images():
    tahrirchi_token = app.config["TAHRIRCHI_API_TOKEN"]

    source_lang = request.form.get('source_lang')
    target_lang = request.form.get('target_lang')
    uploaded_files = request.files.getlist('file[]')
    
    images_list = []
    ocr_text = ""

    for file in uploaded_files:
        app_path = app.config["APP_PATH"]
        file_path = f"{app_path}/static/uploads/{file.filename}"
        file.save(file_path)

        images_list.append(file.filename)
        ocr_res = ocr.get_text_from_image(file_path, reader)
        ocr_text += ocr_res
    
    api_endpoint = app.config["TAHRIRCHI_API_BASE"]
    translated_text = translate.sayqalchi(api_endpoint, ocr_text, source_lang, target_lang, tahrirchi_token)

    if translated_text == None:
        translated_text = "Произошла ошибка перевода! Администрация сервиса была уведомлена"

    return render_template('results.html', images=images_list, ocr_text=ocr_text, 
                           translated_text=translated_text)