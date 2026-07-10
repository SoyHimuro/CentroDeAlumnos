from flask import Flask, render_template
from flask_login import LoginManager

from config import Config
from models import db, Usuario


# ==========================
# CREAR APP
# ==========================

app = Flask(__name__)

app.config.from_object(Config)


# ==========================
# BASE DE DATOS
# ==========================

db.init_app(app)



# ==========================
# LOGIN
# ==========================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"



@login_manager.user_loader
def cargar_usuario(id_usuario):

    return Usuario.query.get(int(id_usuario))



# ==========================
# RUTAS
# ==========================

from routes.main import main
from routes.auth import auth
from routes.admin import admin
from routes.sugerencias import sugerencias
from routes.noticias import noticias
from routes.eventos import eventos

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(sugerencias)
app.register_blueprint(noticias)
app.register_blueprint(eventos)


# ==========================
# CREAR TABLAS
# ==========================

with app.app_context():

    db.create_all()



# ==========================
# EJECUTAR
# ==========================

print(app.url_map)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Run the app in debug mode on all interfaces at port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)