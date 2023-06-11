import Lib.Engine.EventsSystem as evs
import pytest

class TestEvents:
    def test_init(self):
        events_dict = dict({"UP": [1, 2]})
        a = evs.EventSystem(events_dict)

        res = "UP"

        assert list(a.events.keys())[0] == res

    def test_add(self):
        events_dict = dict({"UP": [1, 3]})
        a = evs.EventSystem(events_dict)
        a.add("DOWN")

        res = []

        assert res == a.events.get("DOWN")

    def test_remove(self):
        events_dict = dict({"UP": [1, 0], "DOWN": ["cringe", 3]})
        a = evs.EventSystem(events_dict)
        a.remove("DOWN")

        res = 1

        assert len(list(a.events)) == res

    def test_handle(self):
        events_dict = dict({"UP": [1, 0], "DOWN": ["cringe", 3]})
        a = evs.EventSystem(events_dict)
        a.handle("DOWN", 1)

        res = ["cringe", 3, 1]

        assert res == a.events.get("DOWN")

    def test_trigger(self):
        mas = list()
        events_dict = dict({"UP": [mas.append, mas.append, mas.remove], "DOWN": ["cringe", 3]})
        a = evs.EventSystem(events_dict)
        a.trigger("UP", 1)

        res = [1]

        assert res == mas

    def test_handled(self):
        events_dict = dict({"UP": [1], "DOWN": ["cringe", 3]})
        a = evs.EventSystem(events_dict)

        res = [1]

        assert res == a.get_handled("UP")

