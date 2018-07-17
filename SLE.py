from Matrix import Matrix

class SLE(object):
    """Calculating System Linear Equation by Kramer, Iteration, Matrix and Jordan-Gauss method"""
    def __init__(self, eq=[], sol=[]):
        self.equation = Matrix(mtrx=eq).mul(1.0)
        self.solution = Matrix(mtrx=sol).transpon().mul(1.0)
        self.h = self.w = self.equation.h
        self.answer = self.print_eq_system()


    def print_eq_system(self):
        arr = list()
        for i in range(self.h):
            for j in range(self.w-1):
                arr.append(f"{ self.equation.mtrx[i][j] }X<sub>{ i },{ j }</sub> +")
            arr.append(f"X<sub>{ i },{ self.w }</sub>{ self.equation.mtrx[i][self.w-1] } = { self.solution.mtrx[i][0] }\n")
        arr.append('\n')
        return arr

    def kramer(self):
        def special_mtrx(i):
            eq_system = self.equation.transpon()
            eq_system.mtrx[i] = self.solution.transpon().mtrx[0]
            return eq_system.transpon()

        if self.equation.det:
            self.answer = self.print_eq_system()
            return [special_mtrx(i).det / self.equation.det for i in range(self.h)
                    if not self.answer.append("X{} =\t {} / {} = {}\n".format(i, special_mtrx(i).det, self.equation.det,
                                                                              special_mtrx(i).det / self.equation.det))]
        else:
            raise ArithmeticError('Matrix not have determinant or determinant is zero')

    def iter(self, e=0.01):
        def formula(i, b):
            return (self.solution.mtrx[i][0] - my_sum(self.equation.mtrx[i], b, i)) / self.equation.mtrx[i][i]

        def my_sum(a, b, i):
            return sum(a[j] * b[j] for j in range(self.w) if j != i)

        self.answer = self.print_eq_system()
        a = [[0] * self.w]
        for i in range(1, 1000):
            a.append([(formula(j, a[i - 1])) for j in range(self.h)])
            st = str()
            for j in range(self.w):
                st += f"X<sub>{ j+1 }</sub> = { a[i][j] }; "
            self.answer.append(f"Iteration { i }: { st }\n")
            if abs(a[i - 1][0] - a[i][0]) < e:
                return a[i]
        self.answer = "Answer not find\n"
        return []

    def matrix(self):
        def line():
            return '-' * (self.equation.w + 2) * 4 + '\n'

        def symbol(chr):
            return '- - ' * (self.equation.w // 2) + f' { chr } ' + '- - ' * (self.equation.w // 2) + '\n'

        result = (self.equation.pow(-1).mul(self.solution)).transpon()
        self.answer = [
            line(), self.equation.str(), line(),
            symbol('X'),
            line(), self.solution.str(), line(),
            symbol('='),
            line(), result.str(), line()
        ]
        return result.mtrx[0]

    def jordan_gauss(self):
        def list_to_str(arr):
            st = str()
            for i in range(len(arr[:-1])):
                st += f' { str(round(arr[i], 4)) }X<sub>{ i+1 }</sub> +'
            return f'{ st } = { round(arr[-1], 5) }\n'

        self.answer = self.print_eq_system()
        gen_mtrx = [self.equation.mtrx[i] + self.solution.mtrx[i] for i in range(self.h)]
        for n in range(self.h):
            for i in range(0, len(gen_mtrx)):
                if i != n:
                    for j in range(n+1, len(gen_mtrx)+1):
                        self.answer.append(f'X<sub>{ j }, { i }</sub> = ({ round(gen_mtrx[n][n], 4) } * { round(gen_mtrx[i][j], 4) }'
                                           f' - { round(gen_mtrx[n][j], 4) } * { round(gen_mtrx[i][n], 4) }) / { round(gen_mtrx[n][n], 4) }')
                        gen_mtrx[i][j] = (gen_mtrx[n][n] * gen_mtrx[i][j] - gen_mtrx[n][j] * gen_mtrx[i][n]) / gen_mtrx[n][n]
                        self.answer.append(f' = { round(gen_mtrx[i][j], 5) }\n')
            a = [[gen_mtrx[n][i] for i in range(self.w + 1)]]
            mtx = (Matrix(mtrx=a).truediv(gen_mtrx[n][n])).mtrx
            gen_mtrx[n] = [mtx[0][i] for i in range(self.w + 1)]
            for a in range(self.h):
                gen_mtrx[a][n] = 0 if a != n else 1.0
            self.answer.append('\n')
            for ln in Matrix(mtrx=gen_mtrx).mtrx:
                self.answer.append(list_to_str(ln))
            self.answer.append('\n')
        return [gen_mtrx[i][len(gen_mtrx)] for i in range(self.h)]


if __name__ == '__main__':
    a = SLE(eq=[[6, 4, 1], [2, 5, 4], [1, 5, 6]], sol=[[2, 1, 6]])
    print(a.jordan_gauss(), a.answer)
    print(a.matrix(), a.answer)
    print(a.iter(), a.answer)
    print(a.kramer(), a.answer)
    input()
