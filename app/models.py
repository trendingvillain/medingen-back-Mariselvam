from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Medicine(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    strength = db.Column(db.String(50))
    description = db.Column(db.Text)
    dosage = db.Column(db.Text)
    uses = db.Column(db.Text)
    side_effects = db.Column(db.Text)

    generics = db.relationship('GenericAlternative', backref='medicine', cascade="all, delete-orphan")
    comparisons = db.relationship('ComparisonProduct', backref='medicine', cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='medicine', cascade="all, delete-orphan")
    faqs = db.relationship('FAQ', backref='medicine', cascade="all, delete-orphan")


class GenericAlternative(db.Model):
    __tablename__ = 'generic_alternatives'
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    discount_percent = db.Column(db.Integer)
    image_url = db.Column(db.String(255))


class ComparisonProduct(db.Model):
    __tablename__ = 'comparison_products'
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100))
    generic_name = db.Column(db.String(100))
    average_price = db.Column(db.Numeric(10, 2))
    discounted_price = db.Column(db.Numeric(10, 2))
    chemical_formula = db.Column(db.String(50))
    rating = db.Column(db.Float)
    image_url = db.Column(db.String(255))

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    rating = db.Column(db.Float)
    comment = db.Column(db.Text)


class FAQ(db.Model):
    __tablename__ = 'faqs'
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)

