from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from flask_cors import CORS


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

app = Flask(__name__)
app.after_request(after_request)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:lab1008.@172.25.46.97/input_store'
# 设置数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'person'
    Id=db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Text = db.Column(db.String(500))

    def __repr__(self):
        return self

@app.route('/all', methods=['GET', 'POST'])
def all():
    person=Person.query.all()
    PR=[]
    for i in range(len(person)):
        pr={'name':person[i].Name,'text':person[i].Text}
        PR.append(pr)
    return jsonify(PR)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method=="GET":
        name=request.args.get('name')
        text=request.args.get('text')
    else:
        name=request.json.get('name')
        text=request.json.get('text')
    person=Person(Name=name,Text=text)
    db.session.add(person)
    db.session.commit()
    return jsonify([{'code':200}])

if __name__ == '__main__':
    app.run(debug=True)
    CORS(app, resources={r"/*": {"origins": "*"}})

