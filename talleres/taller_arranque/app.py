import os
import re
from collections import Counter

from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath("./uploads/")
ALLOWED_EXTENSIONS = set(["py","sgm","txt",""])

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():

    return render_template('index.html')


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if not "file" in request.files:
            return "No file part in the form."
        f = request.files["file"]
        if f.filename == "":
            return "No file selected."
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            print(filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            print(f)
            return redirect(url_for("get_file", filename=filename))
        return "File not allowed."
    return render_template('upload.html')

@app.route('/reto1')
def reto1():
    filename = "reut2-000.sgm"
    pre_processed_text = get_pre_processed_text(filename)

    return render_template('reto1.html', count= len(pre_processed_text))

@app.route('/reto2', methods=["GET"])
def reto2():
    filename = request.args.get('filename')
    pre_processed_text = get_pre_processed_text(filename)
    frequency_list = get_frequency_list(pre_processed_text)

    return render_template('reto2.html', frequency= frequency_list)

@app.route('/reto3')
def reto3():
    filename = "reut2-000.sgm"
    number = request.args.get('number')

    pre_processed_text = get_pre_processed_text(filename)
    frequency_list = get_frequency_list(pre_processed_text)
    counter = Counter(frequency_list)

    return render_template('reto3.html', frequency= counter.most_common(int(number)))

@app.route('/reto4')
def reto4():
    filename = request.args.get('filename')
    number = request.args.get('number')

    pre_processed_text = get_pre_processed_text(filename)
    frequency_list = get_frequency_list(pre_processed_text)
    counter = Counter(frequency_list)

    return render_template('reto3.html', frequency=counter.most_common(int(number)))

@app.route('/reto5-1')
def reto5_1():
    filename1 = "reut2-000.sgm"
    filename2 = "reut2-001.sgm"
    pre_processed_text1 = get_pre_processed_text(filename1)
    pre_processed_text2 = get_pre_processed_text(filename2)

    return render_template('reto5_1.html', count1=len(pre_processed_text1), count2 = len(pre_processed_text2))

@app.route('/reto5-2')
def reto5_2():
    filename1 = request.args.get('filename1')
    filename2 = request.args.get('filename2')
    pre_processed_text1 = get_pre_processed_text(filename1)
    pre_processed_text2 = get_pre_processed_text(filename2)
    frequency_list1 = get_frequency_list(pre_processed_text1)
    frequency_list2 = get_frequency_list(pre_processed_text2)

    return render_template('reto5_2.html', frequency_list1=frequency_list1, frequency_list2=frequency_list2)

@app.route('/reto5-3')
def reto5_3():
    filename1 = "reut2-000.sgm"
    filename2 = "reut2-001.sgm"
    number1 = request.args.get('number1')
    number2 = request.args.get('number2')

    pre_processed_text1 = get_pre_processed_text(filename1)
    frequency_list1 = get_frequency_list(pre_processed_text1)
    counter1 = Counter(frequency_list1)

    pre_processed_text2 = get_pre_processed_text(filename2)
    frequency_list2 = get_frequency_list(pre_processed_text2)

    return render_template('reto5_3.html', frequency_list1=counter1.most_common(int(number1)), frequency_list2=counter1.most_common(int(number2)))

@app.route('/reto5-4')
def reto5_4():
    filename1 = request.args.get('filename1')
    filename2 = request.args.get('filename2')
    number1 = request.args.get('number1')
    number2 = request.args.get('number2')

    pre_processed_text1 = get_pre_processed_text(filename1)
    frequency_list1 = get_frequency_list(pre_processed_text1)
    counter1 = Counter(frequency_list1)

    pre_processed_text2 = get_pre_processed_text(filename2)
    frequency_list2 = get_frequency_list(pre_processed_text2)

    return render_template('reto5_3.html', frequency_list1=counter1.most_common(int(number1)), frequency_list2=counter1.most_common(int(number2)))


@app.route("/uploads/<filename>")
def get_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

def get_pre_processed_text(filename):
    document_text = open(filename, 'r')
    text_string = document_text.read().lower()
    match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)
    return [re.sub(r'\d+', 'num', match_pattern) for match_pattern in match_pattern]

def get_frequency_list(text):
    frequency = {}
    for word in text:
        count = frequency.get(word, 0)
        frequency[word] = count + 1

    return frequency

if __name__ == "__main__":
    app.run(debug=True)
