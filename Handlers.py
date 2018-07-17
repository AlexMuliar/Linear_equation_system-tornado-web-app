from tornado.web import RequestHandler, UIModule
from SLE import SLE
from uuid import uuid4

MAX_SIZE = 12


class MainHandler(RequestHandler):
    """Child of tornado.web.RequestHandler
       get() -> Load start page
       post() -> Show calculating result
       get_matrix() -> Obtaining a matrix from a form
       get_solution -> Obtaining solution by matrix"""
    def get(self):
        self.render('pages/index.html', range=range(2, MAX_SIZE+1), session=uuid4())

    def post(self):
        data = self.get_solution()
        session = self.get_argument("session")
        solution = str()
        for i in data[1]:
            solution += str(i).replace('\n', '<br>')
        for i in range(len(data[0])):
            solution += f"X<sub>{ i+1 }</sub> = { data[0][i] }<br>"
        self.render('pages/result.html', solution=solution, session=session, loaded=False)

    def get_matrix(self, size):
        return ([[float(self.get_argument(f'[{ i }][{ j }]')) for j in range(size)] for i in range(size)],
                [[float(self.get_argument(f'[{ i }][{ size }]')) for i in range(size)]])

    def get_solution(self):
        matrix = self.get_matrix(int(self.get_argument('size')))
        data = SLE(eq=matrix[0], sol=matrix[1])
        method = self.get_argument('method')
        if method == 'iter':
            return (data.iter(float(self.get_argument("accuracy"))) , data.answer)
        elif method == 'kramer':
            return (data.kramer(), data.answer)
        elif method == 'gauss':
            return (data.jordan_gauss(), data.answer)
        else:
            return (data.matrix(), data.answer)


class SolutionModule(UIModule):
    """Child of tornado.web.UIModule
        Method render(str) do render input data(str -> html)"""
    def render(self, solution):
        return solution
