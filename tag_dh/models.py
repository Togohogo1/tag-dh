from tag_dh import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'<Task: {self.name}>'

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Text(), nullable=False)
    pass = db.Column(db.Text(), nullable=False)
