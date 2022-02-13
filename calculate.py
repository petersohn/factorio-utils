#!/usr/bin/env python3
import graphviz
from typing import Dict, Optional, Set, Tuple
import sys

class Product:
    def __init__(
            self,
            time: float,
            inputs: Dict[str, int],
            factory_type: str,
            is_intermediate: bool,
            product: int=1,
            time_expensive: Optional[float]=None,
            input_expensive: Optional[Dict[str, int]]=None,
            category: Optional[str]=None) -> None:
        self.time = time
        self.product = product
        self.inputs = inputs
        self.time_expensive = time_expensive
        self.input_expensive = input_expensive
        self.factory_type = factory_type
        self.is_intermediate = is_intermediate
        self.category = category


class Factory:
    def __init__(self, speed: float, productivity: float) -> None:
        self.speed = speed
        self.productivity = productivity


products: Dict[str, Product] = {
    'accumulator': Product(
        time=10,
        product=1,
        inputs={'battery': 5, 'iron plate': 2},
        factory_type='assembling machine',
        is_intermediate=False),
    'advanced circuit': Product(
        time=6,
        inputs={'copper wire': 4, 'electronic circuit': 2, 'plastic bar': 2},
        input_expensive={'copper wire': 8, 'electronic circuit': 2, 'plastic bar': 4},
        factory_type='assembling machine',
        is_intermediate=True),
    'battery': Product(
        time=4,
        time_expensive=5,
        inputs={'copper plate': 1, 'iron plate': 1, 'sulfuric acid': 20},
        input_expensive={'copper plate': 1, 'iron plate': 1, 'sulfuric acid': 40},
        factory_type='chemical plant',
        is_intermediate=True),
    'coal': Product(
        time=1,
        inputs={},
        factory_type='mining drill',
        is_intermediate=True,
        category='raw'),
    'copper ore': Product(
        time=1,
        inputs={},
        factory_type='mining drill',
        is_intermediate=True,
        category='raw'),
    'copper plate': Product(
        time=3.2,
        inputs={'copper ore': 1},
        factory_type='furnace',
        is_intermediate=True,
        category='plate'),
    'copper wire': Product(
        time=0.5,
        product=2,
        inputs={'copper plate': 1},
        factory_type='assembling machine',
        is_intermediate=True),
    'electric engine unit': Product(
        time=10,
        inputs={'electronic circuit': 2, 'engine unit': 1, 'lubricant': 15},
        factory_type='assembling machine',
        is_intermediate=True),
    'electric furnace': Product(
        time=5,
        inputs={'advanced circuit': 5, 'steel plate': 10, 'stone brick': 10},
        factory_type='assembling machine',
        is_intermediate=False),
    'electronic circuit': Product(
        time=0.5,
        inputs={'iron plate': 1, 'copper wire': 3},
        input_expensive={'iron plate': 2, 'copper wire': 8},
        factory_type='assembling machine',
        is_intermediate=True),
    'engine unit': Product(
        time=10,
        inputs={'iron gear wheel': 1, 'pipe': 2, 'steel plate': 1},
        factory_type='assembling machine',
        is_intermediate=True),
    'firearm magazine': Product(
        time=1,
        inputs={'iron plate': 4},
        factory_type='assembling machine',
        is_intermediate=False),
    'flying robot frame': Product(
        time=20,
        inputs={
            'battery': 2,
            'electric engine unit': 1,
            'electronic circuit': 3,
            'steel plate': 1,
        },
        factory_type='assembling machine',
        is_intermediate=True),
    'grenade': Product(
        time=8,
        inputs={'coal': 10, 'iron plate': 5},
        factory_type='assembling machine',
        is_intermediate=False),
    'inserter': Product(
        time=0.5,
        inputs={'electronic circuit': 1, 'iron gear wheel': 1, 'iron plate': 1},
        factory_type='assembling machine',
        is_intermediate=False),
    'iron gear wheel': Product(
        time=0.5,
        inputs={'iron plate': 2},
        input_expensive={'iron plate': 4},
        factory_type='assembling machine',
        is_intermediate=True),
    'iron ore': Product(
        time=1,
        inputs={},
        factory_type='mining drill',
        is_intermediate=True,
        category='raw'),
    'iron plate': Product(
        time=3.2,
        inputs={'iron ore': 1},
        factory_type='furnace',
        is_intermediate=True,
        category='plate'),
    'iron stick': Product(
        time=0.5,
        product=2,
        inputs={'iron plate': 1},
        factory_type='assembling machine',
        is_intermediate=True),
    'low density structure': Product(
        time=20,
        inputs={'copper plate': 20, 'plastic bar': 5, 'steel plate': 2},
        input_expensive={'copper plate': 20, 'plastic bar': 30, 'steel plate': 2},
        factory_type='assembling machine',
        is_intermediate=True),
    'lubricant': Product(
        time=1,
        product=10,
        inputs={'heavy oil': 10},
        factory_type='chemical plant',
        is_intermediate=True),
    'piercing rounds magazine': Product(
        time=3,
        inputs={'copper plate': 5, 'firearm magazine': 1, 'steel plate': 1},
        factory_type='assembling machine',
        is_intermediate=False),
    'pipe': Product(
        time=0.5,
        inputs={'iron plate': 1},
        input_expensive={'iron plate': 2},
        factory_type='assembling machine',
        is_intermediate=False),
    'plastic bar': Product(
        time=1,
        inputs={'coal': 1, 'petroleum gas': 20},
        factory_type='chemical plant',
        is_intermediate=True,
        category='plate'),
    'processing unit': Product(
        time=10,
        inputs={'advanced circuit': 2, 'electronic circuit': 20, 'sulfuric acid': 5},
        input_expensive={'advanced circuit': 2, 'electronic circuit': 20, 'sulfuric acid': 10},
        factory_type='assembling machine',
        is_intermediate=True),
    'productivity module 1': Product(
        time=15,
        inputs={'advanced circuit': 5, 'electronic circuit': 5},
        factory_type='assembling machine',
        is_intermediate=False),
    'radar': Product(
        time=0.5,
        product=1,
        inputs={'electronic circuit': 5, 'iron gear wheel': 5, 'iron plate': 10},
        factory_type='assembling machine',
        is_intermediate=False),
    'rail': Product(
        time=0.5,
        product=2,
        inputs={'iron stick': 1, 'steel plate': 1, 'stone': 1},
        factory_type='assembling machine',
        is_intermediate=False),
    'rocket control unit': Product(
        time=30,
        product=1,
        inputs={'processing unit': 1, 'speed module 1': 1},
        factory_type='assembling machine',
        is_intermediate=True),
    'rocket fuel': Product(
        time=30,
        product=1,
        inputs={'light oil': 10, 'solid fuel': 10},
        factory_type='assembling machine',
        is_intermediate=True),
    'rocket part': Product(
        time=3,
        product=1,
        inputs={'low density structure': 10, 'rocket control unit': 10, 'rocket fuel': 10},
        factory_type='rocket silo',
        is_intermediate=True),
    'satellite': Product(
        time=5,
        product=1,
        inputs={
            'accumulator': 100,
            'low density structure': 100,
            'processing unit': 100,
            'radar': 5,
            'rocket fuel': 50,
            'solar panel': 100,
        },
        factory_type='assembling machine',
        is_intermediate=True),
    'science pack 1 red': Product(
        time=5,
        inputs={'copper plate': 1, 'iron gear wheel': 1},
        factory_type='assembling machine',
        is_intermediate=True,
        category='science'),
    'science pack 2 green': Product(
        time=6,
        inputs={'inserter': 1, 'transport belt': 1},
        factory_type='assembling machine',
        is_intermediate=True,
        category='science'),
    'science pack 3 black': Product(
        time=10,
        product=2,
        inputs={'grenade': 1, 'piercing rounds magazine': 1, 'wall': 2},
        factory_type='assembling machine',
        is_intermediate=True,
        category='science'),
    'science pack 4 blue': Product(
        time=24,
        product=2,
        inputs={'advanced circuit': 3, 'engine unit': 2, 'sulfur': 1},
        factory_type='assembling machine',
        is_intermediate=True,
        category='science'),
    'science pack 5 purple': Product(
        time=21,
        product=3,
        inputs={'electric furnace': 1, 'productivity module 1': 1, 'rail': 30},
        factory_type='assembling machine',
        is_intermediate=True,
        category='science'),
    'science pack 6 yellow': Product(
        time=21,
        product=3,
        inputs={'flying robot frame': 1, 'low density structure': 3, 'processing unit': 2},
        factory_type='assembling machine',
        is_intermediate=True,
        category='science'),
    # This part represents the rocket launch
    'science pack 7 white': Product(
        time=40,  # approximate time of launch
        product=1000,
        inputs={'rocket part': 100, 'satellite': 1},
        factory_type='raw',
        is_intermediate=False,  # not intermediate, rocket parts are
        category='science'),
    'solar panel': Product(
        time=10,
        product=1,
        inputs={'copper plate': 5, 'electronic circuit': 15, 'steel plate': 5},
        factory_type='assembling machine',
        is_intermediate=False),
    # most efficient recipe
    'solid fuel': Product(
        time=2,
        product=1,
        inputs={'light oil': 10},
        factory_type='chemical plant',
        is_intermediate=True),
    'speed module 1': Product(
        time=15,
        inputs={'advanced circuit': 5, 'electronic circuit': 5},
        factory_type='assembling machine',
        is_intermediate=False),
    'steel plate': Product(
        time=16,
        inputs={'iron plate': 5},
        time_expensive=32,
        input_expensive={'iron plate': 10},
        factory_type='furnace',
        is_intermediate=True),
    'stone': Product(
        time=1,
        inputs={},
        factory_type='mining drill',
        is_intermediate=True,
        category='raw'),
    'stone brick': Product(
        time=3.2,
        inputs={'stone': 2},
        factory_type='furnace',
        is_intermediate=True,
        category='plate'),
    'sulfur': Product(
        time=1,
        product=2,
        inputs={'petroleum gas': 30, 'water': 30},
        factory_type='chemical plant',
        is_intermediate=True),
    'sulfuric acid': Product(
        time=1,
        product=50,
        inputs={'iron plate': 1, 'sulfur': 5, 'water': 100},
        factory_type='chemical plant',
        is_intermediate=True),
    'transport belt': Product(
        time=0.5,
        product=2,
        inputs={'iron plate': 1, 'iron gear wheel': 1},
        factory_type='assembling machine',
        is_intermediate=False),
    'wall': Product(
        time=0.5,
        inputs={'stone brick': 5},
        factory_type='assembling machine',
        is_intermediate=False),

    # TODO: implement oil processing
    'heavy oil': Product(
        time=1,
        inputs={},
        factory_type='raw',
        is_intermediate=True,
        category='fluid'),
    'light oil': Product(
        time=1,
        inputs={},
        factory_type='raw',
        is_intermediate=True,
        category='fluid'),
    'petroleum gas': Product(
        time=1,
        inputs={},
        factory_type='raw',
        is_intermediate=True,
        category='fluid'),
    'water': Product(
        time=1,
        inputs={},
        factory_type='raw',
        is_intermediate=True,
        category='fluid'),
}


factories: Dict[Tuple[str, bool], Factory] = {
    # assembling machine 3 + 3 prod. module + 1 speed module
    ('assembling machine', True): Factory(1.3125, 1.3),
    # assembling machine 3 + no modules
    ('assembling machine', False): Factory(1.25, 1.0),
    # electric furnace + 1 prod. module + 1 speed module
    ('furnace', True): Factory(2.7, 1.1),
    # electric mining drill + no modules
    ('mining drill', True): Factory(0.5, 1.0),
    # 2 prod. module + 1 speed module
    ('chemical plant', True): Factory(1.2, 1.2),
    # TODO: implement oil processing
    ('raw', True): Factory(1.0, 1.0),
    ('raw', False): Factory(1.0, 1.0),
    # 4 prod. science packs
    ('rocket silo', True): Factory(0.4, 1.4),
}


class Graph:
    def __init__(self, expensive: bool) -> None:
        self.expensive = expensive
        self.nodes: Dict[str, float] = {'end': 0.0}
        self.edges: Dict[Tuple[str, str], float] = {}
        self.targets: Set[str] = set()

    def _add(self, source: str, target: str, rate: float) -> None:
        product = products[source]
        factory = factories[(product.factory_type, product.is_intermediate)]

        time = product.time_expensive if self.expensive and product.time_expensive is not None else product.time
        inputs = product.input_expensive if self.expensive and product.input_expensive is not None else product.inputs

        self.nodes.setdefault(source, 0.0)
        self.nodes[source] += rate * time / factory.speed / factory.productivity / product.product
        self.edges.setdefault((source, target), 0.0)
        self.edges[(source, target)] += rate

        for input, amount in inputs.items():
            self._add(input, source, rate * amount / factory.productivity / product.product)

    def add(self, item: str, rate: float) -> None:
        if item not in products:
            for name in products.keys():
                if name.startswith(item):
                    item = name
                    break
            else:
                raise RuntimeError('Item not found: {}'.format(item))
        self.targets.add(item)
        self._add(item, 'end', rate)

    def render(self) -> None:
        main_graph = graphviz.Digraph(format='svg')
        main_graph.body.append('rankdir=LR;\n')
        subgraphs: Dict[str, graphviz.Digraph] = {}

        node_names: Dict[str, str] = {}
        for item, rate in self.nodes.items():
            name = 'n{}'.format(len(node_names))
            node_names[item] = name
            product = products.get(item)
            category = None
            if product is not None:
                category = product.category

            if category is not None:
                if category not in subgraphs:
                    g = graphviz.Digraph(category)
                    g.body.append('rank=same;\n')
                    subgraphs[category] = g
                else:
                    g = subgraphs[category]
            else:
                g = main_graph


            g.node(name, '{} [{:.1f}]'.format(item, rate))

        for subgraph in subgraphs.values():
            main_graph.subgraph(subgraph)

        for (source, target), rate in self.edges.items():
            main_graph.edge(
                node_names[source], node_names[target],
                label='{:.1f}'.format(rate))

        print(main_graph.source, file=sys.stderr)
        print(main_graph.pipe(encoding='utf-8'))


science_pack_rate = 1.3 * 1.3125

g = Graph(True)
g.add('science pack 1', science_pack_rate)
g.add('science pack 2', science_pack_rate)
g.add('science pack 3', science_pack_rate)
g.add('science pack 4', science_pack_rate)
g.add('science pack 5', science_pack_rate)
g.add('science pack 6', science_pack_rate)
g.add('science pack 7', science_pack_rate)
g.render()
