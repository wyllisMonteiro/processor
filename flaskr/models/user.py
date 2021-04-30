from flaskr import database

class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), unique=True, nullable=False)
    password = database.Column(database.String(255), nullable=False)
    role = database.Column(database.Integer, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def get_password(self):
        return self.password