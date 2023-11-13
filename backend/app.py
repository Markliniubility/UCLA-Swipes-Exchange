import os
from typing import Optional

from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

from monad import option
from routes.order import order_route
from routes.user import User, user_collection, user_route

load_dotenv()


if __name__ == '__main__':
    flask_app = Flask(__name__)
    flask_app.secret_key = option.unwrap_or(os.getenv("FLASK_SECRET_KEY"), "114514_1919810")

    login_manager = LoginManager()
    login_manager.init_app(flask_app)

    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[User]:
        return option.and_then(user_collection.get(ObjectId(user_id)), lambda bson: User.from_bson(bson))

    flask_app.register_blueprint(user_route, url_prefix='/user')
    flask_app.register_blueprint(order_route, url_prefix='/order')
    flask_app.run(debug=True)
