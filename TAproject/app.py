from flask import Flask
from flask import Flask, request, redirect, url_for, render_template
from flask import session as login_session
import requests
import json

from databases import *


app = Flask(__name__)

app.secret_key = "MY_SUPER_SECRET_KEY"
app.config['SECRET_KEY'] = 'you-will-never-guess-my-super-secret'

# del_all_users()
# del_all_photos()


@app.route('/')
def start():
	return render_template("start.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	photos=get_all_photos()
	if request.method == 'GET':
		return render_template("login.html")
	else:
		username = request.form['username']
		password = request.form['password']
		user = get_user_by_username(username)
		if (not(user == None)) and user.password ==password:
			login_session['name'] = username
			return render_template('home.html', user = user, photos=photos)
		else:
			return render_template("login.html")


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html')
	else:
		username = request.form['username']
		password = request.form['password']
		add_user(username, password)
		return render_template('login.html')


@app.route('/home')
def home():
	photos = get_all_photos()
	links = []
	for i in photos:
		links.append(i.link)
	user = get_user_by_username(login_session['name'])
	return render_template("home.html", links = links, user = user, photos = photos)

@app.route('/search', methods=['GET', 'POST'])
def search():
	headers = {'Authorization': 'Key e585291d7622418a9235d110f9c20f1c'}
	api_url = "https://api.clarifai.com/v2/models/aaa03c23b3724a16a56b629203edc62c/outputs"
	results=[]
	if request.method == 'GET':
		return render_template("search.html", results = results)
	else:
		if request.form['search'] == "":
			return render_template("search.html", results = results)

		user = get_user_by_username(login_session['name'])
		photos = get_all_photos()
		tags = []
		for p in photos:
			data ={"inputs": [{"data": {"image": {"url": p.link}}}]}
			response = requests.post(api_url, headers=headers, data=json.dumps(data))
			print(response.content)
			tags.append(json.loads(response.content)["outputs"][0])
		
		for t in tags:
			for i in t["data"]["concepts"]:
				if i["name"] == request.form['search']:
					results.append(photos[tags.index(t)])
		return render_template("search.html", user = user, results = results)

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
	user = get_user_by_username(login_session['name'])
	if request.method == 'GET':
		return render_template('upload.html', user = user)
	else:
		link = request.form['photo']
		add_photo(link, user.username)
		user_photos = get_photos_by_user(user)
		return render_template('profile.html', user=user, photos = user_photos)

@app.route('/profile')
def profile():
	user = get_user_by_username(login_session['name'])
	user_photos = get_photos_by_user(user)

	return render_template('profile.html', user = user, photos = user_photos)


if __name__ == '__main__':
	app.run(debug=True)
