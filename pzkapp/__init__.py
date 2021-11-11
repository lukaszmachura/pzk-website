import os
from flask import Flask, render_template


def create_app(test_config=None):
    '''Create and configure the app'''

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='pzk',
        DATABASE=os.path.join(app.instance_path, 'pzkapp.sqlite'),
        )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_found(error):
        return "!404!"

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    # app.add_url_rule('/', endpoint='login')

    from . import member
    app.register_blueprint(member.bp)
    # app.add_url_rule('/', endpoint='index')

    return app
