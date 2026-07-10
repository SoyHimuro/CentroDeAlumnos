from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user

from models import db, Sugerencia, Apoyo, Comentario


sugerencias = Blueprint(
    "sugerencias",
    __name__
)


# ==========================
# LISTAR SUGERENCIAS
# ==========================

@sugerencias.route("/sugerencias")
def lista():

    todas = (
        Sugerencia.query
        .order_by(Sugerencia.fecha.desc())
        .all()
    )

    return render_template(
        "sugerencias.html",
        sugerencias=todas
    )



# ==========================
# CREAR SUGERENCIA
# ==========================

@sugerencias.route("/sugerencias/crear", methods=["GET", "POST"])
@login_required
def crear():

    if request.method == "POST":

        titulo = request.form.get("titulo")

        descripcion = request.form.get("descripcion")

        categoria = request.form.get("categoria")


        nueva = Sugerencia(

            titulo=titulo,

            descripcion=descripcion,

            categoria=categoria,

            usuario_id=current_user.id

        )


        db.session.add(nueva)

        db.session.commit()


        flash(
            "Tu sugerencia fue enviada correctamente.",
            "success"
        )


        return redirect(
            url_for("sugerencias.lista")
        )


    return render_template(
        "crear_sugerencia.html"
    )



# ==========================
# DETALLE DE SUGERENCIA
# ==========================

@sugerencias.route("/sugerencias/<int:id>")
def detalle(id):

    sugerencia = Sugerencia.query.get_or_404(id)


    sugerencia.vistas += 1

    db.session.commit()


    return render_template(
        "detalle_sugerencia.html",
        sugerencia=sugerencia
    )



# ==========================
# DAR APOYO
# ==========================

@sugerencias.route("/sugerencias/<int:id>/apoyar")
@login_required
def apoyar(id):

    sugerencia = Sugerencia.query.get_or_404(id)


    existe = Apoyo.query.filter_by(

        usuario_id=current_user.id,

        sugerencia_id=id

    ).first()



    if existe:

        db.session.delete(existe)

        flash(
            "Quitaste tu apoyo.",
            "info"
        )


    else:

        apoyo = Apoyo(

            usuario_id=current_user.id,

            sugerencia_id=id

        )


        db.session.add(apoyo)


        flash(
            "Apoyaste esta propuesta ❤️",
            "success"
        )


    db.session.commit()


    return redirect(
        url_for(
            "sugerencias.detalle",
            id=id
        )
    )



# ==========================
# COMENTAR
# ==========================

@sugerencias.route(
    "/sugerencias/<int:id>/comentar",
    methods=["POST"]
)
@login_required
def comentar(id):

    texto = request.form.get("comentario")


    nuevo_comentario = Comentario(

        contenido=texto,

        usuario_id=current_user.id,

        sugerencia_id=id

    )


    db.session.add(nuevo_comentario)


    db.session.commit()


    flash(
        "Comentario agregado.",
        "success"
    )


    return redirect(
        url_for(
            "sugerencias.detalle",
            id=id
        )
    )