from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, url_for
import os
import json

app = Flask(__name__)

def load_data():
    with open('data/projects.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('data/projects.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', projects=data['projects'], bonus=data['bonus'])

@app.route('/series')
def series():
    data = load_data()
    return render_template('series.html', series=data['series'], bonus=data['bonus_series'])

@app.route('/pdf/<filename>')
def pdf(filename):
    return send_from_directory('.', filename)

@app.route('/admin')
def admin():
    data = load_data()
    return render_template('admin.html', 
                         projects=data['projects'],
                         series=data['series'],
                         bonus=data['bonus'],
                         bonus_series=data['bonus_series'])

@app.route('/admin/add_project', methods=['POST'])
def add_project():
    data = load_data()
    new_project = {
        'title': request.form['title'],
        'filename': request.form['filename'],
        'desc': request.form['desc']
    }
    data['projects'].append(new_project)
    save_data(data)
    return redirect(url_for('admin'))

@app.route('/admin/add_series', methods=['POST'])
def add_series():
    data = load_data()
    new_series = {
        'day': request.form['day'],
        'project': request.form['project'],
        'filename': request.form['filename'],
        'summary': request.form['summary']
    }
    data['series'].append(new_series)
    save_data(data)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True) 