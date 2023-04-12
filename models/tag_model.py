from ..app import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=True)

    def __repr__(self):
        return "<Tag %r>" % self.name

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    def __repr__(self):
        return "<Image %r>" % self.id

class Life(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    popular_name = db.Column(db.String(80), unique=False, nullable=True)
    description = db.Column(db.String(500), unique=False, nullable=True)
    origin = db.Column(db.Integer, unique=False, nullable=False)
    extinction = db.Column(db.Integer, unique=False, nullable=True)
    individuals_number = db.Column(db.Integer, unique=False, nullable=True)
    # Relationships
    #ancestors = many to many with same table
    #images = one to many with images table
    #tags = many to many with tags table
    # Opcional fields
    #fossils?
    #sites - actual - origin
    def __repr__(self):
        return "<Life %r>" % self.name

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    popular_name = db.Column(db.String(80), unique=False, nullable=True)
    description = db.Column(db.String(500), unique=False, nullable=True)
    origin = db.Column(db.Integer, unique=False, nullable=False)
    extinction = db.Column(db.Integer, unique=False, nullable=True)
    individuals_number = db.Column(db.Integer, unique=False, nullable=True)
    # Relationships
    #ancestors = many to many with same table
    #images = one to many with images table
    #tags = many to many with tags table
    #life = one to many with life table
    # Opcional fields
    #fossils?
    #sites - actual - origin
    def __repr__(self):
        return "<Domain %r>" % self.name

class Kingdom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    popular_name = db.Column(db.String(80), unique=False, nullable=True)
    description = db.Column(db.String(500), unique=False, nullable=True)
    origin = db.Column(db.Integer, unique=False, nullable=False)
    extinction = db.Column(db.Integer, unique=False, nullable=True)
    individuals_number = db.Column(db.Integer, unique=False, nullable=True)
    # Relationships
    #ancestors = many to many with same table
    #images = one to many with images table
    #tags = many to many with tags table
    #domain = one to many with life table
    # Opcional fields
    #fossils?
    #sites - actual - origin
    def __repr__(self):
        return "<Kingdom %r>" % self.name

class Phylum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    popular_name = db.Column(db.String(80), unique=False, nullable=True)
    description = db.Column(db.String(500), unique=False, nullable=True)
    origin = db.Column(db.Integer, unique=False, nullable=False)
    extinction = db.Column(db.Integer, unique=False, nullable=True)
    individuals_number = db.Column(db.Integer, unique=False, nullable=True)
    # Relationships
    #ancestors = many to many with same table
    #images = one to many with images table
    #tags = many to many with tags table
    #kingdom = one to many with life table
    # Opcional fields
    #fossils?
    #sites - actual - origin
    def __repr__(self):
        return "<Phylum %r>" % self.name


    