class Matrix(object):
    """Matrix of math, set a Matrix size or array, get object type of Matrix"""
    def __init__(self, h=0, w=0, mtrx=[]):
        if mtrx:
            self.mtrx, self.h, self.w = mtrx, len(mtrx), len(mtrx[0])
        else:
            self.mtrx, self.h, self.w = [[float(i) for i in input(f'{ j }: ').split()] for j in range(h)], h, w
        if self.h == self.w and self.h > 1:
            self.det = self.__determinant()
        else:
            self.det = None

    def str(self):
        answer = str()
        for i in range(self.h):
            for j in range(self.w):
                if self.mtrx[i][j] >= 0:
                    st = ' ' + str(round(self.mtrx[i][j], 5))
                else:
                    st = str(round(self.mtrx[i][j], 5))
                if len(st) < 8:
                    st += " " * (8 - len(st)) + ","
                answer += (st + "\t")
            answer += '\n'
        return answer

    def add(self, other):
        if self.h != other.h or self.w != other.w:
            raise ValueError('Matrix size must be equal')
        return Matrix(mtrx=[[self.mtrx[j][i] + other.mtrx[j][i] for i in range(self.h)] for j in range(self.w)])

    def sub(self, other):
        if self.h != other.h or self.w != other.w:
            raise ValueError('Matrix size must be equal')
        return Matrix(mtrx=[[self.mtrx[j][i] - other.mtrx[j][i] for i in range(self.h)] for j in range(self.w)])

    def mul(self, other):
        if isinstance(other, Matrix):
            if self.w != other.h:
                raise ValueError("Matrix size not valid")
            else:
                # algorithm multiplication two matrices
                return Matrix(mtrx=[[sum([self.mtrx[i][k] * other.mtrx[k][j] for k in range(0, self.w)])
                                     for j in range(0, other.w)] for i in range(0, self.h)])
        elif isinstance(other, int) or isinstance(other, float):
            return Matrix(mtrx=[[self.mtrx[i][j] * other for j in range(0, self.w)] for i in range(0, self.h)])
        else:
            raise TypeError('type must be int, float or  will be instance Matrix')

    def truediv(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.mul(1 / other)
        else:
            raise TypeError('type must be int or float')

    def pow(self, other):
        if not (isinstance(other, int) or (isinstance(other, float) and other % 1 == 0)):
            raise ValueError('Value must be whole number')
        elif self.det:
            mtrx = Matrix(mtrx=self.mtrx)
            if other < 0:
                mtrx, other = self.__mirror(), other * -1
            if other > 0:
                for i in range(1, int(other)):
                    mtrx = mtrx.mul(mtrx)
                return mtrx
            else:
                return mtrx.mul(mtrx.__mirror())
        else:
            raise ValueError("Determinant doesn't exist or equation zero")

    def transpon(self):
        return Matrix(mtrx=[[self.mtrx[i][j] for i in range(self.h)] for j in range(self.w)])

    def __mirror(self):
        mirror_matrix = Matrix(mtrx=[[(self.__determinant(arr=self.__minor(self.mtrx, i, j))) * (-1)**(j+i)
                          for j in range(0, self.w)] for i in range(self.h)]).transpon().mul(self.det ** (self.h - 3))
        return mirror_matrix.transpon().truediv((mirror_matrix.transpon().mul(self).mtrx[0][0]))

    def __minor(self, arr=[], ln=0, col=0):
        return [[arr[i][j] for j in range(len(arr)) if j != ln] for i in range(len(arr)) if i != col]

    def __determinant(self, arr=[]):
        if not arr:
            arr = self.mtrx
        if len(arr) == 2:
            return arr[0][0] * arr[1][1] - arr[0][1] * arr[1][0]
        else:
            return float(sum(((-1) ** i) * self.__determinant(self.__minor(arr=arr, ln=i)) * arr[0][i] for i in range(len(arr[0]))))


if __name__ == '__main__':
    from random import random
    h = w = 3
    a = Matrix(mtrx=[[random() for i in range(w)] for j in range(h)])
    b = Matrix(mtrx=[[1, 2, 3], [4, 5, 6, ], [9, 8, -2]])
    c = Matrix(mtrx=[[1, 2], [5, 6]])

