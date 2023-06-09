class EngException(Exception):
    pass


class MatException(EngException):
    WRONG_USAGE = "This operation is not defined for this data"
    WRONG_SIZE = "This operation is not allowed because of different size"
    SQUARE_MATRIX = "This operation does not work on non-square matrices"
    SINGULAR_MATRIX = "This operation is not allowed for singular matrix"
    VECTORSPACE_WRONG_USAGE = "All elements need to be vector"
    POINT_WRONG_USAGE = "This operation is not defined for Point"
    WRONG_INDS = "This opertion is not defined for this indexes"
