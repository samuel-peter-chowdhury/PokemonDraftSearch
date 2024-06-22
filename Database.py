from sqlalchemy import Column, ForeignKey, Integer, Double, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

db_url = 'sqlite:///pokemon_data.db'
engine = create_engine(db_url)
base = declarative_base()


class BaseModel(base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)


class PokemonModel(BaseModel):
    __tablename__ = 'pokemon'

    name = Column(String, unique=True, nullable=False)
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    special_attack = Column(Integer, nullable=False)
    special_defense = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    bst = Column(Integer, nullable=False)
    weight = Column(Double, nullable=False)
    height = Column(Double, nullable=False)
    point_value = Column(Integer, nullable=True)
    types = relationship('PokemonTypeModel', primaryjoin='PokemonModel.id==PokemonTypeModel.pokemon_id')
    abilities = relationship('PokemonAbilityModel', primaryjoin='PokemonModel.id==PokemonAbilityModel.pokemon_id')
    moves = relationship('PokemonMoveModel', primaryjoin='PokemonModel.id==PokemonMoveModel.pokemon_id')
    type_effective = relationship('PokemonTypeEffectiveModel', primaryjoin='PokemonModel.id==PokemonTypeEffectiveModel.pokemon_id')

    def __init__(self, pokemon):
        self.name = pokemon.name.lower()
        self.hp = pokemon.hp
        self.attack = pokemon.attack
        self.defense = pokemon.defense
        self.special_attack = pokemon.special_attack
        self.special_defense = pokemon.special_defense
        self.speed = pokemon.speed
        self.bst = pokemon.hp + pokemon.attack + pokemon.defense + pokemon.special_attack + pokemon.special_defense + pokemon.speed
        self.weight = pokemon.weight
        self.height = pokemon.height
        self.point_value = pokemon.point_value

    def __repr__(self):
        return vars(self)


class PokemonTypeModel(BaseModel):
    __tablename__ = 'pokemon_type'

    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    name = Column(String, nullable=False)

    def __init__(self, pokemon_id, name):
        self.pokemon_id = pokemon_id
        self.name = name.lower()

    def __repr__(self):
        return vars(self)


class PokemonAbilityModel(BaseModel):
    __tablename__ = 'pokemon_ability'

    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    name = Column(String, nullable=False)

    def __init__(self, pokemon_id, name):
        self.pokemon_id = pokemon_id
        self.name = name.lower()

    def __repr__(self):
        return vars(self)


class PokemonMoveModel(BaseModel):
    __tablename__ = 'pokemon_move'

    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)

    def __init__(self, pokemon_id, name, category):
        self.pokemon_id = pokemon_id
        self.name = name.lower()
        self.category = category.lower() if category is not None else None

    def __repr__(self):
        return vars(self)


class PokemonTypeEffectiveModel(BaseModel):
    __tablename__ = 'pokemon_type_effective'

    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    name = Column(String, nullable=False)
    multiplier = Column(Double, nullable=True)

    def __init__(self, pokemon_id, name, multiplier):
        self.pokemon_id = pokemon_id
        self.name = name.lower()
        self.multiplier = multiplier

    def __repr__(self):
        return vars(self)


base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)
session = session_maker()
