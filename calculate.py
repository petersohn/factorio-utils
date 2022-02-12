#!/usr/bin/env python3
import graphviz
from typing import Dict, Optional, Set, Tuple
import sys

class Product:
    def __init__(
            self, time: float, product: int, inputs: Dict[str, int],
            time_expensive: Optional[float],
            input_expensive: Optional[Dict[str, int]],
            factory_type: str, is_intermediate: bool) -> None:
        self.time = time
        self.product = product
        self.inputs = inputs
        self.time_expensive = time_expensive
        self.input_expensive = input_expensive
        self.factory_type = factory_type
        self.is_intermediate = is_intermediate


class Factory:
    def __init__(self, speed: float, productivity: float) -> None:
        self.speed = speed
        self.productivity = productivity


products: Dict[str, Product] = {
    'coal': Product(
        1, 1,
        {}, None, None,
        'mining drill', True),
    'copper ore': Product(
        1, 1,
        {}, None, None,
        'mining drill', True),
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
    'iron ore': Product(
        1, 1,
        {}, None, None,
        'mining drill', True),
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
    'stone': Product(
        1, 1,
        {}, None, None,
        'mining drill', True),
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


factories: Dict[Tuple[str, bool], Factory] = {
    # assembling machine 3 + 3 prod. module + 1 speed module
    ('assembling machine', True): Factory(1.3125, 1.3),
    # assembling machine 3 + no modules
    ('assembling machine', False): Factory(1.25, 1.0),
    # electric furnace + 1 prod. module + 1 speed module
    ('furnace', True): Factory(2.7, 1.1),
    # electric mining drill + no modules
    ('mining drill', True): Factory(0.5, 1.0),
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
            self._add(input, source, rate * amount / factory.productivity)

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
        sources = graphviz.Digraph()
        sources.body.append('rank=source\n')
        sinks = graphviz.Digraph()
        sinks.body.append('rank=sink\n')
        targets = graphviz.Digraph()
        targets.body.append('rank=same\n')

        node_names: Dict[str, str] = {}
        for item, rate in self.nodes.items():
            name = 'n{}'.format(len(node_names))
            node_names[item] = name

            g = main_graph
            if item == 'end':
                g = sinks
            elif not products[item].inputs:
                g = sources
            elif item in self.targets:
                g = targets

            g.node(name, '{} [{:.1f}]'.format(item, rate))

        main_graph.subgraph(sources)
        main_graph.subgraph(targets)
        main_graph.subgraph(sinks)

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
g.render()
