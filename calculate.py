from typing import Map

class Product:
    def __init__(
            self, time: float, product: int, input: Map[str, int],
            time_expensive, input_expensive: Optional[Map[str, int]],
            factory_type: str, is_intermediate: bool):
        self.time = time
        self.input = input
        self.factory_type = factory_type
        self.is_intermediate = is_intermediate


products: Map[str, Product] = {
    'copper plate': Product(
        3.2, 1,
        {'copper ore': 1}, None, None,
        'furnace', True),
    'copper wire': Product(
        0.5, 2,
        {'copper plate': 1}, None, None,
        'assembling machine', True),
    'electronic circuit': Product(
        0.5, 1,
        {'iron plate': 1, 'copper wire': 3},
        None,
        {'iron plate': 2, 'copper wire': 8},
        'assembling machine', True),
    'firearm magazine': Product(
        1, 1,
        {'iron plate': 4}, None, None,
        'assembling machine', False),
    'grenade': Product(
        8, 1,
        {'coal': 10, 'iron plate': 5},
        None, None,
        'assembling machine', False),
    'inserter': Product(
        0.5, 1,
        {'electronic circuit': 1, 'iron gear wheel': 1, 'iron plate': 1},
        None, None,
        'assembling machine', False),
    'iron gear wheel': Product(
        0.5, 1,
        {'iron plate': 2}, None, {'iron plate': 4},
        'assembling machine', True),
    'iron plate': Product(
        3.2, 1,
        {'iron ore': 1}, None, None,
        'furnace', True),
    'piercing rounds magazine': Product(
        3, 1,
        {'copper plate': 5, 'firearm magazine': 1, 'steel plate': 1},
        None, None,
        'assembling machine', False),
    'science pack 1 red': Product(
        5, 1,
        {'copper plate': 1, 'iron gear wheel': 1}, None, None,
        'assembling machine', True),
    'science pack 2 green': Product(
        6, 1,
        {'inserter': 1, 'transport belt': 1}, None, None,
        'assembling machine', True),
    'science pack 3 black': Product(
        10, 2,
        {'grenade': 1, 'piercing rounds magazine': 1, 'wall': 2}, None, None,
        'assembling machine', True),
    'steel plate': Product(
        16, 1,
        {'iron plate': 5}, 32, {'iron plate': 10},
        'furnace', True),
    'stone brick': Product(
        3.2, 1,
        {'stone': 2}, None, None,
        'furnace', True),
    'transport belt': Product(
        0.5, 2,
        {'iron plate': 1, 'iron gear wheel': 1}, None, None,
        'assembling machine', False),
    'wall': Product(
        0.5, 1,
        {'stone brick': 5}, None, None,
        'assembling machine', False),
}
