from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField,TextAreaField
from wtforms.validators import DataRequired,NumberRange

class ProductForm(FlaskForm):
    product_id = StringField('Product ID', validators=[DataRequired()])
    name = StringField('Product Name', validators=[DataRequired()])
    description=TextAreaField("Description")
    submit = SubmitField('Submit')

class LocationForm(FlaskForm):
    location_id = StringField('Location ID', validators=[DataRequired()])
    name = StringField('Location Name', validators=[DataRequired()])
    description=TextAreaField("Description")

    submit = SubmitField('Submit')

class MovementForm(FlaskForm):
    product_id = SelectField('Product', coerce=str)
    from_location = SelectField('From Location', coerce=str)
    to_location = SelectField('To Location', coerce=str)
    qty = IntegerField('Quantity', validators=[DataRequired(),NumberRange(min=1)])
    submit = SubmitField('Submit')
