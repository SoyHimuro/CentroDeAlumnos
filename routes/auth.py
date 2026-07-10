from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Usuario



auth = Blueprint(
    "auth",
    __name__
)





# ==========================
# REGISTRO
# ==========================


@auth.route("/registro", methods=["GET","POST"])
def registro():


    if request.method == "POST":


        nombre = request.form.get("nombre")

        correo = request.form.get("correo")

        curso = request.form.get("curso")

        contraseña = request.form.get("contraseña")



        existe = Usuario.query.filter_by(
            correo=correo
        ).first()



        if existe:

            flash(
                "Ese correo ya está registrado.",
                "danger"
            )

            return redirect(
                url_for("auth.registro")
            )



        nuevo_usuario = Usuario(

            nombre=nombre,

            correo=correo,

            curso=curso,

            contraseña=generate_password_hash(
                contraseña
            ),
            rol="Estudiante"
        )

        



        db.session.add(nuevo_usuario)

        db.session.commit()



        flash(
            "Cuenta creada correctamente.",
            "success"
        )


        return redirect(
            url_for("auth.login")
        )



    return render_template(
        "registro.html"
    )







# ==========================
# LOGIN
# ==========================


@auth.route("/login", methods=["GET","POST"])
def login():



    if request.method == "POST":


        correo = request.form.get("correo")

        contraseña = request.form.get("contraseña")



        usuario = Usuario.query.filter_by(
            correo=correo
        ).first()



        if usuario and check_password_hash(
            usuario.contraseña,
            contraseña
        ):


            login_user(usuario)



            flash(
                "Bienvenido nuevamente.",
                "success"
            )


            return redirect("/")



        else:


            flash(
                "Correo o contraseña incorrectos.",
                "danger"
            )



    return render_template(
        "login.html"
    )







# ==========================
# LOGOUT
# ==========================


@auth.route("/logout")
@login_required
def logout():

    logout_user()


    flash(
        "Sesión cerrada.",
        "info"
    )


    return redirect("/")