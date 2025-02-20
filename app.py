from flask import Flask, render_template
from com.haneull.models.crime_controller import CrimeController

app = Flask(__name__)

@app.route('/')
def index():
    crimecontroller = CrimeController()
    crimecontroller.modeling('cctv_in_seoul.csv', 'crime_in_seoul.csv', 'pop_in_seoul.csv')
    return render_template('index.html')