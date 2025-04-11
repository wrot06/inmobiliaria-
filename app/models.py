from app import db  # Importamos db que ya ha sido inicializado

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ownerId = db.Column(db.Integer, nullable=False)

    # Relación con las fotos
    photos = db.relationship('Photo', backref='property', lazy=True)

    def __repr__(self):
        return f"<Property {self.id}, {self.type}, {self.city}>"


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)

    def __repr__(self):
        return f"<Photo {self.id}, {self.url}>"


# Modelo de User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20))

    # Relación con Visit (una visita puede estar asociada con un único usuario como inquilino)
    visits = db.relationship('Visit', back_populates='tenant', lazy=True)  # Usamos back_populates aquí


# Modelo de Visit
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proposed_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pendiente')

    # Relación con User (visitante)
    tenant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tenant = db.relationship('User', back_populates='visits')  # Correspondiente back_populates

    # Relación con Property (propiedad)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    property = db.relationship('Property', backref='visits')
