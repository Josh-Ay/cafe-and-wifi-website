from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
from wtforms import StringField, SubmitField, RadioField


class AddNewCafe(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    map_url = StringField(label="Map URL", validators=[DataRequired(), URL()])
    img_url = StringField(label="Image URL", validators=[DataRequired(), URL()])
    location = StringField(label="Location", validators=[DataRequired()])
    seats = StringField(label="Number of Seats per setting available (e.g 10, 20)", validators=[DataRequired()])
    coffee_price = StringField(label="Coffee Price in £ (e.g 5, 10, 15)")
    has_sockets = RadioField(label="Sockets", choices=[("1", "Sockets")], default="0")
    has_toilet = RadioField(label="Toilet", choices=[("1", "Toilets")], default="0")
    has_wifi = RadioField(label="WIFI", choices=[("1", "WiFi")], default="")
    can_take_calls = RadioField(label="Calls", choices=[("1", "Calls")], default="0")
    submit_btn = SubmitField(label="Add", render_kw={"class": "submit-btn"})
