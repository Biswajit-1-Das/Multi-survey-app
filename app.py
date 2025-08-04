from flask import Flask, render_template

app = Flask(__name__)

# Route to index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to individual survey form pages
@app.route('/survey/<survey_type>')
def show_form(survey_type):
    valid_surveys = ['rpl', 'stt', 'dtet', 'vocational']
    if survey_type in valid_surveys:
        return render_template(f"{survey_type}_form.html", survey_type=survey_type.upper())
    else:
        return "Invalid survey type", 404

if __name__ == '__main__':
    app.run(debug=True)
