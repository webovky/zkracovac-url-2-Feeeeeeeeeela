from pony.orm import PrimaryKey, Required, Optional, Set, Database

# Import Flask-Pony instance from __init__.py module

# Get a reference to the base class of Pony entities
db = Database()
db.bind(provider="sqlite", filename="./database.sqlite", create_db=True)

class User(db.Entity):
    login = PrimaryKey(str)
    password = Required(str)
    email = Optional(str)
    addresses = Set("Shortener")


class Shortener(db.Entity):
    shortcut = PrimaryKey(str)
    url = Required(str)
    user = Optional(User)

db.generate_mapping(create_tables=True)
