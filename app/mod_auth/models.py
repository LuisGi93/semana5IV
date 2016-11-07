# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from werkzeug import check_password_hash, generate_password_hash

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'auth_user'

    # User Name
    name    = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(192),  nullable=False)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    # New instance instantiation procedure
    def __init__(self, name, email, password, role, status):

        self.name     = name
        self.email    = email
        self.set_password(password)
        self.role    = role
        self.status = status


    def __repr__(self):
        return '<User %r>' % (self.name)

class Receta(Base):

    __tablename__ = 'receta'

    # User Name
    descripcion    = db.Column(db.String(400),  nullable=False)

    titulo    = db.Column(db.String(128),  nullable=False,
                                            unique=True)

    # Identification Data: email & password
    usuario    = db.Column(db.String(128),  nullable=False)
    # New instance instantiation procedure
    def __init__(self, titulo, email, descripcion):
        self.titulo = titulo
        self.usuario     = email
        self.descripcion    = descripcion


    def __repr__(self):
        return '<Titulo %r>' % (self.titulo)
