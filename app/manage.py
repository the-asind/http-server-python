from flask_migrate import Migrate
from server import app, db

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
