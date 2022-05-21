from flask import Flask, make_response, jsonify, request
import dataset

app = Flask(__name__)

db = dataset.connect('sqlite:///sqlite.db')


table = db['news']


def fetch_db(new_id):
    return table.find_one(new_id = new_id)

def fetch_db_all():
    news = []
    for new in table:
        news.append(new)
    return news

@app.route('/api/db_populate')
def db_populate():
    table.insert({
        'new_id':'1',
        'name': "Facebok",
        'description': "Web app",
        'date':"01.05.2022",
        'author': "sandro iashvili"
})
    table.insert({
        'new_id':'2',
        'name': "Nvidea",
        'description': "Desktop app",
        'date':"01.05.2020",
        'author': "sandro iashvili"
    })
    return make_response(jsonify(fetch_db_all()),200)



@app.route('/api/news', methods = ['GET', 'POST'])
def api_news():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()),200)
    elif request.method == 'POST':
        content = request.json
        new_id = content['new_id']
        table.insert(content)
        return make_response(jsonify(fetch_db(new_id)),201)
    
@app.route('/api/news/<new_id>', methods = ['GET', 'PUT', 'DELETE'])
def api_news_details(new_id):
    if request.method == 'GET':
        new_obj = fetch_db(new_id)
        if new_obj:
            return make_response(jsonify(new_obj),200)
        else:
            return make_response(jsonify(new_obj),404)
        
    elif request.method == 'PUT':
        content = request.json
        table.update(content, ['new_id'])
        new_obj = fetch_db(new_id)
        return make_response(jsonify(new_obj),200)
    
    elif request.method == 'DELETE':
        table.delete(id = new_id)
        return make_response(jsonify({}, 204))
        
if __name__ == '__main__':
    app.run(debug=True)