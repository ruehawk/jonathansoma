# app.py
import sqlite3
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.db'
db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)


class School(db.Model):
    __tablename__ = 'schooldata'
    __table_args__ = {'extend_existing': True}
    LOC_CODE = db.Column(db.Text, primary_key=True)


# result = School.query.all()

@app.route("/")
def index():
    school_count = School.query.count()
    schools = School.query.all()
    return render_template("list.html", count=school_count, schools=schools, location="New York City")


@app.route('/schools/<slug>')
def detail(slug):
    school = School.query.filter_by(LOC_CODE=slug).first()
    return render_template("detail.html", school=school)

@app.route('/zip/<zipcode>')
def zip(zipcode):
    schools = School.query.filter_by(ZIP=zipcode).all()
    return render_template("list.html", schools=schools, count=len(schools), location=zipcode)

@app.route('/city/<cityname>')
def city(cityname):
    schools = School.query.filter_by(city=cityname.upper()).all()
    return render_template("list.html", schools=schools, count=len(schools), location=cityname)


@app.route("/about")
def about():
    print(School.query.count())
    return render_template("list.html")

@app.route('/city')
def city_list():
    # Get the unique city values from the database
    cities = School.query.with_entities(School.city).distinct().all()
    # ...more notes I'm hiding...
    # Convert to titlecase while we're pulling out of the weird list thing
    cities = [city[0].title() for city in cities]
    # Now that they're both "New York," we can now dedupe and sort
    cities = sorted(list(set(cities)))
    return render_template("cities.html", cities=cities)

@app.route('/zip')
def zip_list():
    # Get the unique city values from the database
    zips = School.query.with_entities(School.ZIP).distinct().all()
    # ...more notes I'm hiding...
    # Convert to titlecase while we're pulling out of the weird list thing
    zips = [ZIP[0] for ZIP in zips]
    # Now that they're both "New York," we can now dedupe and sort
    zips = sorted(list(set(zips)))
    return render_template("zips.html", zips=zips)


if __name__ == '__main__':
    app.run(debug=True)
