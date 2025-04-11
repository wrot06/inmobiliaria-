from app import db  # Importamos db que ya ha sido inicializado

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ownerId = db.Column(db.Integer, nullable=False)

    # Para agregar fotos, si es necesario
    photos = db.relationship('Photo', backref='property', lazy=True)

    def __repr__(self):
        return f"<Property {self.id}, {self.type}, {self.city}>"

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)

    def __repr__(self):
        return f"<Photo {self.id}, {self.url}>"
