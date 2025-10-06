from flask import Blueprint, render_template,redirect,url_for
from models import db, Product, Location, ProductMovement
from forms import ProductForm, LocationForm, MovementForm

main = Blueprint("main", __name__,template_folder="templates")

@main.route("/")
def home():
    return render_template("base.html")

# Products
@main.route('/products', methods=['GET', 'POST'])
def products():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(product_id=form.product_id.data, name=form.name.data,description=form.description.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('main.products'))
    products = Product.query.all()
    return render_template('products.html', products=products, form=form)

# Locations
@main.route('/locations', methods=['GET', 'POST'])
def locations():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(location_id=form.location_id.data, name=form.name.data,description=form.description.data)
        db.session.add(location)
        db.session.commit()
        return redirect(url_for('main.locations'))
    locations = Location.query.all()
    return render_template('locations.html', locations=locations, form=form)

# Product Movements
@main.route('/movements', methods=['GET', 'POST'])
def movements():
    form = MovementForm()
    products = Product.query.all()
    locations = Location.query.all()
    form.product_id.choices = [(p.product_id, p.name) for p in products]
    location_choices = [('', '---')] + [(l.location_id, l.name) for l in locations]
    form.from_location.choices = location_choices
    form.to_location.choices = location_choices

    if form.validate_on_submit():
        movement = ProductMovement(
            product_id=form.product_id.data,
            from_location=form.from_location.data or None,
            to_location=form.to_location.data or None,
            qty=form.qty.data
        )
        db.session.add(movement)
        db.session.commit()
        return redirect(url_for('main.movements'))

    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=movements, form=form,products=products,locations=locations)

# Report
@main.route('/reports',methods=["GET","POST"])
def report():
    locations = Location.query.all()
    products = Product.query.all()
    balance = []
    for product in products:
        for location in locations:
            qty_in = db.session.query(db.func.sum(ProductMovement.qty)).filter_by(product_id=product.product_id, to_location=location.location_id).scalar() or 0
            qty_out = db.session.query(db.func.sum(ProductMovement.qty)).filter_by(product_id=product.product_id, from_location=location.location_id).scalar() or 0
            balance.append({
                'product': product.name,
                'location': location.name,
                'qty': qty_in - qty_out
            })
    return render_template('reports.html', report=balance)


@main.route('/products/edit/<string:product_id>',methods=["POST","GET"])
def edit(product_id):
    product=Product.query.filter_by(product_id=product_id).first_or_404()
    form=ProductForm(obj=product)

    if form.validate_on_submit():
        product.product_id=form.product_id.data
        product.name=form.name.data
        product.description=form.description.data
        db.session.commit()
        return redirect(url_for('main.products'))
    return render_template("edit_product.html",form=form,product=product)

@main.route('/products/delete/<string:product_id>',methods=["POST","GET"])
def delete(product_id):
    product=Product.query.filter_by(product_id=product_id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("main.products"))


@main.route('/edit_location/<string:location_id>',methods=["POST","GET"])
def edit_location(location_id):
    location=Location.query.filter_by(location_id=location_id).first_or_404()
    form=LocationForm(obj=location)

    if form.validate_on_submit():
        location.location_id=form.location_id.data
        location.name=form.name.data
        location.description=form.description.data
        db.session.commit()
        return redirect(url_for('main.locations'))
    return render_template("edit_location.html",form=form,location=location)

@main.route('/delete_location/<string:location_id>',methods=["POST","GET"])
def delete_location(location_id):
    location=Location.query.filter_by(location_id=location_id).first_or_404()
    db.session.delete(location)
    db.session.commit()
    return redirect(url_for("main.locations"))

@main.route('/movements/edit/<int:movement_id>', methods=["GET", "POST"])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    form = MovementForm(obj=movement)
    products = Product.query.all()
    locations = Location.query.all()
    form.product_id.choices = [(p.product_id, p.name) for p in products]
    location_choices = [('', '---')] + [(l.location_id, l.name) for l in locations]
    form.from_location.choices = location_choices
    form.to_location.choices = location_choices

    if form.validate_on_submit():
        movement.product_id = form.product_id.data
        movement.from_location = form.from_location.data or None
        movement.to_location = form.to_location.data or None
        movement.qty = form.qty.data
        db.session.commit()
        return redirect(url_for('main.movements'))

    return render_template('edit_movement.html', form=form)

@main.route('/movements/delete/<int:movement_id>', methods=["POST","GET"])
def delete_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    db.session.delete(movement)
    db.session.commit()
    return redirect(url_for('main.movements'))

