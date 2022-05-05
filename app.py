from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
