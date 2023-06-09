import Lib.Engine.BasicClasses as en
import Lib.Math.LowLevelMath as llm
import Lib.Exceptions.EngineException as enex
import pytest

vs = llm.VectorSpace([llm.Vector([1, 0, 0]), llm.Vector([0, 1, 0]), llm.Vector([0, 0, 1])])
p1 = llm.Point([0, 0, 0])
cs = llm.CoordinateSystem(p1, vs)

v1 = llm.Vector([1, 0, 0])
v2 = llm.Vector([0, 1, 0])
v3 = llm.Vector([0, 0, 1])
vs = llm.VectorSpace([v1, v2, v3])
point = llm.Point([0, 0, 0])


class TestEntity:
    def test_set_property(self):
        entity = en.Entity(llm.CoordinateSystem(point, vs))
        entity.set_property("kek", 1915)
        assert entity["kek"] == 1915

    def test_remove_property_error(self):
        basis = llm.VectorSpace([llm.Vector([1, 0, 0]), llm.Vector([0, 1, 0]), llm.Vector([0, 0, 1])])
        entity = en.Entity(llm.CoordinateSystem(llm.Point([0, 0, 0]), basis))
        prop = "Cringe"

        with pytest.raises(enex.EngineException):
            entity.remove_property(prop)

    def test_get_property(self):
        entity = en.Entity(llm.CoordinateSystem(point, vs))
        entity.set_property("kek", 1915)

        assert entity.get_property("kek") == 1915


class TestsEntitiesList:
    def test_get_entity_error(self):
        basis = llm.VectorSpace([llm.Vector([1, 0, 0]), llm.Vector([0, 1, 0]), llm.Vector([0, 0, 1])])
        cs0 = llm.CoordinateSystem(llm.Point([0, 0, 0]), basis)
        cs1 = llm.CoordinateSystem(llm.Point([1, 1, 1]), basis)

        entity1 = en.Entity(cs0)
        entity2 = en.Entity(cs1)
        enlist = en.EntityList([entity1])

        with pytest.raises(enex.EngineException):
            enlist.get(en.Identifier(entity2))

    def test_get(self):
        entity1 = en.Entity(llm.CoordinateSystem(point, vs))
        entity2 = en.Entity(llm.CoordinateSystem(point, vs))
        entity_list = en.EntityList([entity1, entity2])
        entity1_id = entity1.id

        assert entity_list.get(entity1_id) == entity1


class TestsGameObject:
    def test_move(self):
        entity_list = en.EntityList([en.Entity(cs)])
        game = en.Game(llm.CoordinateSystem(point, vs), entity_list)
        obj = game.get_object()(llm.Point([-1, 2, 3]), llm.Vector([1, 2, 3]))
        obj.move(llm.Vector([1, 1, 1]))

        res = llm.Vector([0, 3, 4])

        assert obj["position"] == res

    def test_planar_rotate(self):
        entity_list = en.EntityList([en.Entity(cs)])
        game = en.Game(llm.CoordinateSystem(point, vs), entity_list)
        obj = game.get_object()(llm.Point([0, 0, 0]), llm.Vector([1, 2, 3]))
        obj.planar_rotate([0, 1], 90)

        res = llm.Vector([[-2], [1], [3]])

        assert obj["direction"] == res

    def test_rotate_3d(self):
        entity_list = en.EntityList([en.Entity(cs)])
        game = en.Game(llm.CoordinateSystem(point, vs), entity_list)
        obj = game.get_object()(llm.Point([1, 1, 1]), llm.Vector([2, 1, 0]))
        obj.rotate_3d([90, 0, 90])

        res = llm.Vector([[-1], [0], [2]])

        assert obj["direction"] == res
