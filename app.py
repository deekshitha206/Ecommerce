# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

# ----------------- App Setup -----------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-this')

# Absolute path for DB inside instance folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(DB_DIR, 'ecommerce.db')

# Ensure the instance folder exists
os.makedirs(DB_DIR, exist_ok=True)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------- Models -----------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))   # path under static/ e.g., images/shirt1.jpg
    stock = db.Column(db.Integer, default=0)

# ----------------- DB Init & Seed -----------------
def init_db():
    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:
            sample = [
                Product(name='Red Shirt', price=299.0, description='Comfortable red shirt', image='images/shirt.png', stock=10),
                Product(name='Blue Jeans', price=899.0, description='Stylish blue jeans', image='images/jean.png', stock=5),
                Product(name='Sneakers', price=1499.0, description='Sporty sneakers', image='images/shoes1.png', stock=7),
                Product(name='Classic Watch', price=1999.0, description='Classic wrist watch', image='images/watch.jpg', stock=3),
            ]
            db.session.add_all(sample)
            db.session.commit()

# ----------------- Routes -----------------
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = str(request.form.get('product_id'))
    qty = int(request.form.get('quantity', 1))
    p = Product.query.get(product_id)
    if p and p.stock is not None and qty > p.stock:
        flash('Not enough stock available.')
        return redirect(request.referrer or url_for('index'))

    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + qty
    session['cart'] = cart
    flash('Added to cart')
    return redirect(request.referrer or url_for('index'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    products = []
    total = 0.0
    if cart:
        ids = [int(k) for k in cart.keys()]
        products = Product.query.filter(Product.id.in_(ids)).all()
        for p in products:
            total += p.price * cart.get(str(p.id), 0)
    return render_template('cart.html', cart=cart, products=products, total=total)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', {})
    for key, val in request.form.items():
        if key.startswith('qty_'):
            pid = key.split('_', 1)[1]
            try:
                q = int(val)
            except:
                q = 0
            if q <= 0:
                cart.pop(pid, None)
            else:
                cart[pid] = q
    session['cart'] = cart
    flash('Cart updated')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty.')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        if not name or not address:
            flash('Please fill required fields')
            return redirect(url_for('checkout'))

        # Clear cart after successful checkout
        session.pop('cart', None)
        return render_template('checkout_success.html', name=name)
    return render_template('checkout.html')

# ----------------- Run -----------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
