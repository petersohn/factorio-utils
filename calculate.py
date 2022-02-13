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
            input_expensive: Optional[Dict[str, int]]=None) -> None:
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
        time=1,
        inputs={},
        time_expensive=None,
        input_expensive=None,
        factory_type='mining drill',
        is_intermediate=True),
    'copper ore': Product(
        time=1,
        product=1,
        inputs={},
        time_expensive=None,
        input_expensive=None,
        factory_type='mining drill',
        is_intermediate=True),
    'copper plate': Product(
        time=3.2,
        product=1,
        inputs={'copper ore': 1},
        time_expensive=None,
        input_expensive=None,
        factory_type='furnace',
        is_intermediate=True),
    'copper wire': Product(
        time=0.5,
        product=2,
        inputs={'copper plate': 1},
        time_expensive=None,
        input_expensive=None,
        factory_type='assembling machine',
        is_intermediate=True),
    'electronic circuit': Product(
        time=0.5,
        product=1,
        inputs={'iron plate': 1, 'copper wire': 3},
        time_expensive=None,
        input_expensive={'iron plate': 2, 'copper wire': 8},
        factory_type='assembling machine',
        is_intermediate=True),
    'firearm magazine': Product(
        time=1,
        product=1,
        inputs={'iron plate': 4},
        time_expensive=None,
        input_expensive=None,
        factory_type='assembling machine',
        is_intermediate=False),
    'grenade': Product(
        time=8,
        product=1,
        inputs={'coal': 10, 'iron plate': 5},
        time_expensive=None,
        input_expensive=None,
        factory_type='assembling machine',
        is_intermediate=False),
    'inserter': Product(
        time=0.5,
        product=1,
        inputs={'electronic circuit': 1, 'iron gear wheel': 1, 'iron plate': 1},
        time_expensive=None,
        input_expensive=None,
        factory_type='assembling machine',
        is_intermediate=False),
    'iron gear wheel': Product(
        time=0.5,
        product=1,
        inputs={'iron plate': 2},
        time_expensive=None,
        input_expensive={'iron plate': 4},
        factory_type='assembling machine',
        is_intermediate=True),
    'iron ore': Product(
        time=1,
        product=1,
        inputs={},
        time_expensive=None,
        input_expensive=None,
        factory_type='mining drill',
        is_intermediate=True),
    'iron plate': Product(
        time=3.2,
        product=1,
        inputs={'iron ore': 1},
        time_expensive=None,
        input_expensive=None,
        factory_type='furnace',
        is_intermediate=True),
    'piercing rounds magazine': Product(
        time=3,
        product=1,
        inputs={'copper plate': 5, 'firearm magazine': 1, 'steel plate': 1},
        time_expensive=None,
        input_expensive=None,
        factory_type='assembling machine',
        is_intermediate=False),
    'science pack 1 red': Product(
        time=5,
        product=1,
        inputs={'copper plate': 1, 'iron gear wheel': 1},
        time_expensive=None,
        input_expensive=None,
        factory_type='assembling machine',
        is_intermediate=True),
    'science pack 2 green': Product(
        time=6,
        product=1,
        inputs={'inserter': 1, 'transport belt': 1},
        time_expensive=None,
        input_expensive=None,
        factory_type='assembling machine',
        is_intermediate=True),
    'science pack 3 black': Product(
        time=10,
        product=2,
        inputs={'grenade': 1, 'piercing rounds magazine': 1, 'wall': 2},
        time_expensive=None,
        input_expensive=None,
        factory_type='assembling machine',
        is_intermediate=True),
    'steel plate': Product(
        time=16,
        product=1,
        inputs={'iron plate': 5},
        time_expensive=32,
        input_expensive={'iron plate': 10},
        factory_type='furnace',
        is_intermediate=True),
    'stone': Product(
        time=1,
        product=1,
        inputs={},
        time_expensive=None,
        input_expensive=None,
        factory_type='mining drill',
        is_intermediate=True),
    'stone brick': Product(
        time=3.2,
        product=1,
        inputs={'stone': 2},
        time_expensive=None,
        input_expensive=None,
        factory_type='furnace',
        is_intermediate=True),
    'transport belt': Product(
        time=0.5,
        product=2,
        inputs={'iron plate': 1, 'iron gear wheel': 1},
        time_expensive=None,
        input_expensive=None,
        factory_type='assembling machine',
        is_intermediate=False),
    'wall': Product(
        time=0.5,
        product=1,
        inputs={'stone brick': 5},
        time_expensive=None,
        input_expensive=None,
        factory_type='assembling machine',
        is_intermediate=False),
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
