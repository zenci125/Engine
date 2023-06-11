import Lib.Math.LowLevelMath as llm
import Lib.Engine.BasicClasses as en
import Lib.Engine.GraphicClasses as gs

class EventSystem:
    def __init__(self, events: dict):
        self.events = events

    def add(self, name: str):
        self.events[name] = []

    def remove(self, name: str):
        self.events.pop(name)

    def handle(self, name: str, func: callable):
        self.events[name].append(func)

    def remove_handled(self, name: str, func: callable):
        self.events[name].remove(func)

    def trigger(self, name, *args):
        for event in self.events[name]:
            event(*args)

    def get_handled(self, name: str):
        return self.events.get(name)

    def __getitem__(self, item: str):
        return self.get_handled(item)
