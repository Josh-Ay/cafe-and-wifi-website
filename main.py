from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import AddNewCafe
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "652as%Gd$5mre0er287d"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Bootstrap(app)
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return dictionary


@app.get("/")
def home():
    all_cafes = Cafe.query.all()

    return render_template("index.html", cafes=all_cafes)


@app.route("/add", methods=["GET", "POST"])
def add_new_cafe():
    form = AddNewCafe()

    if form.validate_on_submit():
        def convert_value_to_boolean(value):
            if int(value) == 1:
                return True
            else:
                return False

        new_cafe = Cafe(name=form.name.data, map_url=form.map_url.data, img_url=form.img_url.data,
                        location=form.location.data, coffee_price=form.coffee_price.data, seats=form.seats.data,
                        has_toilet=convert_value_to_boolean(form.has_toilet.data),
                        has_wifi=convert_value_to_boolean(form.has_wifi.data),
                        has_sockets=convert_value_to_boolean(form.has_sockets.data),
                        can_take_calls=convert_value_to_boolean(form.can_take_calls.data)
                        )

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html", form=form)


@app.get("/cafes/cafe/<int:cafe_id>")
def show_cafe(cafe_id):
    cafe_to_show = None
    all_cafes = [cafe.to_dict() for cafe in Cafe.query.all()]
    for cafe in all_cafes:
        if cafe["id"] == cafe_id:
            cafe_to_show = cafe

    return render_template("cafe.html", cafe=cafe_to_show, cafe_name=cafe_to_show["name"])


@app.get("/cafes/cafe")
def get_specific_cafes():
    query_param = request.args.get("q")
    all_cafes = [cafe.to_dict() for cafe in Cafe.query.all()]
    results = []

    for cafe in all_cafes:
        if cafe[f"{query_param}"] == 1:
            results.append(cafe)

    return render_template("index.html", results=results, query=query_param.split("_")[-1].upper())


if __name__ == "__main__":
    app.run(debug=True)
