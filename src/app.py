from flask import Flask, render_template, request, redirect, url_for, current_app
from board_repository import BoardRepository
from to_do_items_view_model import ToDoItemsViewModel
from flask_login import LoginManager, login_required, login_user, current_user
from flask_principal import Principal, Permission, RoleNeed, identity_changed, Identity, identity_loaded, UserNeed
from app_user import AppUser
from auth_provider import AuthProvider
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = "some_key"

    board_repository = BoardRepository()
    auth_provider = AuthProvider()
    login_manager = LoginManager()

    auth_is_disabled = os.environ['AUTHENTICATION_DISABLED'] == 'True'
    app.config['LOGIN_DISABLED'] = auth_is_disabled

    Principal(app)
    reader_permission = Permission(RoleNeed(AuthProvider.READER_ROLE))
    writer_permission = Permission(RoleNeed(AuthProvider.WRITER_ROLE))

    def authorise(permission_decorator):
        return lambda func: func if auth_is_disabled else permission_decorator(func)

    def get_user_roles():
        return current_user.roles if not auth_is_disabled else AuthProvider.ALL_ROLES

    @app.route('/')
    @login_required
    @authorise(reader_permission.require(http_exception=403))
    def index():
        to_do_items = sorted(board_repository.get_items(), key=lambda item: item.status, reverse=True)
        view_model = ToDoItemsViewModel(user_roles=get_user_roles(), items=to_do_items)
        return render_template('index.html', view_model=view_model)

    @app.route('/', methods=['POST'])
    @login_required
    @authorise(writer_permission.require(http_exception=403))
    def add():
        board_repository.add_item(request.form['title'])
        return redirect(url_for('index'))

    @app.route('/complete_item', methods=['GET'])
    @authorise(writer_permission.require(http_exception=403))
    @login_required
    def complete_item():
        board_repository.complete_item(request.args.get('id'))
        return redirect(url_for('index'))

    @app.route('/delete_item', methods=['GET'])
    @authorise(writer_permission.require(http_exception=403))
    @login_required
    def delete_item():
        board_repository.delete_item(request.args.get('id'))
        return redirect(url_for('index'))

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(auth_provider.get_login_redirect_uri())

    @app.route('/login/callback', methods=['GET'])
    def login_callback():
        user = auth_provider.get_authenticated_user(request.args.get('code'))
        login_user(user)

        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

        return redirect(url_for('index'))

    @login_manager.user_loader
    def load_user(user_id):
        return auth_provider.get_user(user_id)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user

        identity.provides.add(UserNeed(current_user.id))
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role))

    login_manager.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()