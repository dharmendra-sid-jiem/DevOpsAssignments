from flask import Flask, request, render_template, redirect, url_for, flash
import requests
from dotenv import load_dotenv
import os 
load_dotenv()
BACKEND_URL = os.getenv('BACKEND_URL')
 
app= Flask(__name__)
app.secret_key = 'a_very_secure_and_unique_secret_key'


@app.route('/')
def home():
     return render_template('index.html')

@app.route('/submit', methods = ['POST'])
def submit():
    try:
        form_data =dict(request.form)
        name = request.form['name']
        email = request.form['email']

        if not name or not email:
            flash("Name and Email are required fields.")
            return redirect(url_for('home'))

        requests.post(BACKEND_URL+'/submit', json=form_data)
        return redirect(url_for('success'))
    except Exception as e:
        flash(f"Error submitting data: {e}")
        return redirect(url_for('home'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/view')
def view():
    data = requests.get(BACKEND_URL+'/view')          
    
    return data.json()

@app.route('/api')
def api():
    data = requests.get(BACKEND_URL+'/api')          
    
    return data.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)