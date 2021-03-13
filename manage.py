from app.factory import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand
from app.middleware.middlewares import GlobalMiddleware

app = create_app(config_name="DEVELOPMENT")
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    app.wsgi_app = GlobalMiddleware(app.wsgi_app)
    # app.run()
    manager.run()
