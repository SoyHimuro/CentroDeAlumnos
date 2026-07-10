from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user

from models import (
    Sugerencia,
    Noticia,
    Evento,
    Notificacion
)


main = Blueprint(
    "main",
    __name__
)



@main.route("/")
def inicio():


    noticias = (
        Noticia.query
        .order_by(Noticia.fecha.desc())
        .limit(3)
        .all()
    )


    eventos = (
        Evento.query
        .order_by(Evento.fecha.asc())
        .limit(3)
        .all()
    )


    cantidad_sugerencias = (
        Sugerencia.query.count()
    )


    return render_template(
        "index.html",
        noticias=noticias,
        eventos=eventos,
        cantidad_sugerencias=cantidad_sugerencias
    )





# ==========================
# PERFIL DE USUARIO
# ==========================

@main.route("/perfil")
@login_required
def perfil():

    mis_sugerencias = (
        Sugerencia.query
        .filter_by(usuario_id=current_user.id)
        .order_by(Sugerencia.fecha.desc())
        .all()
    )


    return render_template(
        "perfil.html",
        usuario=current_user,
        sugerencias=mis_sugerencias
    )
# ==========================
# EDITAR PERFIL
# ==========================

@main.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():


    if request.method == "POST":


        nombre = request.form.get("nombre")

        curso = request.form.get("curso")


        current_user.nombre = nombre

        current_user.curso = curso



        foto = request.files.get("foto")


        if foto and foto.filename:


            nombre_foto = foto.filename


            foto.save(
                "static/uploads/" + nombre_foto
            )


            current_user.foto = nombre_foto



        from models import db

        db.session.commit()



        flash(
            "Perfil actualizado correctamente.",
            "success"
        )


        return redirect("/perfil")



    return render_template(
        "editar_perfil.html",
        usuario=current_user
    )
# ==========================
# NOTIFICACIONES
# ==========================

@main.route("/notificaciones")
@login_required
def notificaciones():


    lista = (
        Notificacion.query
        .filter_by(usuario_id=current_user.id)
        .order_by(Notificacion.fecha.desc())
        .all()
    )


    return render_template(
        "notificaciones.html",
        notificaciones=lista
    )
@main.route("/centro")
def centro():

    return render_template(
        "centro.html"
    )
@main.route("/propuestas")
def propuestas():

    return render_template(
        "propuestas.html"
    )