from Database import session, PokemonModel, PokemonTypeModel, PokemonAbilityModel, PokemonMoveModel, PokemonTypeEffectiveModel
from sqlalchemy import select, and_


class NumberSearchField:
    def __init__(self, minimum=0, maximum=9999):
        self.minimum = minimum
        self.maximum = maximum


class SearchObject:
    def __init__(self):
        self.hp = NumberSearchField()
        self.attack = NumberSearchField()
        self.defense = NumberSearchField()
        self.special_attack = NumberSearchField()
        self.special_defense = NumberSearchField()
        self.speed = NumberSearchField()
        self.bst = NumberSearchField()
        self.point_value = NumberSearchField(0, 20)
        self.type_1 = None
        self.type_2 = None
        self.ability = None
        self.move = None
        self.special_move_category = None
        self.type_effective_resist_1 = None
        self.type_effective_resist_2 = None
        self.type_effective_immune = None


def execute_search(search_object: SearchObject):
    stmt = (select(PokemonModel).where(
        and_(
            and_(
                PokemonModel.hp >= search_object.hp.minimum,
                PokemonModel.hp <= search_object.hp.maximum
            ),
            and_(
                PokemonModel.attack >= search_object.attack.minimum,
                PokemonModel.attack <= search_object.attack.maximum
            ),
            and_(
                PokemonModel.defense >= search_object.defense.minimum,
                PokemonModel.defense <= search_object.defense.maximum
            ),
            and_(
                PokemonModel.special_attack >= search_object.special_attack.minimum,
                PokemonModel.special_attack <= search_object.special_attack.maximum
            ),
            and_(
                PokemonModel.special_defense >= search_object.special_defense.minimum,
                PokemonModel.special_defense <= search_object.special_defense.maximum
            ),
            and_(
                PokemonModel.speed >= search_object.speed.minimum,
                PokemonModel.speed <= search_object.speed.maximum
            ),
            and_(
                PokemonModel.bst >= search_object.bst.minimum,
                PokemonModel.bst <= search_object.bst.maximum
            ),
            and_(
                PokemonModel.point_value >= search_object.point_value.minimum,
                PokemonModel.point_value <= search_object.point_value.maximum
            ),
            (PokemonModel.types.any(
                PokemonTypeModel.name == search_object.type_1.lower()
            ) if search_object.type_1 is not None else PokemonModel.types.any()),
            (PokemonModel.types.any(
                PokemonTypeModel.name == search_object.type_2.lower()
            ) if search_object.type_2 is not None else PokemonModel.types.any()),
            (PokemonModel.abilities.any(
                PokemonAbilityModel.name == search_object.ability.lower()
            ) if search_object.ability is not None else PokemonModel.abilities.any()),
            (PokemonModel.moves.any(
                PokemonMoveModel.name == search_object.move.lower()
            ) if search_object.move is not None else PokemonModel.moves.any()),
            (PokemonModel.moves.any(
                PokemonMoveModel.category == search_object.special_move_category.lower()
            ) if search_object.special_move_category is not None else PokemonModel.moves.any()),
            (PokemonModel.type_effective.any(
                and_(
                    PokemonTypeEffectiveModel.name == search_object.type_effective_resist_1.lower(),
                    PokemonTypeEffectiveModel.multiplier < 1.0
                )
            ) if search_object.type_effective_resist_1 is not None else PokemonModel.type_effective.any()),
            (PokemonModel.type_effective.any(
                and_(
                    PokemonTypeEffectiveModel.name == search_object.type_effective_resist_2.lower(),
                    PokemonTypeEffectiveModel.multiplier < 1.0
                )
            ) if search_object.type_effective_resist_2 is not None else PokemonModel.type_effective.any()),
            (PokemonModel.type_effective.any(
                and_(
                    PokemonTypeEffectiveModel.name == search_object.type_effective_immune.lower(),
                    PokemonTypeEffectiveModel.multiplier == 0.0
                )
            ) if search_object.type_effective_immune is not None else PokemonModel.type_effective.any())
        )
    ))
    response = session.execute(stmt)
    pokemon = []
    for p in response.scalars():
        moves = None
        if search_object.special_move_category is not None:
            moves = ', '.join([m.name for m in p.moves if m.category == search_object.special_move_category])
        pokemon.append({'name': p.name, 'point_value': p.point_value, 'speed': p.speed,
                        'moves': moves})
    return pokemon
