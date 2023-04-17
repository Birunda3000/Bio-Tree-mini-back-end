from config import Config, db
from services import save_new_tag, save_new_taxon

tag_seeder_list = [
    {
        "name": "tag1",
        "description": "tag1 description",
    },
    {
        "name": "tag2",
        "description": "tag2 description",
    },
    {
        "name": "tag3",
        "description": "tag3 description",
    },
    {
        "name": "tag4",
        "description": "tag4 description",
    },
    {
        "name": "tag5",
        "description": "tag5 description",
    },
    {
        "name": "tag56",
        "description": "tag6 description",
    },
    {
        "name": "Pesquisa",
        "description": "tag7 description",
    },
]

taxon_seeder_list = [
    {
        "taxon_class": "life",
        "name": "Celular life",
        "popular_name": "Celular life",
        "description": "Celular life description",
        "origin": 3,
        "extinction": None,
        "individuals_number": 10000,
        "superior_taxon": None,
        "tags": [1, 2, 3]
    },
    {
        "taxon_class": "domain",
        "name": "Eukaryota",
        "popular_name": "Eukaryota",
        "description": "Eukaryota description",
        "origin": 1,
        "extinction": None,
        "individuals_number": 1000,
        "superior_taxon": 1,
        "tags": [1, 2, 3]
    },
    {
        "taxon_class": "kingdom",
        "name": "Animalia",
        "popular_name": "Animal",
        "description": "Animal description",
        "origin": 1,
        "extinction": None,
        "individuals_number": 100,
        "superior_taxon": 2,
        "tags": [1, 2]
    },
]


def seed_db_tags():
    for tag in tag_seeder_list:
        save_new_tag(tag)

def seed_db_taxons():
    for taxon in taxon_seeder_list:
        save_new_taxon(taxon)


def seed_db():
    seed_db_tags()
    seed_db_taxons()
