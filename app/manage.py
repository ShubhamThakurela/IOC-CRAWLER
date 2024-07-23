from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_script import Manager
from __init__ import blueprint
from main import create_app

load_dotenv()
app = create_app()
app.register_blueprint(blueprint)
app.app_context().push()
manager = Manager(app)
migrate = Migrate(app)


# host_name = ConstantService.server_host()
@manager.command
def run():
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    manager.run()
