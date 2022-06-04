#!/usr/bin/env python3
import graphviz
import copy
from typing import Dict, Optional, Set, Tuple
import sys


class RenderProduct:
    def __init__(self, color: str, category: Optional[str]=None):
        self.color = color
        self.category = category


class Product(RenderProduct):
    def __init__(
            self,
            time: float,
            inputs: Dict[str, int],
            color: str,
            factory_type: str,
            product: int=1,
            time_expensive: Optional[float]=None,
            input_expensive: Optional[Dict[str, int]]=None,
            category: Optional[str]=None) -> None:
        super().__init__(color, category)
        self.time = time
        self.product = product
        self.inputs = inputs
        self.time_expensive = time_expensive
        self.input_expensive = input_expensive
        self.factory_type = factory_type


class Factory:
    def __init__(self, speed: float, productivity: float) -> None:
        self.speed = speed
        self.productivity = productivity


products: Dict[str, Product] = {
    'accumulator': Product(
        time=10,
        product=1,
        inputs={'battery': 5, 'iron plate': 2},
        color='darkslategray2',
        factory_type='assembling machine final'),
    'advanced circuit': Product(
        time=6,
        inputs={'copper wire': 4, 'electronic circuit': 2, 'plastic bar': 2},
        input_expensive={'copper wire': 8, 'electronic circuit': 2, 'plastic bar': 4},
        color='firebrick3',
        factory_type='assembling machine IM'),
    'battery': Product(
        time=4,
        time_expensive=5,
        inputs={'copper plate': 1, 'iron plate': 1, 'sulfuric acid': 20},
        input_expensive={'copper plate': 1, 'iron plate': 1, 'sulfuric acid': 40},
        color='darkcyan',
        factory_type='chemical plant'),
    'coal': Product(
        time=1,
        inputs={},
        factory_type='mining drill',
        color='gray10',
        category='raw'),
    'copper ore': Product(
        time=1,
        inputs={},
        factory_type='mining drill',
        color='coral3',
        category='raw'),
    'copper plate': Product(
        time=3.2,
        inputs={'copper ore': 1},
        factory_type='furnace',
        color='coral2',
        category='plate'),
    'copper wire': Product(
        time=0.5,
        product=2,
        inputs={'copper plate': 1},
        color='coral',
        factory_type='assembling machine IM'),
    'electric engine unit': Product(
        time=10,
        inputs={'electronic circuit': 2, 'engine unit': 1, 'lubricant': 15},
        color='darkmagenta',
        factory_type='assembling machine IM'),
    'electric furnace': Product(
        time=5,
        inputs={'advanced circuit': 5, 'steel plate': 10, 'stone brick': 10},
        color='darkorange4',
        factory_type='assembling machine final'),
    'electronic circuit': Product(
        time=0.5,
        inputs={'iron plate': 1, 'copper wire': 3},
        input_expensive={'iron plate': 2, 'copper wire': 8},
        color='forestgreen',
        factory_type='assembling machine IM'),
    'engine unit': Product(
        time=10,
        inputs={'iron gear wheel': 1, 'pipe': 2, 'steel plate': 1},
        color='burlywood3',
        factory_type='assembling machine IM'),
    'firearm magazine': Product(
        time=1,
        inputs={'iron plate': 4},
        color='goldenrod3',
        factory_type='assembling machine final'),
    'flying robot frame': Product(
        time=20,
        inputs={
            'battery': 2,
            'electric engine unit': 1,
            'electronic circuit': 3,
            'steel plate': 1,
        },
        color='lightsteelblue4',
        factory_type='assembling machine IM'),
    'grenade': Product(
        time=8,
        inputs={'coal': 10, 'iron plate': 5},
        color='grey20',
        factory_type='assembling machine final'),
    'inserter': Product(
        time=0.5,
        inputs={'electronic circuit': 1, 'iron gear wheel': 1, 'iron plate': 1},
        color='gold2',
        factory_type='assembling machine final'),
    'iron gear wheel': Product(
        time=0.5,
        inputs={'iron plate': 2},
        input_expensive={'iron plate': 4},
        color='gray65',
        factory_type='assembling machine IM'),
    'iron ore': Product(
        time=1,
        inputs={},
        factory_type='mining drill',
        color='cadetblue4',
        category='raw'),
    'iron plate': Product(
        time=3.2,
        inputs={'iron ore': 1},
        factory_type='furnace',
        color='slategray4',
        category='plate'),
    'iron stick': Product(
        time=0.5,
        product=2,
        inputs={'iron plate': 1},
        color='gray40',
        factory_type='assembling machine IM'),
    'low density structure': Product(
        time=20,
        inputs={'copper plate': 20, 'plastic bar': 5, 'steel plate': 2},
        input_expensive={'copper plate': 20, 'plastic bar': 30, 'steel plate': 2},
        color='bisque4',
        factory_type='assembling machine IM'),
    'lubricant': Product(
        time=1,
        product=10,
        inputs={'heavy oil': 10},
        color='darkgreen',
        factory_type='chemical plant'),
    'piercing rounds magazine': Product(
        time=3,
        inputs={'copper plate': 5, 'firearm magazine': 1, 'steel plate': 1},
        color='crimson',
        factory_type='assembling machine final'),
    'pipe': Product(
        time=0.5,
        inputs={'iron plate': 1},
        input_expensive={'iron plate': 2},
        color='navajowhite4',
        factory_type='assembling machine final'),
    'plastic bar': Product(
        time=1,
        inputs={'coal': 1, 'petroleum gas': 20},
        factory_type='chemical plant',
        color='gray80',
        category='plate'),
    'processing unit': Product(
        time=10,
        inputs={'advanced circuit': 2, 'electronic circuit': 20, 'sulfuric acid': 5},
        input_expensive={'advanced circuit': 2, 'electronic circuit': 20, 'sulfuric acid': 10},
        color='blue3',
        factory_type='assembling machine IM'),
    'productivity module 1': Product(
        time=15,
        inputs={'advanced circuit': 5, 'electronic circuit': 5},
        color='brown',
        factory_type='assembling machine final'),
    'productivity module 2': Product(
        time=30,
        inputs={'productivity module 1': 4, 'advanced circuit': 5, 'processing unit': 5},
        color='brown',
        factory_type='assembling machine final'),
    'productivity module 3': Product(
        time=60,
        inputs={'productivity module 2': 5, 'advanced circuit': 5, 'processing unit': 5},
        color='brown',
        factory_type='assembling machine final'),
    'radar': Product(
        time=0.5,
        product=1,
        inputs={'electronic circuit': 5, 'iron gear wheel': 5, 'iron plate': 10},
        color='burlywood3',
        factory_type='assembling machine final'),
    'rail': Product(
        time=0.5,
        product=2,
        inputs={'iron stick': 1, 'steel plate': 1, 'stone': 1},
        color='burlywood2',
        factory_type='assembling machine final'),
    'rocket control unit': Product(
        time=30,
        product=1,
        inputs={'processing unit': 1, 'speed module 1': 1},
        color='darkolivegreen4',
        factory_type='assembling machine IM'),
    'rocket fuel': Product(
        time=30,
        product=1,
        inputs={'light oil': 10, 'solid fuel': 10},
        color='darkgoldenrod2',
        factory_type='assembling machine IM'),
    'rocket part': Product(
        time=3,
        product=1,
        inputs={'low density structure': 10, 'rocket control unit': 10, 'rocket fuel': 10},
        color='darkorange4',
        factory_type='rocket silo'),
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
        color='deepskyblue4',
        factory_type='assembling machine IM'),
    'science': Product(
        time=60,
        inputs={
            'science pack 1 red': 1,
            'science pack 2 green': 1,
            'science pack 3 black': 1,
            'science pack 4 blue': 1,
            'science pack 5 purple': 1,
            'science pack 6 yellow': 1,
            'science pack 7 white': 1,
        },
        factory_type='lab',
        color='skyblue3'),
    'science pack 1 red': Product(
        time=5,
        inputs={'copper plate': 1, 'iron gear wheel': 1},
        factory_type='assembling machine IM',
        color='red2',
        category='science'),
    'science pack 2 green': Product(
        time=6,
        inputs={'inserter': 1, 'transport belt': 1},
        factory_type='assembling machine IM',
        color='green3',
        category='science'),
    'science pack 3 black': Product(
        time=10,
        product=2,
        inputs={'grenade': 1, 'piercing rounds magazine': 1, 'wall': 2},
        factory_type='assembling machine IM',
        color='gray30',
        category='science'),
    'science pack 4 blue': Product(
        time=24,
        product=2,
        inputs={'advanced circuit': 3, 'engine unit': 2, 'sulfur': 1},
        factory_type='assembling machine IM',
        color='cyan2',
        category='science'),
    'science pack 5 purple': Product(
        time=21,
        product=3,
        inputs={'electric furnace': 1, 'productivity module 1': 1, 'rail': 30},
        factory_type='assembling machine IM',
        color='magenta3',
        category='science'),
    'science pack 6 yellow': Product(
        time=21,
        product=3,
        inputs={'flying robot frame': 1, 'low density structure': 3, 'processing unit': 2},
        factory_type='assembling machine IM',
        color='yellow3',
        category='science'),
    # This part represents the rocket launch
    'science pack 7 white': Product(
        time=40,  # approximate time of launch
        product=1000,
        inputs={'rocket part': 100, 'satellite': 1},
        factory_type='raw',
        color='grey70',
        category='science'),
    'solar panel': Product(
        time=10,
        product=1,
        inputs={'copper plate': 5, 'electronic circuit': 15, 'steel plate': 5},
        color='cornflowerblue',
        factory_type='assembling machine final'),
    # most efficient recipe
    'solid fuel': Product(
        time=2,
        product=1,
        inputs={'light oil': 10},
        color='gray20',
        factory_type='chemical plant'),
    'speed module 1': Product(
        time=15,
        inputs={'advanced circuit': 5, 'electronic circuit': 5},
        color='dodgerblue3',
        factory_type='assembling machine final'),
    'speed module 2': Product(
        time=30,
        inputs={'speed module 1': 4, 'advanced circuit': 5, 'processing unit': 5},
        color='dodgerblue2',
        factory_type='assembling machine final'),
    'speed module 3': Product(
        time=60,
        inputs={'speed module 2': 5, 'advanced circuit': 5, 'processing unit': 5},
        color='dodgerblue1',
        factory_type='assembling machine final'),
    'steel plate': Product(
        time=16,
        inputs={'iron plate': 5},
        time_expensive=32,
        input_expensive={'iron plate': 10},
        color='slategray3',
        factory_type='furnace'),
    'stone': Product(
        time=1,
        inputs={},
        factory_type='mining drill',
        color='lightgoldenrod4',
        category='raw'),
    'stone brick': Product(
        time=3.2,
        inputs={'stone': 2},
        factory_type='furnace',
        color='lightblue3',
        category='plate'),
    'sulfur': Product(
        time=1,
        product=2,
        inputs={'petroleum gas': 30, 'water': 30},
        color='lightgoldenrod2',
        factory_type='chemical plant'),
    'sulfuric acid': Product(
        time=1,
        product=50,
        inputs={'iron plate': 1, 'sulfur': 5, 'water': 100},
        color='lightsalmon2',
        factory_type='chemical plant'),
    'transport belt': Product(
        time=0.5,
        product=2,
        inputs={'iron plate': 1, 'iron gear wheel': 1},
        color='khaki3',
        factory_type='assembling machine final'),
    'wall': Product(
        time=0.5,
        inputs={'stone brick': 5},
        color='khaki4',
        factory_type='assembling machine final'),

    # TODO: implement oil processing
    'crude oil': Product(
        time=1,
        inputs={},
        factory_type='raw',
        color='black',
        category='raw'),
    'heavy oil': Product(
        time=1,
        inputs={},
        factory_type='raw',
        color='darkorange3',
        category='fluid'),
    'light oil': Product(
        time=1,
        inputs={},
        factory_type='raw',
        color='darkgoldenrod2',
        category='fluid'),
    'petroleum gas': Product(
        time=1,
        inputs={},
        factory_type='raw',
        color='gray70',
        category='fluid'),
    'water': Product(
        time=1,
        inputs={},
        factory_type='raw',
        color='skyblue2',
        category='fluid'),
}


render_products: Dict[str, RenderProduct] = copy.copy(products)
render_products['heavy oil cracking'] = RenderProduct(
    color=products['heavy oil'].color,
    category='oil processing')
render_products['light oil cracking'] = RenderProduct(
    color=products['light oil'].color,
    category='oil processing')
render_products['advanced oil processing'] = RenderProduct(
    color='darkorange4',
    category='oil processing')


factories: Dict[str, Factory] = {
    # assembling machine 3 + 3 prod. module + 1 speed module
    'assembling machine IM': Factory(1.3125, 1.3),
    # assembling machine 3 + no modules
    'assembling machine final': Factory(1.25, 1.0),
    # assembling machine 3 + 2 speed modules
    'assembling machine speed': Factory(2.5, 1.0),
    # electric furnace + 1 prod. module + 1 efficiency module
    'furnace': Factory(1.7, 1.1),
    # electric mining drill + no modules
    'mining drill': Factory(0.5, 1.0),
    # 2 prod. module + 1 speed module
    'chemical plant': Factory(1.2, 1.2),
    # TODO: implement oil processing
    'raw': Factory(1.0, 1.0),
    # 4 prod. science packs
    'rocket silo': Factory(0.4, 1.4),
    # full research + 2 prod. module
    'lab': Factory(2.45, 1.2),
}


def calculate_forward(
        factory: Factory,
        input_rate: float,
        factory_input: float,
        time: float,
        outputs: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
    num_factories = input_rate * time / factory_input / factory.speed
    output_rates = {
        name: rate * factory.productivity * input_rate / factory_input
        for name, rate in outputs.items()
    }
    return (num_factories, output_rates)


class Graph:
    def __init__(self, expensive: bool) -> None:
        self.expensive = expensive
        self.nodes: Dict[str, float] = {'end': 0.0}
        self.edges: Dict[Tuple[str, str], float] = {}
        self.targets: Set[str] = set()

    def _add(self, source: str, target: str, rate: float) -> None:
        product = products[source]
        factory = factories[product.factory_type]

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

    def add_oil_processing(self) -> None:
        if 'heavy oil' in self.nodes or 'light oil' in self.nodes:
            raise RuntimeError('Only petroleum gas is supported')
        if 'petroleum gas' not in self.nodes:
            return

        # Oil refinery uses the same modules
        factory = factories['chemical plant']
        advanced_oil_processing, outputs = calculate_forward(
            factory=factory,
            input_rate=1.0,
            factory_input=100,
            time=5,
            outputs={'heavy oil': 25, 'light oil': 45, 'petroleum gas': 55})
        heavy_oil_cracking, light_oil = calculate_forward(
            factory=factory,
            input_rate=outputs['heavy oil'],
            factory_input=40,
            time=2,
            outputs={'light oil': 30})
        light_oil_cracking, petroleum_gas = calculate_forward(
            factory=factory,
            input_rate=outputs['light oil'] + light_oil['light oil'],
            factory_input=30,
            time=2,
            outputs={'petroleum gas': 20})

        multiplier = self.nodes['petroleum gas'] / (
            outputs['petroleum gas'] + petroleum_gas['petroleum gas'])

        def add_raw_input(source: str, target: str, amount: float):
            self.nodes.setdefault(source, 0.0)
            self.nodes[source] += amount * multiplier
            self.edges[(source, target)] = amount * multiplier

        self.nodes['advanced oil processing'] = advanced_oil_processing * multiplier
        self.nodes['heavy oil cracking'] = heavy_oil_cracking * multiplier
        self.nodes['light oil cracking'] = light_oil_cracking * multiplier

        self.edges[('advanced oil processing', 'heavy oil cracking')] = outputs['heavy oil'] * multiplier
        self.edges[('advanced oil processing', 'light oil cracking')] = outputs['light oil'] * multiplier
        self.edges[('advanced oil processing', 'petroleum gas')] = outputs['petroleum gas'] * multiplier
        self.edges[('heavy oil cracking', 'light oil cracking')] = light_oil['light oil'] * multiplier
        self.edges[('light oil cracking', 'petroleum gas')] = petroleum_gas['petroleum gas'] * multiplier

        add_raw_input('crude oil', 'advanced oil processing', 1.0)
        # add_raw_input('water', 'advanced oil processing', advanced_oil_processing * 50 / 5)
        # add_raw_input('water', 'heavy oil cracking', heavy_oil_cracking * 30 / 2)
        # add_raw_input('water', 'light oil cracking', light_oil_cracking * 30 / 2)

        products['water'].category = 'raw'


    def render(self) -> None:
        main_graph = graphviz.Digraph(format='svg')
        main_graph.body.append('rankdir=LR;\n')
        subgraphs: Dict[str, graphviz.Digraph] = {}

        for item, rate in self.nodes.items():
            product = render_products.get(item)
            category = None
            color = None
            if product is not None:
                category = product.category
                color = product.color

            if category is not None:
                if category not in subgraphs:
                    g = graphviz.Digraph(category)
                    g.body.append('rank=same;\n')
                    subgraphs[category] = g
                else:
                    g = subgraphs[category]
            else:
                g = main_graph


            g.node(item, '{} [{:.1f}]'.format(item, rate),
                color=color, fontcolor=color)

        for subgraph in subgraphs.values():
            main_graph.subgraph(subgraph)

        for (source, target), rate in self.edges.items():
            color = render_products[source].color
            main_graph.edge(
                source, target, label='{:.1f}'.format(rate),
                color=color, fontcolor=color)

        print(main_graph.source, file=sys.stderr)
        print(main_graph.pipe(encoding='utf-8'))


def speed_up_modules() -> None:
    for name, product in products.items():
        if 'module' in name:
            product.factory_type = 'assembling machine speed'

g = Graph(True)

######## Science ########
science_pack_factory = factories['assembling machine IM']
lab = factories['lab']
science_pack_rate = science_pack_factory.speed * science_pack_factory.productivity * lab.productivity

# g.add('science', science_pack_rate)

######## Modules ########

# speed_up_modules()
module = products['speed module 3']
module_factory = factories[module.factory_type]
module_rate = module_factory.speed * module_factory.productivity / module.time

# g.add('speed module 3', module_rate * 2)
# g.add('productivity module 3', module_rate * 4)
g.add_oil_processing()

# g.add('plastic bar', 45)
g.add('iron plate', 45)
# g.add('copper wire', 45)

g.render()
