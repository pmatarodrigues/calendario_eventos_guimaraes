import json
from aggregators.emguimaraes import Emguimaraes 

aggregators = {
    "emguimaraes": Emguimaraes
}

eventos = {}

for name, aggregator in aggregators.items():
    aggregatorEvents = aggregator.get_events()
    eventos[name] = aggregatorEvents

print(json.dumps(eventos))

# #TODO: adicionar verificações, se existe antes de trabalhar dados
