import Lib.Math.LowLevelMath as llm
import Lib.Engine.BasicClasses as en


class GameCanvas:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.distances = llm.Matrix(n, m)

    def draw(self):
        pass

    def update(self, camera):
        self.distances = camera.get_rays_matrix(self.n, self.m)

class GameConsole(GameCanvas):
    charmap = ".:; > <+r* zsvfwqkP694VOGbUAKXH8RD # $B0MNWQ %&@"

    def draw(self):
        pass
