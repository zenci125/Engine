import pytest
from Lib.Engine.ConfigClass import GameConfiguration

class TestConfig:
    def test_init(self):
        a = GameConfiguration("D:/viseng/config/config.txt")

        res = ["Gennady", "Hotel"]

        assert list(a.configuration.key()) == res