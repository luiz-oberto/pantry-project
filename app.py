from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config['SECRET_KEY'] = 'chave_123@'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pantry.db'

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)



@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=', tudo bem?'):
    return render_template('base.html', person=name)

@app.route('/api/item/add', methods=["POST"])
def add_item():
    data = request.json
    if 'name' and 'quantity' in data:
        item = Item(name=data["name"], quantity=data['quantity'])
        db.session.add(item)
        db.session.commit()
        return jsonify({'message': "Item added sucessfully"})
    return jsonify({'message': "Invalid item data"})

@app.route('/api/items')
def get_items():
    items = Item.query.all()
    item_list = []
    for item in items:
        item_data = {
            "id": item.id,
            "name": item.name,
            "quantity": item.quantity
        }
        item_list.append(item_data)
    return jsonify(item_list)

# @app.route('/api/item/delete', methods=["DELETE"])

# @app.route('/api/item/update' methods=["PUT"])

# @app.route('/login')
# @app.route('/logout')

@app.route('/')
def hello_word():
    return 'Hello Word!'

if __name__ == '__main__':
    app.run(debug=True)