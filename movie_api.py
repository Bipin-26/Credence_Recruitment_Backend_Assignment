from flask import Flask, render_template, jsonify, request, url_for, redirect
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['JSON_SORT_KEYS']=False
app.config['MONGO_DBNAME'] = 'Project'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Project'
mongo = PyMongo(app)
collection = mongo.db.moviestore

@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/index')
def index():
    docs = collection.find()
    return jsonify({"MOvieStore":docs})
    

@app.route('/insert', methods=['POST','GET'])
def insert():
    if request.method == 'POST': 
        name = request.form["movie_name"]
        img = request.form['movie_img']
        summary = request.form  ['movie_summary']
        insert_query = collection.insert_one({'name':name,"img":img,"summary":summary})
        return redirect(url_for('index'))
    return render_template('insert.html')


@app.route('/update', methods=['POST','GET'])
def update():
    docs = collection.find({})
    if request.method == 'POST':
        old_movie_name = request.form.get('old_movie')
        new_movie_name = request.form.get('new_movie')
        old_img_link = request.form.get('old_img')
        new_img_link = request.form.get('new_img')
        old_summary = request.form.get('old_summary')
        new_summary = request.form.get('new_summary')
        old_update_name_query = {'name':old_movie_name}
        old_update_img_query = {'img':old_img_link}
        old_update_summary_query = {'summary':old_summary}
        new_update_name_query = {'$set':{'name':new_movie_name} }
        new_update_img_query = {'$set':{'img':new_img_link}}
        new_update_summary_query = {'$set':{'summary':new_summary}}
        update_name = collection.update_one(old_update_name_query,new_update_name_query)
        update_img = collection.update_one(old_update_img_query,new_update_img_query)
        update_summary = collection.update_one(old_update_summary_query,new_update_summary_query)
        return redirect('index')
    return render_template('update.html', data = docs)


@app.route('/remove', methods=['POST'])
def remove():
    name = request.form.get('movie_name')
    delete_query = collection.delete_one({'name':name})
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)