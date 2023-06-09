from math import *
import Lib.Exceptions.MathException as ex


class Matrix:
    def __init__(self, item1: (int, list), item2: int = None):
        if item2 is not None:
            if (not (isinstance(item2, int) and isinstance(item1, int))) or item2 == 0 or item1 == 0:
                raise ex.MatException(ex.MatException.WRONG_USAGE)

            self.data = [[0 for _ in range(item2)] for _ in range(item1)]
            self.rows = item1
            self.cols = item2

        elif isinstance(item1, int):
            if item1 == 0:
                raise ex.MatException(ex.MatException.WRONG_USAGE)

            self.data = []
            self.data = [[0 for _ in range(item1)] for _ in range(item1)]
            self.rows = item1
            self.cols = item1

        elif isinstance(item1, list):
            self.data = item1
            self.rows = len(item1)
            cols = len(item1[0])
            for i in range(self.rows):
                if len(item1[i]) != cols:
                    raise ex.MatException(ex.MatException.WRONG_USAGE)
                cols = len(item1[i])

            self.cols = cols

    def addition(self, other: ('Matrix', float)):
        if isinstance(other, (int, float)) and other == 0:
            other = Matrix(self.rows, self.cols)

        if not isinstance(other, Matrix):
            raise ex.MatException(ex.MatException.WRONG_USAGE)

        if not (self.rows == other.rows and self.cols == other.cols):
            raise ex.MatException(ex.MatException.WRONG_SIZE)

        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] += other.data[i][j]
        return self

    def __add__(self, other: (float, 'Matrix')):
        return self.addition(other)

    __radd__ = __add__

    def multiply_by_scalar(self, other: (float, int)):
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] *= other
        return self

    def matrix_multiply(self, other: 'Matrix'):
        if self.cols != other.rows:
            raise ex.MatException(ex.MatException.WRONG_USAGE)

        result = [[0 for _ in range(other.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result[i][j] += round(self.data[i][k] * other.data[k][j], 5)
        return Matrix(result)

    def multiply(self, other: (float, 'Matrix')):
        if isinstance(other, Matrix):
            return self.matrix_multiply(other)

        elif isinstance(other, (int, float)):
            return self.multiply_by_scalar(other)

    def __mul__(self, other):
        return self.multiply(other)

    __rmul__ = __mul__

    def subtraction(self, other):
        return self + (other * (-1))

    def __sub__(self, other):
        return self.subtraction(other)

    def get_minor(self, rowslist: list, colslist: list):
        minor = list()
        for i in range(self.rows):
            if i in rowslist:
                continue

            line = list()
            for j in range(self.rows):
                if j in colslist:
                    continue

                line.append(self.data[i][j])
            minor.append(line)
        return Matrix(minor)

    def det(self):
        n = self.rows
        m = self.cols

        if n != m:
            raise ex.MatException(ex.MatException.SQUARE_MATRIX)

        if n == 1:
            return self.data[0][0]

        result = 0
        for i in range(n):
            submatrix = self.get_minor([0], [i])
            submatrix_det = submatrix.det()
            result += self.data[0][i] * submatrix_det * (-1) ** i
        return result

    def inverse(self):
        if self.rows != self.cols:
            raise ex.MatException(ex.MatException.SQUARE_MATRIX)

        determinant = self.det()
        if determinant == 0:
            raise ex.MatException(ex.MatException.SINGULAR_MATRIX)

        adjugate = [[0] * self.cols for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                sub_matrix = self.get_minor([row], [col])
                sign = (-1) ** (row + col)
                adjugate[col][row] = sign * sub_matrix.det() / determinant
        return Matrix(adjugate)

    def division_by_scalar(self, other: (float, int)):
        return self.__mul__(1 / other)

    def division_by_matrix(self, other: 'Matrix'):
        return self.__mul__(other.inverse())

    def __truediv__(self, other):
        if isinstance(other, Matrix):
            return self.division_by_matrix(other)

        elif isinstance(other, (int, float)):
            return self.division_by_scalar(other)

    def transpose(self):
        transposed_matrix = list()
        for i in range(self.cols):
            temp_row = list()
            for j in range(self.rows):
                temp_row.append(self.data[j][i])
            transposed_matrix.append(temp_row)

        if isinstance(self, Vector):
            return Vector(transposed_matrix)
        else:
            return Matrix(transposed_matrix)

    @classmethod
    def identity(cls, size):
        result = [[0] * size for _ in range(size)]
        for i in range(size):
            result[i][i] = 1

        return cls(result)

    @classmethod
    def gram(cls, vector_list):
        mtrx = list()
        for i in range(len(vector_list)):
            res = list()
            for j in range(len(vector_list)):
                res.append(vector_list[i].scalar_product(vector_list[j]))
            mtrx.append(res)

        return cls(mtrx)

    @classmethod
    def get_rotation_matrix(cls, inds: [int, int], angle, n):
        if not isinstance(inds, list) or len(inds) != 2:
            raise ex.MatException(ex.MatException.WRONG_INDS)

        if inds[0] > n or inds[1] > n:
            raise ex.MatException(ex.MatException.WRONG_INDS)

        angle = angle * pi / 180
        m = cls.identity(n).data
        i = inds[0]
        j = inds[1]

        m[i][i] = round(cos(angle), 5)
        m[i][j] = round(sin(angle) * ((-1) ** (i + j)), 5)
        m[j][i] = round(sin(angle) * (-(-1) ** (i + j)), 5)
        m[j][j] = round(cos(angle), 5)

        if i > j:
            return cls(m).transpose()

        return cls(m)

    @classmethod
    def get_teit_bryan_matrix(cls, angles: list):
        if not isinstance(angles, list):
            raise ex.MatException(ex.MatException.WRONG_USAGE)

        if len(angles) == 1:
            return cls.get_rotation_matrix([1, 2], angles[0], 3) * \
                cls.get_rotation_matrix([0, 2], 0, 3) * \
                cls.get_rotation_matrix([0, 1], 0, 3)

        elif len(angles) == 2:
            return cls.get_rotation_matrix([1, 2], angles[0], 3) * \
                cls.get_rotation_matrix([0, 2], angles[1], 3) * \
                cls.get_rotation_matrix([0, 1], 0, 3)

        elif len(angles) == 3:
            return cls.get_rotation_matrix([1, 2], angles[0], 3) * \
                cls.get_rotation_matrix([0, 2], angles[1], 3) * \
                cls.get_rotation_matrix([0, 1], angles[2], 3)

    def __eq__(self, other):
        return self.data == other.data

    def __getitem__(self, idx):
        return self.data[idx]

    def __str__(self):
        if isinstance(self.data, list):
            return "\n".join(["\t".join([str(val) for val in row]) for row in self.data])


class Vector(Matrix):
    def __init__(self, item1: (list[list], list, int)):
        if isinstance(item1, list) and isinstance(item1, int):
            raise ex.MatException(ex.MatException.WRONG_USAGE)

        if isinstance(item1, list):
            if isinstance(item1[0], list):   # [[1, 2, 3]] or [[1], [2], [3]]
                super().__init__(item1)

            elif isinstance(item1[0], int):  # [1, 2, 3]
                temp = list()
                temp.append(item1)
                super().__init__(temp)

        elif isinstance(item1, int):
            temp = [[0 for _ in range(item1)]]
            super().__init__(temp)            # [[0, 0, 0]]

        self.is_col = (len(self.data[0]) == 1)

    def length(self):
        return (self.scalar_product(self)) ** 0.5

    def scalar_product(self, other):
        if self.is_col != other.is_col:
            raise ex.MatException(ex.MatException.WRONG_USAGE)
        v1 = self
        v2 = other
        if not self.is_col:
            v1 = self.transpose()
        res = BilinearForm(Matrix.identity(v1.rows), v1, v2)
        return res

    def vector_product(self, other):
        if self.is_col != other.is_col:
            raise ex.MatException(ex.MatException.WRONG_USAGE)

        v1 = self
        v2 = other

        if self.is_col:
            v1 = v1.transpose()
            v2 = v2.transpose()

        b1 = Vector([[1], [0], [0]])
        b2 = Vector([[0], [1], [0]])
        b3 = Vector([[0], [0], [1]])

        mat = Matrix([[b1, b2, b3],
                      v1.data[0],
                      v2.data[0]])

        res = mat.det()
        return res

    def dim(self):
        if self.is_col:
            return len(self.data)
        return len(self.data[0])

    def norm(self):
        return self/self.length()

    def __mod__(self, other):
        return self.scalar_product(other)

    def __pow__(self, other):
        return self.vector_product(other)

    def __getitem__(self, idx):
        vec = self
        if self.is_col:
            vec = vec.transpose()
        return vec.data[0][idx]

    def __str__(self):
        return "\n".join(["\t".join([str(val) for val in row]) for row in self.data])


def BilinearForm(mtrx, v1, v2):
    result = 0
    if not v2.is_col:
        v2 = v2.transpose()

    for i in range(len(v1.data)):
        for j in range(len(v2.data)):
            result += mtrx.data[i][j] * v1.data[i][0] * v2.data[j][0]
    return result


class Point(Vector):
    def __inti__(self, val):
        if isinstance(val, Vector):
            super().__init__(val.data)
        else:
            super().__init__(val)

    def __add__(self, vector: Vector):
        if not isinstance(vector, Vector):
            raise ex.MatException(ex.MatException.WRONG_USAGE)

        return Point(super().__add__(vector).data)

    def __sub__(self, vector):
        if not isinstance(vector, Vector):
            raise ex.MatException(ex.MatException.WRONG_USAGE)

        return Point(super().__sub__(vector).data)


class VectorSpace:
    def __init__(self, vector_list):
        size = len(vector_list)
        for vec in vector_list:
            if not isinstance(vec, Point) and isinstance(vec, Vector):
                if vec.dim() != size:
                    raise ex.MatException(ex.MatException.WRONG_SIZE)

        self.vector_list = vector_list

    def scalar_product(self, v1, v2):
        if not (isinstance(v1, Vector) and isinstance(v2, Vector)):
            raise ex.MatException(ex.MatException.WRONG_USAGE)

        if v1.is_col != v2.is_col:
            raise ex.MatException(ex.MatException.WRONG_USAGE)

        if v1.is_col != v2.is_col:
            raise ex.MatException(ex.MatException.WRONG_USAGE)

        return (v1.transpose() * Matrix.gram(self.vector_list) * v2)[0][0]

    def vector_product(self, v1, v2):
        if not (isinstance(v1, Vector) and isinstance(v2, Vector)):
            raise ex.MatException(ex.MatException.WRONG_USAGE)

        if v1.is_col != v2.is_col:
            raise ex.MatException(ex.MatException.WRONG_USAGE)

        vec1 = v1
        vec2 = v2
        if v1.is_col:
            vec1 = vec1.transpose()
            vec2 = vec2.transpose()

        b1 = self.vector_list[1].vector_product(self.vector_list[2])
        b2 = self.vector_list[2].vector_product(self.vector_list[0])
        b3 = self.vector_list[0].vector_product(self.vector_list[1])

        mat = Matrix([[b1, b2, b3],
                      vec1.data[0],
                      vec2.data[0]])

        return mat.det()


class CoordinateSystem:
    def __init__(self, initial_point: Point, vs: VectorSpace):
        self.initial_point = initial_point
        self.vs = vs
