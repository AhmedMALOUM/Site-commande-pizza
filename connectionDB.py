from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_pour_la_session'

# Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pizzainnobdb"
)
cursor = conn.cursor()

# Route pour afficher les pizzas
@app.route("/")
def index():
    cursor.execute("SELECT NROPIZZ, DESIGNPIZZ, TARIFPIZZ, image1_chemin FROM pizza")
    pizzas = cursor.fetchall()
    return render_template("index.html", pizzas=pizzas)

# Route pour ajouter une pizza au panier
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    pizza_id = request.form.get("pizza_id")
    pizza_name = request.form.get("pizza_name")
    pizza_price = float(request.form.get("pizza_price"))

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({'id': pizza_id, 'name': pizza_name, 'price': pizza_price})
    session.modified = True

    return redirect(url_for("index"))

# Route pour afficher le panier
@app.route("/cart")
def cart():
    panier = session.get('cart', [])
    total = sum(item['price'] for item in panier)
    return render_template("cart.html", panier=panier, total=total)

# Route pour valider la commande
@app.route("/place_order", methods=["POST"])
def place_order():
    panier = session.get('cart', [])
    if not panier:
        return redirect(url_for("cart"))

    # Enregistrement des commandes dans la base de données (optionnel)
    # TODO: Ajouter logique pour enregistrer la commande dans la base

    session.pop('cart', None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
