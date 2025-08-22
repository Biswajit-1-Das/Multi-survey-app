from flask import Flask, render_template, request
import os
import csv

app = Flask(__name__)
SURVEYS = ['rpl', 'stt', 'dtet', 'vocational']

# Get connection string from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

db = SQLAlchemy(app)

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

    # If file exists, read the headers
    if file_exists:
        with open(csv_filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
    else:
        fieldnames = list(data.keys())

    # Ensure all fields are present (avoid ValueError)
    for key in data.keys():
        if key not in fieldnames:
            fieldnames.append(key)

    # Write the row
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    return render_template("thank_you.html", survey=survey_type.upper())


