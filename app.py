# Imports
import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy import func, DateTime
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.debug = True

# Configs
# Our database configurations will go here

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/testApi'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Modules
# SQLAlchemy will be initiated here
# Modules

db = SQLAlchemy(app)
migrate = Migrate(app, db)
make_searchable(db.metadata)


class Agurate_Crop(db.Model):
    __tablename__ = 'agurate_crops'

    id = db.Column(db.Integer, primary_key=True)
    crop_code = db.Column(db.String(80), unique=True, index=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.Text, default='no image')
    created_at = db.Column(db.DateTime,server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())
    document_token = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('document_token'))

    crop_variety = db.relationship('Agurate_Crop_Variety', backref='agurate_crops')

    def __init__(self, crop_code, name, image, created_at , updated_at, document_token):
        self.crop_code = crop_code
        self.name = name
        self.image=image
        self.created_at=created_at
        self.updated_at=updated_at
        self.document_token=document_token

    def __repr__(self):
        return '' % self.id


class Agurate_Crop_Variety(db.Model):
    __tablename__ = 'agurate_crop_varieties'

    id = db.Column(db.Integer, primary_key=True)
    crop_code = db.Column(db.String(256), db.ForeignKey('agurate_crops.crop_code'), index=True,
                          nullable=False)
    crop_variety_code = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    document_token = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('document_token'))
    crop_variety_property = db.relationship('Agurate_Crop_Variety_Property', backref='agurate_crop_varieties')

    # crop_id = db.Column(db.Integer, db.ForeignKey('agurate_crops.id'))

    def __repr__(self):
        return '' % self.crop_code % self.crop_variety_code % self.name


class Agurate_Crop_Variety_Property(db.Model):
    __tablename__ = 'agurate_crop_variety_properties'
    id = db.Column(db.Integer, primary_key=True)
    crop_variety_code = db.Column(db.String(256), db.ForeignKey('agurate_crop_varieties.crop_variety_code'),nullable=False)

    entity = db.Column(db.String(256), nullable=False)
    attribute = db.Column(db.String(100))
    value = db.Column(db.String(100))
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    document_token = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('document_token'))

class Agurate_Farmer(db.Model):
    __tablename__ = 'agurate_farmers'
    id = db.Column(db.Integer, primary_key=True)
    farmer_code = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False, index=True)
    location = db.Column(db.String(100), index=True, nullable=False)
    address = db.Column(db.String, index=True)
    seedling_seller = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    email = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    document_token = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('document_token'))

    def __repr__(self):
        return '' % self.farm_code % self.name



class Agurate_Farm(db.Model):
    __tablename__ = 'agurate_farms'
    id = db.Column(db.Integer, primary_key=True)
    farm_code = db.Column(db.String(256), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False, index=True)
    main_farmer_code = db.Column(db.String(100), db.ForeignKey('agurate_farmers.farmer_code'), nullable=False)
    address = db.Column(db.String(100), nullable=False, index=True)
    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)
    size = db.Column(db.Numeric)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    document_token = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('document_token'))

    def __repr__(self):
        return '' % self.farm_code % self.main_farmer_code % self.name


class Agurate_Farm_Property(db.Model):
    __tablename__ = 'agurate_farms_properties'
    id = db.Column(db.Integer, primary_key=True)
    farm_code = db.Column(db.String(256), db.ForeignKey('agurate_farms.farm_code'), nullable=False)
    property_code= db.Column(db.String(100), nullable=False, index=True)
    property_value = db.Column(db.String, nullable=False)
    group = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    document_token = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('document_token'))
    def __repr__(self):
        return '' %self.farm_code % self.property_code

class Agurate_Farm_Crop(db.Model):
    __tablename__ = 'agurate_farms_crops'
    id = db.Column(db.Integer, primary_key=True)
    farm_code = db.Column(db.String(100),db.ForeignKey('agurate_farms.farm_code'),nullable=False, index=True)
    crop_variety_code = db.Column(db.String(100), db.ForeignKey('agurate_crop_varieties.crop_variety_code'), nullable=True,
                                  index=True)
    quantity= db.Column(db.Numeric, nullable=False)
    unit_price = db.Column(db.Numeric)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    document_token = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('document_token'))
    def __repr__(self):
        return '' %self.farm_code % self.crop_variety_code

class Agurate_Farmer_Yields(db.Model):
    __tablename__ = 'agruate_farmer_yields'

    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.String(20), unique=True, nullable=False)
    farmer = db.Column(db.String(100),db.ForeignKey('agurate_farmers.farmer_code'), nullable=False)
    crop = db.Column(db.String(100), nullable=False)
    expected_date = db.Column(db.Date)
    actual_date = db.Column(db.Date)
    expected_yield = db.Column(db.Numeric)
    actual_yield = db.Column(db.Numeric)
    metrics = db.Column(db.String(10))
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    document_token = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('document_token'))

class Agurate_Farmers_Farm(db.Model):
    __tablename__ = 'agurate_farmers_farm'

    id = db.Column(db.Integer, primary_key= True)
    farmer_code = db.Column(db.String, db.ForeignKey('agurate_farmers.farmer_code'), nullable=False)
    farm_code = db.Column(db.String, db.ForeignKey('agurate_farms.farm_code'), index=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    document_token = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('document_token'))

class Agurate_Farmer_Log(db.Model):
    __tablename__= 'agurate_farmer_logs'
    id= db.Column(db.Integer, primary_key=True)
    farmer= db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    note = db.Column(db.Text)
    status = db.Column(db.String(100), nullable=False)
    employee = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    document_token = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('document_token'))

class Agurate_Seedling_Price(db.Model):
    __tablename__ = 'agurate_seedling_price'

    id = db.Column(db.Integer, primary_key=True)
    farmer_code = db.Column(db.String(100), nullable=False)
    crop_variety_code = db.Column(db.String(100), db.ForeignKey('agurate_crop_varieties.crop_variety_code'), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    document_token = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('document_token'))
'''
class People(db.Model):
    __tablename__='people'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime,server_onupdate=db.func.now())
'''

@app.route('/crop', methods=['POST', 'GET' ])
def AddOrGetCrops():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            newcrop = Agurate_Crop(crop_code=data['crop_code'], name=data['name'], image=data['image'])
            db.session.add(newcrop)
            db.session.commit()
            return {"message": f"crop {newcrop.name} successfully added."}
        else:
            return {"error ": "data not in json format"}
    elif request.method == 'GET':
        crops = Agurate_Crop.query.all()
        results = [
            {
                'crop_code': crop.crop_code,
                'name': crop.name,
                'image': crop.image
            } for crop in crops]

        return {'count': len(results), 'crops': results}


@app.route('/crops/<crop_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_crops(crop_id):
    crop = Agurate_Crop.query.get_or_404(crop_id)

    if request.method == 'GET':
        response = {
            "crop_code": crop.crop_code,
            "name": crop.name,
            "image": crop.image
        }
        return {"message": "success", "crop": response}

    elif request.method == 'PUT':
        data = request.get_json()
        crop.crop_code = data['crop_code']
        crop.name = data['name']
        crop.image = data['image']
        db.session.add(crop)
        db.session.commit()
        return {"message": f"crop {crop.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(crop)
        db.session.commit()
        return {"message": f"Crop {crop.name} successfully deleted."}


@app.route('/crop_variety', methods=['POST', 'GET'])
def AddOrGetCropVariety():
    if request.method =='POST':
        if request.is_json:
            data = request.get_json()
            newvariety = Agurate_Crop_Variety(crop_code=data['crop_code'], crop_variety_code=data['crop_variety_code'],
                                              name=data['name'])
            db.session.add(newvariety)
            db.session.commit()
            return {"message": f"crop variety {newvariety.crop_variety_code } successfully added."}
        else:
            return {"error": "data not in json format"}
    elif request.method=='GET':
        crop_varieties = Agurate_Crop_Variety.query.all()
        results = [
            {
                'crop_code':crop_variety.crop_code,
                'crop_variety_code': crop_variety.crop_variety_code,
                'name':crop_variety.name

            }for crop_variety in crop_varieties
        ]
        return {'count': len(results), 'crop_varieties': results}

@app.route('/crop_variety/<crop_variety_id>', methods=['GET', 'PUT','DELETE'])
def handle_crop_variety(crop_variety_id):
    crop_variety = Agurate_Crop_Variety.query.get_or_404(crop_variety_id)

    if request.method == 'GET':
        response ={
            'crop_code': crop_variety.crop_code,
            'crop_variety_code': crop_variety.crop_variety_code,
            'name': crop_variety.name
        }
        return {"message": "success", "crop variety ": response}

    elif request.method == 'PUT':
        data= request.get_json()
        crop_variety.crop_code=data['crop_code']
        crop_variety.crop_variety_code=data['crop_variety_code']
        crop_variety.name=data['name']
        db.session.add(crop_variety)
        db.session.commit()
        return {"message ": f"Crop variety {crop_variety.crop_variety_code} updated successfully."}


    elif request.method == 'DELETE':

        db.session.delete(crop_variety)

        db.session.commit()

        return {"message": f"Crop variety {crop_variety.crop_variety_code} successfully deleted."}



@app.route('/crop_variety_property', methods=['POST', 'GET', ])
def AddOrGetCropVarietyProperty():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            newcropvarietyprop = Agurate_Crop_Variety_Property(crop_variety_code=data['crop_variety_code'], entity=data['entity'],
                                                               attribute=data['attribute'], value=data['value'], note =data['note'])
            db.session.add(newcropvarietyprop)
            db.session.commit()
            return {"message": f"crop property {newcropvarietyprop.entity} successfully added."}
        else:
            return {"error ": "data not in json format"}
    elif request.method == 'GET':
        crop_properties = Agurate_Crop_Variety_Property.query.all()
        results = [
            {
                'crop_variety_code': crop_property.crop_variety_code,
                'entity': crop_property.entity,
                'attribute': crop_property.attribute,
                'value': crop_property.value
            } for crop_property in crop_properties]

        return {'count': len(results), 'crops properties': results}


@app.route('/crop_property/<prop_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_crop_prop(prop_id):
    crop_prop = Agurate_Crop_Variety_Property.query.get_or_404(prop_id)

    if request.method == 'GET':
        response = {
            "crop_variety_code": crop_prop.crop_variety_code,
            "entity": crop_prop.entity,
            "attribute": crop_prop.attribute,
            "value": crop_prop.value,
            "note": crop_prop.note
        }
        return {"message": "success", "crop properties": response}

    elif request.method == 'PUT':
        data = request.get_json()
        crop_prop.crop_variety_code_code = data['crop_variety_code']
        crop_prop.entity = data['entity']
        crop_prop.attribute = data['attribute']
        crop_prop.value = data['value']
        crop_prop.note = data['note']
        db.session.add(crop_prop)
        db.session.commit()
        return {"message": f"crop property {crop_prop.entity} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(crop_prop)
        db.session.commit()
        return {"message": f"Crop Property {crop_prop.entity} successfully deleted."}

if __name__ == '__main__':
    app.run()

