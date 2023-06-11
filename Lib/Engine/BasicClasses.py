import Lib.Math.LowLevelMath as llm
import Lib.Exceptions.EngineException as enex
import time
import math
import random

precision = 4


class Ray:
    def __init__(self, cs, initialpt: llm.Point, direction: llm.Vector):
        self.cs = cs
        self.initialpt = initialpt
        self.direction = direction

    def normalize(self):
        return self.direction.norm()


class Identifier:
    identifiers = set()

    def __init__(self, id=None):
        if id is not None:
            self.id = id

        else:
            self.id = self.__generate__()
            while self.id in Identifier.identifiers:
                self.id = self.__generate__()

        Identifier.identifiers.add(self.id)

    @classmethod
    def __generate__(cls):
        timestamp = int(time.time())
        random.seed(timestamp)
        return random.randint(1, 100000)

    def get_value(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id


class Entity:
    def __init__(self, cs: llm.CoordinateSystem):
        self.__dict__["properties"] = set()
        self.cs = cs
        self.id = Identifier()

    def set_property(self, prop: str, value) -> None:
        if prop == "properties":
            raise enex.EngineException(enex.EngineException.NOT_PERMISSION)

        self.__dict__[prop] = value
        self.__dict__["properties"].add(prop)

    def get_property(self, prop: str) -> any:
        if prop == "properties":
            raise enex.EngineException(enex.EngineException.NOT_PERMISSION)

        if prop not in self.__dict__["properties"]:
            raise enex.EngineException(enex.EngineException.NOT_FOUND)

        return self.__dict__[prop]

    def remove_property(self, prop: str) -> None:
        if prop == "properties":
            raise enex.EngineException(enex.EngineException.NOT_PERMISSION)

        if prop not in self.__dict__["properties"]:
            raise enex.EngineException(enex.EngineException.NOT_FOUND)

        self.__delattr__(prop)
        self.__dict__["properties"].remove(prop)

    def __getitem__(self, prop):
        return self.get_property(prop)

    def __getattr__(self, prop):
        return self.get_property(prop)

    def __setitem__(self, prop, value):
        self.set_property(prop, value)

    def __setattr__(self, prop, value):
        self.set_property(prop, value)


class EntityList:
    def __init__(self, entities=None):
        if entities is None:
            entities = []
        self.entities = entities

    def append(self, entity: Entity) -> None:
        self.entities.append(entity)

    def remove(self, entity: Entity) -> None:
        if entity.id not in [i.identifier for i in self.entities]:
            raise enex.EngineException(enex.EngineException.NOT_FOUND)

        self.entities.remove(entity)

    def get(self, iden: Identifier):
        for i in self.entities:
            if i.id.get_value() == iden.get_value():
                return i

        raise enex.EngineException(enex.EngineException.NOT_FOUND)

    def exec(self, f, *args, **kwargs):
        for i in self.entities:
            f(i, *args, **kwargs)

    def __getitem__(self, id: Identifier):
        return self.get(id)


class Game:
    def __init__(self, cs: llm.CoordinateSystem, entities: EntityList):
        self.cs = cs
        self.entities = entities

    def run(self) -> None:
        pass

    def update(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def get_entity(self):
        class GameEntity(Entity):
            def __init__(kself):
                super().__init__(self.cs)

        return GameEntity

    def get_ray_class(self):
        class GameRay(Ray):
            def __init__(kself, initialpt: llm.Point, direction: llm.Vector):
                super().__init__(self.cs, initialpt, direction)

        return GameRay

    def get_object(self):
        class GameObject(self.get_entity()):
            def __init__(self, pos: llm.Point, direction: llm.Vector):
                super().__init__()
                self.set_position(pos)
                self.set_direction(direction)
                self.dim = direction.dim()

            def move(self, direction: llm.Vector):
                self["position"] = self["position"] + direction

            def planar_rotate(self, inds, angle):
                direction = llm.Matrix.get_rotation_matrix(inds, angle, self.dim) * self["direction"].transpose()
                self.set_direction(direction)

            def rotate_3d(self, angles: list):
                direction = llm.Matrix.get_teit_bryan_matrix(angles) * self["direction"].transpose()
                self.set_direction(direction)

            def set_position(self, pos: llm.Point):
                self.set_property("position", pos)

            def set_direction(self, direction: llm.Vector):
                self.set_property("direction", direction)

        return GameObject

    def get_camera(self):
        class GameCamera(self.get_object()):
            def __init__(self, pos: llm.Point, fov: float, drawdist: float, look_at: llm.Point = None,
                         vfov: float = None):
                super().__init__(pos, look_at)

                if vfov is None:
                    vfov = math.atan((16 / 9) * math.tan(math.radians(fov) / 2))
                    self.set_property("vfov", vfov)

                else:
                    self.set_property("vfov", math.radians(vfov))

                self.set_property("fov", math.radians(fov))
                self.set_property("drawdist", drawdist)

                if look_at is not None:
                    self.set_property("look_at", look_at)

            def get_rays_matrix(self, n: int, m: int):
                res = llm.Matrix(n, m)
                alpha, beta = self.fov, self.vfov
                dalpha, dbeta = alpha / n, beta / m

                if self["direction"] is None:
                    direction = llm.Vector(
                        [self["look_at"][i] - self["position"][i] for i in range(len(self["look_at"]))])

                else:
                    direction = self["direction"]

                for i in range(n):
                    ai = dalpha * i - (alpha / 2)
                    for j in range(m):
                        bi = dalpha * i - (beta / 2)
                        pr_direction = llm.Matrix.get_rotation_matrix([0, 1], ai, 3) * llm.Matrix.get_rotation_matrix(
                            [0, 2], bi, 3)
                        pr_direction *= direction.transpose() * (
                                direction.length() ** 2 / direction.scalar_product(pr_direction))
                        res[i][j] = Ray(self.cs, self["position"], pr_direction)

                return res

        return GameCamera

    def HyperPlane(self):
        class GameHyperPlane(self.get_object()):
            def __init(self, pos: llm.Point, normal: llm.Vector) -> None:
                super().__init__(pos, normal)

            def intersection_distance(self, ray: Ray):
                ray_pt = ray.initialpt.transpose()
                ray_dir = ray.direction.transpose()
                abc = self.direction.transpose()
                pos = self.position.transpose()

                if abc % ray_dir == 0:
                    if abc % (ray_pt - pos) == 0:
                        return 0

                    else:
                        raise enex.EngineException("Parallel ray and hyperplane")

                else:
                    t = -(abc % (ray_pt - pos)) / (abc % ray_dir)

                    if t < 0:
                        return -1
                    else:
                        return (ray_dir * t).length()

        return GameHyperPlane

    def HyperEllipsoid(self):
        class GameHyperEllipsoid(self.get_object()):
            def __init__(self, pos: llm.Point, direction: llm.Vector, semiaxes: list[float]):
                super().__init__(pos, direction)
                self.set_property("semiaxes", semiaxes)

            def planar_rotate(self, inds: list, angle: float):
                super().planar_rotate(inds, angle)

            def rotate_3d(self, angles: list):
                super().rotate_3d(angles)

            def intersection_distance(self, ray: Ray):
                ray_pt = ray.initialpt.transpose()  # [[1], [2], [3]]
                ray_dir = ray.direction.transpose()
                ellips_dir = self.direction.transpose()

                A = (ray_dir[0] / ellips_dir[0]) ** 2 + (ray_dir[1] / ellips_dir[1]) ** 2 + (
                            ray_dir[2] / ellips_dir[2]) ** 2
                B = 2 * ((ray_dir[0] * ray_pt[0]) / (ellips_dir[0] ** 2) + (
                        ray_dir[1] * ray_pt[1]) / (ellips_dir[1] ** 2) + (ray_dir[2] * ray_pt[2]) / (
                                 ellips_dir[2] ** 2))
                C = (ray_pt[0] / ellips_dir[0]) ** 2 + (ray_pt[1] / ellips_dir[1]) ** 2 + (
                            ray_pt[2] / ellips_dir[2]) ** 2 - 1

                disc = B ** 2 - 4 * A * C

                if disc < 0:
                    return -1

                else:
                    t1 = (-B + disc ** 0.5) / (2 * A)
                    t2 = (-B - disc ** 0.5) / (2 * A)

                    v1 = ray_dir * t1
                    v2 = ray_dir * t2

                    if t1 > 0 and t2 > 0:
                        return min(v1.length(), v2.length())

                    elif t1 > 0 and t2 <= 0:
                        return v1.length()

                    elif t1 <= 0 and t2 > 0:
                        return v2.length()

                    else:
                        return -1

        return GameHyperEllipsoid


