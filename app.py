from flask import Flask, render_template, request, jsonify, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pantry.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


############################## --ROTAS AUTENTICAÇÃO-- ###################################
# autenticação - carrega o usuário que não deslogou na última sessão
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# rota de login de usuário
@app.route('/login', methods=["GET"])
def rota_para_login():
    return render_template('login.html')

# fazer login
@app.route('/api/login', methods=["GET","POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if user and password == user.password:
            login_user(user)
            return redirect('/')
    
    return 'informação inválida'

# rota de logout
@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect('/')

# @app.route('/register')

############################ --END AUTENTICAÇÃO-- ################################

############################ --ROTAS INTERAÇÃO COM ITENS-- #####################
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


if __name__ == '__main__':
    app.run(debug=True)