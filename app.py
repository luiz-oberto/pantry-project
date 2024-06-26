from flask import Flask, render_template, request, jsonify, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'chave_123@'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pantry.db'

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


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

# Rota para o formulário
@app.route('/add_item', methods=["GET"])
def add_item_form():
    return render_template('add_item.html')

# Adiciona um item
@app.route('/items/add', methods=["GET", "POST"])
def add_item():
   if request.method == "POST":
        name = request.form.get("name")
        quantity = request.form.get("quantity")

        if not name or not quantity or int(quantity) < 0:
            error = "Name or Quantity invalid."
            return render_template("add_item.html", error=error)
        
        item = Item(name=name, quantity=quantity)
        db.session.add(item)
        db.session.commit()
        return redirect('/')


# Deleta um item
@app.route('/items/delete/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')
    return redirect('/')

# Rota para o formulário de atualização
@app.route('/items/update/<int:item_id>', methods=["GET"])
def update_item_form(item_id):
    item = Item.query.get(item_id)
    if item:
        return render_template('update_item.html', item=item)
    return jsonify({"message": "Item not found"}), 404

# Atualizar item
@app.route('/items/update/<int:item_id>', methods=["POST"])
def update_item(item_id):
    item = Item.query.get(item_id)
    data_name = request.form.get('name')
    data_quantity = request.form.get('quantity')
    print(data_name)
    print(item.name)
    if item.name != data_name:
        item.name = data_name
    if item.quantity != data_quantity:
        item.quantity = data_quantity

    db.session.add(item)
    db.session.commit()
    return redirect('/')


# @app.route('/login')
# @app.route('/logout')

if __name__ == '__main__':
    app.run(debug=True)