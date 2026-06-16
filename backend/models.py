
import datetime

from .extension import db

class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



class User(BaseModel):
    username = db.Column(db.String(80), required=True, nullable=False)
    email = db.Column(db.String(120), unique=True,required=True, nullable=False)
    password = db.Column(db.String(128), required=True, nullable=False)

    requests = db.relationship('Request', back_populates='user', lazy=True)

class Request(BaseModel):
    data=db.Column(db.JSON())
    status = db.Column(db.Enum('Created', 'Approved', 'Rejected'), default='Created')
    type = db.Column(db.String(80), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='requests', lazy=True)


class Section(BaseModel):
    name = db.Column(db.String(80), required=True, nullable=False)
    products = db.relationship('Product', back_populates='section', lazy=True)



class Product(BaseModel):
    name = db.Column(db.String(80), required=True, nullable=False)
    price = db.Column(db.Numeric(10, 2), required=True, nullable=False)
    stock = db.Column(db.Numeric(10, 2))
    expiry = db.Column(db.DateTime, nullable=True)
    unit_of_sale = db.Column(db.Enum('unit', 'kg', 'litre'), nullable=True)
    mfd = db.Column(db.DateTime, nullable=True)

    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)

    section = db.relationship('Section', back_populates='products', lazy=True)


class SaleItem(BaseModel):
    quantity = db.Column(db.Numeric(10, 2), required=True, nullable=False)
    price_at_sale = db.Column(db.Numeric(10, 2), required=True, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', lazy=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    sale = db.relationship('Sale', back_populates='sale_items', lazy=True)


class Sale(BaseModel):
    
    total_amount = db.Column(db.Numeric(10, 2), required=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    sale_items = db.relationship('SaleItem', back_populates='sale', lazy=True)