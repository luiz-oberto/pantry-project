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

# Adiciona um item
@app.route('/api/items/add', methods=["GET","POST"])
def add_item():
    data = request.json
    if 'name' and 'quantity' in data:
        item = Item(name=data["name"], quantity=data['quantity'])
        db.session.add(item)
        db.session.commit()
        return jsonify({'message': "Item added sucessfully"})
    return jsonify({'message': "Invalid item data"}), 400

# Lista todos os itens na página inicial
@app.route('/')
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
    return render_template('items.html', item_list=item_list)

# Deleta um item
@app.route('/api/items/delete/<int:item_id>', methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted successfully"})
    return jsonify({"message": "Item not found"}), 404

# Atualizar item
@app.route('/api/items/update/<int:item_id>', methods=["PUT"])
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        jsonify({'message': "Item not found"}), 404
    
    data = request.json
    if 'quantity' in data:
        item.quantity = data['quantity']
    
    db.session.commit()
    return jsonify({'message': "Item updated successfully"})


# @app.route('/login')
# @app.route('/logout')

if __name__ == '__main__':
    app.run(debug=True)