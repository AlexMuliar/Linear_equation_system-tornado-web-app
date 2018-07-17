from tornado.web import RequestHandler
import pymongo as db


class StorageHandler(RequestHandler):
    """Child of tornado.web.RequestHandler
       get() -> Load page with solution from DB by ID
       post() -> Save solution in DB and show page with solution ID"""
    def get(self):
        storage = Storage()
        session = self.get_argument('session')
        if session:
            try:
                solution = storage.get_by_id(session)['solution']
                self.render('pages/result.html', solution=solution, session=session, loaded=True)
            except:
                self.render('pages/result.html', solution="Result don't find, check correct your ID", session=session, loaded=True)
        else:
            self.write("You should input ID of record")

    def post(self):
        storage = Storage()
        session = self.get_argument('session')
        data = self.get_argument('solution')
        if storage.get_by_id(session):
            self.render("pages/id.html", ID='', added=False)
        else:
            storage.insert_solution(session, data)
            self.render("pages/id.html", ID=session, added=True)


class Storage(object):
    """Interface with MongoDB for saving solution
        get_by_id -> get record by ID
        insert_solution -> insert new record(id, data)"""
    def __init__(self):
        self.storage = db.MongoClient("localhost", 27017)["SLE"]["Solution"]

    def get_by_id(self, id):
        return self.storage.find_one({"_id": id})

    def insert_solution(self, id, data):
        self.storage.insert_one({"_id": id, "solution": data})
