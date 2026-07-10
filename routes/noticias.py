from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user

from models import db, Noticia


noticias = Blueprint(
    "noticias",
    __name__
)


@noticias.route("/noticias")
def lista():

    todas = Noticia.query.order_by(
        Noticia.fecha.desc()
    ).all()


    return render_template(
        "noticias.html",
        noticias=todas
    )



@noticias.route("/admin/noticia/crear", methods=["GET","POST"])
@login_required
def crear():

    if not current_user.administrador:
        return redirect("/")


    if request.method == "POST":


        nueva = Noticia(

            titulo=request.form.get("titulo"),

            contenido=request.form.get("contenido"),

            usuario_id=current_user.id

        )


        db.session.add(nueva)

        db.session.commit()


        flash(
            "Noticia publicada correctamente.",
            "success"
        )


        return redirect("/noticias")


    return render_template(
        "crear_noticia.html"
    )
@noticias.route("/admin/noticia/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar(id):

    if not current_user.administrador:
        return redirect("/")


    noticia = Noticia.query.get_or_404(id)


    db.session.delete(noticia)

    db.session.commit()


    flash(
        "Noticia eliminada correctamente.",
        "success"
    )


    return redirect("/noticias")