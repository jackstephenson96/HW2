## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError, validators
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.debug=True

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	album_name = StringField('Enter the name of an album: ', validators=[validators.Required()])
	likes = RadioField('How much do you like this album? (1 low, 3 high) ', choices=[(" 1", " 1"),(" 2", " 2"),(" 3"," 3")], validators=[validators.Required()])
	submit = SubmitField('Submit')

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
	return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
	return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artist_form():
	#what code goes here?
	return render_template('artistform.html')

@app.route('/artistinfo', methods = ['GET', 'POST'])
def artist_result():
	params = {}
	results_python = []
	params['term'] = request.args.get('artist')
	baseurl = 'https://itunes.apple.com/search'
	r = requests.get(baseurl, params=params, headers={"Accept":"application/json"})
	response_json = json.loads(r.text)['results']
	for thing in response_json:
		results_python.append(thing)
	return render_template('artist_info.html', objects=results_python)

@app.route('/specific/song/<artist_name>', methods = ['GET', 'POST'])
def specific(artist_name):
	params = {}
	results = []
	params['term'] = artist_name
	baseurl = 'https://itunes.apple.com/search'
	r = requests.get(baseurl, params=params, headers={"Accept":"application/json"})
	response_json = json.loads(r.text)['results']
	for thing in response_json:
		results.append(thing)
	return render_template('specific_artist.html', results=results)

@app.route('/artistlinks')
def artist_links():
	#what code goes here?
	return render_template('artist_links.html')

@app.route('/album_entry', methods = ['GET', 'POST'])
def album_entry():
	albumform = AlbumEntryForm()
	return render_template('album_entry.html', form=albumform)

@app.route('/album_result', methods = ['GET', 'POST'])
def album_result():
	albumform = AlbumEntryForm(request.form)
	results_python = {}
	results_python['album_name'] = albumform.album_name.data
	results_python['likes'] = albumform.likes.data
	return render_template('album_result.html', results=results_python)


if __name__ == '__main__':
	app.run(use_reloader=True,debug=True)
