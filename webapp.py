import sqlalchemy
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float, desc
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify
from flask import render_template

engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
base = automap_base()
base.prepare(engine,reflect=True)

base.classes.keys()

OTU = base.classes.otu
SAMPLES = base.classes.samples
METADATA = base.classes.samples_metadata

app = Flask(__name__) 

session = Session(engine)

inspector = inspect(engine)

sample_columns = inspector.get_columns('samples')
sample_columns

for column in sample_columns:
    print(column['name'])

sample_names = SAMPLES.__table__.columns.keys()
sample_names[1:]

@app.route("/names")
def names():
    sample_names = SAMPLES.__table__.columns.keys()
    names = sample_names[1:]
    return(jsonify(names))

@app.route("/otu")
def otu():
    otu_descriptions = session.query(OTU.lowest_taxonomic_unit_found).all()
    otu_ids = [i for i, in otu_descriptions]
    return(jsonify(otu_ids))

@app.route('/metadata/<sample>')
def metadata_sample(sample):
    sample_obj = session.query(METADATA).filter_by(SAMPLEID=sample)[0]

    return_obj = {
        "AGE": sample_obj.AGE,
        "BBTYPE": sample_obj.BBTYPE,
        "ETHNICITY": sample_obj.ETHNICITY,
        "GENDER": sample_obj.GENDER,
        "LOCATION": sample_obj.LOCATION,
        "SAMPLEID": sample_obj.SAMPLEID
    }
    return jsonify(return_obj)

@app.route('/wfreq/<sample>')
def wfreq_sample(sample):
    sample_obj = session.query(METADATA).filter_by(SAMPLEID=sample)[0]

    return jsonify(sample_obj.WFREQ)

@app.route('/samples/<sample>')
def sample(sample):
    data = session.query(SAMPLES, "otu_id", "BB_" + sample).order_by(desc('otu_id')).all()
    otu_ids = []
    sample_values = []
    for i in data:
        otu_ids.append(i.otu_id)
        sample_values.append(i[2])
    dict = {
        "otu_ids": otu_ids,
        "sample_values": sample_values
    }

    list = [dict]
    return jsonify(list)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True)