from app.main.model import Supplier


def create_base_seed_supplier(db):

    supplier = Supplier(name="SUPPLIER 1", cpf="67179848050")
    db.session.add(supplier)

    supplier = Supplier(name="SUPPLIER 2", cnpj="13504619000185")
    db.session.add(supplier)

    supplier = Supplier(name="SUPPLIER 3", cpf="84928321006")
    db.session.add(supplier)

    db.session.commit()
