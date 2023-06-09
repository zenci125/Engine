import Lib.Math.LowLevelMath as mc
import Lib.Exceptions.MathException as ex
import pytest


class TestMatrix:
    def test_init_zero_n(self=None):
        m1 = mc.Matrix(3)

        res = mc.Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        assert res == m1

    def test_init_zero_nm(self=None):
        m1 = mc.Matrix(2, 3)

        res = mc.Matrix([[0, 0, 0], [0, 0, 0]])

        assert res == m1

    def test_init_zero_nm_2(self=None):
        m1 = mc.Matrix(3, 3)

        res = mc.Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        assert res == m1

    def test_add(self=None):
        m1 = mc.Matrix([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
        m2 = mc.Matrix([[1, 2, 3], [4, 5, 6], [-1, 3, 4]])
        m3 = mc.Matrix([[2, 3, 4], [6, 7, 8], [2, 6, 7]])

        res = m1 + m2

        assert res == m3

    def test_add_error(self=None):
        m1 = mc.Matrix([[1, 2, 3]])
        m2 = mc.Matrix([[1, 2], [3, 4]])

        with pytest.raises(ex.MatException):
            m1 + m2

    def test_sub(self=None):
        m1 = mc.Matrix([[1, 2, 3], [1, 1, 1], [7, 8, 9]])
        m2 = mc.Matrix([[10, 11, 5], [5, 6, 7], [16, 17, 18]])
        m3 = mc.Matrix([[9, 9, 2], [4, 5, 6], [9, 9, 9]])

        res = m2 - m1

        assert res == m3

    def test_sub_error(self=None):
        m1 = mc.Matrix([[1, 2, 3]])
        m2 = mc.Matrix([[1, 2], [3, 4]])

        with pytest.raises(ex.MatException):
            m1 - m2

    def test_sub_error_2(self=None):
        m1 = mc.Matrix([[1, 2, 3], [1, 2, 3]])
        m2 = mc.Matrix([[1, 2], [3, 4]])

        with pytest.raises(ex.MatException):
            m1 - m2

    def test_det(self=None):
        m1 = mc.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        det = 0

        assert m1.det() == det

    def test_det_error(self=None):
        m1 = mc.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9], [5, 6, 7]])

        with pytest.raises(ex.MatException):
            m1.det()

    def test_inverse(self):
        m1 = mc.Matrix([[1, 2, 3], [4, 5, 6], [7, 9, 9]])

        res = mc.Matrix([[-1.5, 1.5, -0.5], [1, -2, 1], [0.16666666666666666, 0.8333333333333334, -0.5]])

        assert res == m1.inverse()

    def test_inverse_error_square(self):
        m1 = mc.Matrix([[1, 2, 3], [1, 2, 4]])

        with pytest.raises(ex.MatException):
            m1.inverse()

    def test_inverse_error_det(self):
        m1 = mc.Matrix([[9, 3], [18, 6]])

        with pytest.raises(ex.MatException):
            m1.inverse()

    def test_mul(self=None):
        m1 = mc.Matrix([[1, 2, 3], [3, 2, 1]])
        m2 = mc.Matrix([[4, 5], [6, 7], [8, 9]])
        m3 = mc.Matrix([[40, 46], [32, 38]])

        res = m1 * m2

        assert res == m3

    def test_mul_2(self=None):
        m1 = mc.Matrix([[1], [2], [3]])
        m2 = mc.Matrix([[4]])
        m3 = mc.Matrix([[4], [8], [12]])

        res = m1 * m2

        assert res == m3

    def test_mul_error(self=None):
        m1 = mc.Matrix([[1, 2, 3, 4], [4, 3, 2, 1]])
        m2 = mc.Matrix([[4, 5], [6, 7], [8, 9]])

        with pytest.raises(ex.MatException):
            m1 * m2

    def test_mul_error_type(self=None):
        m1 = mc.Matrix([[1, 2, 3, 4], [4, 3, 2, 1]])
        m2 = mc.Point([4, 5, 6])

        with pytest.raises(ex.MatException):
            m1 * m2

    def test_mul_error_size(self=None):
        m1 = mc.Matrix([[1, 2, 3], [1, 1, 1], [7, 8, 9]])
        m2 = mc.Matrix([[10, 11], [5, 6]])

        with pytest.raises(ex.MatException):
            m1 * m2

    def test_get_minor(self=None):
        m1 = mc.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m2 = mc.Matrix([[5, 6], [8, 9]])

        res = m1.get_minor([0], [0])

        assert res == m2

    def test_get_minor_2(self=None):
        m1 = mc.Matrix([[1, 2], [3, 4]])
        m2 = mc.Matrix([[1]])

        res = m1.get_minor([1], [1])

        assert res == m2

    def test_truediv(self=None):
        m1 = mc.m1 = mc.Matrix([[1, 2, 3], [3, 5, 6], [5, 0, 9]])
        m2 = mc.Matrix([[1, 0, 2], [1, 0, 3], [0, 2, 1]])
        m3 = mc.Matrix([[1, 0, 1], [5.5, -2.5, 2.5], [6, -1, 0]])

        res = m1 / m2

        assert res == m3

    def test_truediv_2(self=None):
        m1 = mc.Matrix([[1, 2], [3, 4]])
        m2 = mc.Matrix([[0.5, 1], [1.5, 2]])

        res = m1 / 2

        assert res == m2

    def test_transpose(self=None):
        m1 = mc.Matrix([[1, 2, 0], [4, 7, 6], [7, 11, 9]])
        m2 = mc.Matrix([[1, 4, 7], [2, 7, 11], [0, 6, 9]])

        res = m1.transpose()

        assert res == m2

    def test_transpose_2(self=None):
        m1 = mc.Matrix([[1, 2, 0], [4, 7, 6]])
        m2 = mc.Matrix([[1, 4], [2, 7], [0, 6]])

        res = m1.transpose()

        assert res == m2

    def test_gram(self=None):
        v1 = mc.Vector([[1], [2], [3]])
        v2 = mc.Vector([[4], [5], [6]])
        v3 = mc.Vector([[7], [8], [9]])
        m1 = mc.Matrix.gram([v1, v2, v3])

        res = mc.Matrix([[14, 32, 50], [32, 77, 122], [50, 122, 194]])

        assert res == m1

    def test_gram_2(self=None):
        v1 = mc.Vector([[3], [4]])
        v2 = mc.Vector([[4], [4]])
        m1 = mc.Matrix.gram([v1, v2])
        res = mc.Matrix([[25, 28], [28, 32]])

        assert res == m1

    def test_identity(self=None):
        m1 = mc.Matrix.identity(2)

        res = mc.Matrix([[1, 0], [0, 1]])

        assert res == m1

    def test_identity_3(self=None):
        m1 = mc.Matrix.identity(3)

        res = mc.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

        assert res == m1

    def test_get_rotation_matrix(self=None):
        m1 = mc.Matrix.get_rotation_matrix([1, 2], 90, 3)
        res = mc.Matrix([[1, 0, 0],
                        [0, 0, -1],
                        [0, 1, 0]])

        assert res == m1

    def test_get_rotation_matrix_1(self=None):
        m1 = mc.Matrix.get_rotation_matrix([1, 2], 0, 3)
        res = mc.Matrix([[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1]])

        assert res == m1

    def test_get_rotation_matrix_inds_error(self=None):
        with pytest.raises(ex.MatException):
            mc.Matrix.get_rotation_matrix([1, 3], 90, 2)

    def test_get_rotation_matrix_inds_error_list(self=None):
        with pytest.raises(ex.MatException):
            mc.Matrix.get_rotation_matrix([1, 3, 4], 90, 5)


class TestVector:
    def test_init_error(self=None):
        with pytest.raises(ex.MatException):
            mc.Vector([[1], [2], [3, 4]])

    def test_init_transposed_or_not(self=None):
        v1 = mc.Vector([[1], [2], [3]])
        v2 = mc.Vector([1, 2, 3])

        res1 = True
        res2 = False

        assert v1.is_col == res1
        assert v2.is_col == res2

    def test_init_zero(self=None):
        v1 = mc.Vector(3)

        res = mc.Vector([0, 0, 0])

        assert res == v1

    def test_length(self=None):
        v1 = mc.Vector([1, 0, 0])

        res = 1

        assert res == v1.length()

    def test_scalar_product_rows(self=None):
        v1 = mc.Vector([[1], [2], [3]])
        v2 = mc.Vector([[4], [5], [6]])
        v = 32

        res = v1 % v2

        assert res == v

    def test_scalar_product(self=None):
        v1 = mc.Vector([[1], [2], [3]])
        v2 = mc.Vector([[4], [5], [6]])
        v = 32

        res = v1 % v2

        assert res == v

    def test_scalar_product_2(self=None):
        v1 = mc.Vector([[1], [0], [3]])
        v2 = mc.Vector([[4], [5], [6]])
        v = 22

        res = v1 % v2

        assert res == v

    def test_vector_product(self=None):
        v1 = mc.Vector([[1], [2], [3]])
        v2 = mc.Vector([[4], [5], [6]])
        v3 = mc.Vector([[-3], [6], [-3]])

        res = v1 ** v2

        assert res == v3

    def test_vector_product_2(self=None):
        v1 = mc.Vector([[1], [2], [3]])
        v2 = mc.Vector([[1], [2], [3]])
        v3 = mc.Vector([[0], [0], [0]])

        res = v1**v2

        assert res == v3

    def test_dim(self=None):
        v1 = mc.Vector([[1, 2, 3]])
        m = 3
        res = v1.dim()

        assert res == m

    def test_dim_2(self=None):
        v1 = mc.Vector([[]])
        m = 0
        res = v1.dim()

        assert res == m


def test_BilinearForm1():
    m = mc.Matrix([[1, 0], [5, 6]])
    v1 = mc.Vector([[1, 2]])
    v2 = mc.Vector([[3, 4]])
    ans = 3

    res = mc.BilinearForm(m, v1, v2)

    assert res == ans


def test_BilinearForm2():
    m = mc.Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 1]])
    v1 = mc.Vector([[1, 2, 4]])
    v2 = mc.Vector([[3, 4, 9]])
    ans = 0

    res = mc.BilinearForm(m, v1, v2)

    assert res == ans


class TestPoint:
    def test_add(self=None):
        p1 = mc.Point([1, 4, 6])
        v1 = mc.Vector([1, 2, 3])
        p2 = mc.Point([2, 6, 9])

        res = p1 + v1

        assert res == p2

    def test_add_2(self=None):
        p1 = mc.Point([[1], [2], [3]])
        v1 = mc.Vector([[7], [6], [4]])
        p2 = mc.Point([[8], [8], [7]])

        res = p1 + v1

        assert res == p2

    def test_sub(self=None):
        p1 = mc.Point([1, 2, 3])
        v1 = mc.Vector([9, 1, 5])
        p2 = mc.Point([-8, 1, -2])

        res = p1 - v1

        assert res == p2

    def test_sub_2(self=None):
        p1 = mc.Point([[0], [0], [0]])
        v1 = mc.Vector([[1], [2], [3]])
        p2 = mc.Point([[-1], [-2], [-3]])

        res = p1 - v1

        assert res == p2


class TestVectorSpace:
    def test_init_err_vectorspace(self=None):
        v1 = mc.Vector([[1], [2], [3]])
        v2 = mc.Matrix([[4], [5], [6]])

        with pytest.raises(ex.MatException):
            mc.VectorSpace([v1, v2])

    def test_scalar_product_basis(self=None):
        v1 = mc.Vector([[1], [0], [3]])
        v2 = mc.Vector([[4], [5], [6]])

        b1 = mc.Vector([[1], [5], [0]])
        b2 = mc.Vector([[2], [2], [3]])
        b3 = mc.Vector([[1], [0], [1]])

        basis = mc.VectorSpace([b1, b2, b3])

        ans = 293
        res = basis.scalar_product(v1, v2)

        assert res == ans

    def test_scalar_product_basis_error(self=None):
        v1 = mc.Vector([[1], [0], [4]])
        v2 = [[4], [5], [6]]

        b1 = mc.Vector([[1], [2], [3]])
        b2 = mc.Vector([[4], [5], [6]])
        b3 = mc.Vector([[7], [8], [9]])

        basis = mc.VectorSpace([b1, b2, b3])

        with pytest.raises(ex.MatException):
            basis.scalar_product(v1, v2)

    def test_vector_product_basis(self=None):
        v1 = mc.Vector([[1], [0], [3]])
        v2 = mc.Vector([[4], [5], [6]])

        b1 = mc.Vector([[1], [0], [0]])
        b2 = mc.Vector([[0], [1], [0]])
        b3 = mc.Vector([[0], [0], [1]])

        basis = mc.VectorSpace([b1, b2, b3])

        ans = mc.Vector([[-15], [6], [5]])
        res = basis.vector_product(v1, v2)

        assert res == ans

    def test_vector_product_basis_1(self=None):
        v1 = mc.Vector([[1], [0]])
        v2 = mc.Vector([[4], [5], [6]])

        b1 = mc.Vector([[1], [0], [0]])
        b2 = mc.Vector([[0], [1], [0]])
        b3 = mc.Vector([[0], [0], [1]])

        basis = mc.VectorSpace([b1, b2, b3])

        with pytest.raises(ex.MatException):
            basis.vector_product(v1, v2)

    def test_vector_product_basis_2(self=None):
        v1 = mc.Vector([[1], [0], [4]])
        v2 = [[4], [5], [6]]

        b1 = mc.Vector([[1], [2], [3]])
        b2 = mc.Vector([[4], [5], [6]])
        b3 = mc.Vector([[7], [8], [9]])

        basis = mc.VectorSpace([b1, b2, b3])

        with pytest.raises(ex.MatException):
            basis.vector_product(v1, v2)
