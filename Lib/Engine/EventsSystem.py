import Lib.Math.LowLevelMath as llm
import Lib.Engine.BasicClasses as en
import Lib.Engine.GraphicClasses as gs

class EventSystem:
    def __init__(self, events: dict):
        self.events = events

    def add(self, name):
        self.events[name] = []

    def remove(self, name):
        self.events.pop(name)

    def handle(self, name, func):
        self.events[name].append(func)

    def remove_handled(self, name, func):
        self.events[name].remove(func)

    def trigger(self, name, *args):
        for event in self.events[name]:
            event(*args)

    def get_handled(self, name):
        return self.events.get(name)

    def __getitem__(self, item):
        return self.get_handled(item)
