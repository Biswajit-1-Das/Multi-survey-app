from flask import Flask, render_template, request
import os
import csv

app = Flask(__name__)
SURVEYS = ['rpl', 'stt', 'dtet', 'vocational']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey/<survey_type>')
def show_form(survey_type):
    if survey_type in SURVEYS:
        return render_template(f"{survey_type}_form.html", survey_type=survey_type.upper())
    else:
        return "Invalid survey type", 404

@app.route('/submit/<survey_type>', methods=['POST'])
def submit_form(survey_type):
    if survey_type not in SURVEYS:
        return "Invalid submission", 404

    data = dict(request.form)
    csv_filename = f"survey_data/{survey_type}.csv"

    os.makedirs('survey_data', exist_ok=True)
    file_exists = os.path.isfile(csv_filename)

    with open(csv_filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())

        if not file_exists:
            writer.writeheader()  # Write column names
        writer.writerow(data)    # Write response

    return render_template("thank_you.html", survey=survey_type.upper())


