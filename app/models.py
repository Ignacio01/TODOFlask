from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(20000))
    done = db.Column(db.Boolean)

    def __repr__(self):
        return 'List {}'.format(self.title)
