from config import db

taxon_tag = db.Table(
    "taxon_tag",
    db.Column("taxon_id", db.Integer, db.ForeignKey("taxons.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=True)

    # Relationships
    # images = many to many with images table
    def __repr__(self):
        return "<Tag %r>" % self.name


IMAGES_ORIGINS = ["tag", "taxon"]


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.Enum(*IMAGES_ORIGINS), unique=False, nullable=False)
    url = db.Column(db.String(500), unique=True, nullable=False)

    def __repr__(self):
        return "<Image %r>" % self.id


# Life -> Domain -> Kingdom -> Phylum -> Class -> Order -> Family -> Genus -> Species -> Subspecies

TAXON_TYPES = [
    "life",
    "domain",
    "kingdom",
    "phylum",
    "class",
    "order",
    "family",
    "genus",
    "species",
    "subspecies",
]


class Taxon(db.Model):
    __tablename__ = "taxons"
    id = db.Column(db.Integer, primary_key=True)
    taxon = db.Column(db.Enum(*TAXON_TYPES), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    popular_name = db.Column(db.String(80), unique=False, nullable=True)
    description = db.Column(db.String(500), unique=False, nullable=True)
    origin = db.Column(db.Integer, unique=False, nullable=False)
    extinction = db.Column(db.Integer, unique=False, nullable=True)
    individuals_number = db.Column(db.Integer, unique=False, nullable=True)
    tags = db.relationship(
        "Tag", secondary=taxon_tag, backref=db.backref("taxons", lazy="dynamic")
    )

    # Relationships
    # supeior_taxon = many to one with same table
    # ancestors = many to many with same table
    # images = one to many with images table
    # tags = many to many with tags table
    # Opcional fields
    # fossils?
    # sites - actual - origin
    def __repr__(self):
        return "<Taxon - %r>" % self.name


"""
class Life(db.Model):
    __tablename__ = "life"
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
    __tablename__ = "domains"
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
    __tablename__ = "kingdoms"
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
    __tablename__ = "phylums"
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

class Class(db.Model):
    __tablename__ = "classes"
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
    #phylum = one to many with life table
    # Opcional fields
    #fossils?
    #sites - actual - origin
    def __repr__(self):
        return "<Class %r>" % self.name

class Order(db.Model):
    __tablename__ = "orders"
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
    #class = one to many with life table
    # Opcional fields
    #fossils?
    #sites - actual - origin
    def __repr__(self):
        return "<Order %r>" % self.name

class Family(db.Model):
    __tablename__ = "families"
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
    #order = one to many with life table
    # Opcional fields
    #fossils?
    #sites - actual - origin
    def __repr__(self):
        return "<Family %r>" % self.name

class Genus(db.Model):
    __tablename__ = "genera"
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
    #family = one to many with life table
    # Opcional fields
    #fossils?
    #sites - actual - origin
    def __repr__(self):
        return "<Genus %r>" % self.name

class Species(db.Model):
    __tablename__ = "species"
    id = db.Column(db.Integer, primary_key=True)
    specific_epithet = db.Column(db.String(80), unique=False, nullable=False)
    popular_name = db.Column(db.String(80), unique=False, nullable=True)
    description = db.Column(db.String(500), unique=False, nullable=True)
    origin = db.Column(db.Integer, unique=False, nullable=False)
    extinction = db.Column(db.Integer, unique=False, nullable=True)
    individuals_number = db.Column(db.Integer, unique=False, nullable=True)
    # Relationships
    #ancestors = many to many with same table
    #images = one to many with images table
    #tags = many to many with tags table
    #genus = one to many with life table
    # Opcional fields
    #fossils?
    #sites - actual - origin
    def __repr__(self):
        return "<Species %r>" % "genus name " + self.specific_epithet

class Subspecies(db.Model):
    __tablename__ = "subspecies"
    id = db.Column(db.Integer, primary_key=True)
    subspecific_epithet = db.Column(db.String(80), unique=False, nullable=False)
    popular_name = db.Column(db.String(80), unique=False, nullable=True)
    description = db.Column(db.String(500), unique=False, nullable=True)
    origin = db.Column(db.Integer, unique=False, nullable=False)
    extinction = db.Column(db.Integer, unique=False, nullable=True)
    individuals_number = db.Column(db.Integer, unique=False, nullable=True)
    # Relationships
    #ancestors = many to many with same table
    #images = one to many with images table
    #tags = many to many with tags table
    #species = one to many with life table
    # Opcional fields
    #fossils?
    #sites - actual - origin
    def __repr__(self):
        return "<Subspecies %r>" % "genus name " + "species name " + self.subspecific_epithet
"""
