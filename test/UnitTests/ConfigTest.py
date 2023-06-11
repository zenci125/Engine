from Lib.Engine.ConfigClass import GameConfiguration
import pytest

class TestConfig:
    def test_init(self):
        con = GameConfiguration("D:/py projects/viseng/config/test.txt")

        res = ["Gennady", "Hotel"]

        assert list(con.configuration.keys()) == res

    def test_get_variable(self):
        con = GameConfiguration("D:/py projects/viseng/config/test.txt")
        item = "Gennady"

        res = "Tsidarmyan"

        assert res == con.get_variable(item)

    def test_set_variable(self):
        con = GameConfiguration("D:/py projects/viseng/config/test.txt")
        item = "Gennady"
        var = "G"
        con.set_variable(item, var)

        res = "G"

        assert con[item] == res

    def test_execute(self):
        con = GameConfiguration("D:/py projects/viseng/config/test.txt")
        item = "Gennady"
        var = "G"
        con.set_variable(item, var)
        con.execute_file("D:/py projects/viseng/config/test.txt")

        res = "Tsidarmyan"

        assert con[item] == res

    def test_save(self):
        con = GameConfiguration("D:/py projects/viseng/config/test.txt")
        con.set_variable("Otel", "Eleon")
        con.save("D:/py projects/viseng/config/testw.txt")

        con_new = GameConfiguration("D:/py projects/viseng/config/testw.txt")
        item = "Otel"

        res = "Eleon"

        assert con_new[item] == res


