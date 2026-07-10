from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user

from models import db, Evento



eventos = Blueprint(
    "eventos",
    __name__
)




@eventos.route("/eventos")
def lista():


    eventos = Evento.query.all()


    return render_template(
        "eventos.html",
        eventos=eventos
    )





@eventos.route("/admin/evento/crear", methods=["GET","POST"])
@login_required
def crear():


    if not current_user.administrador:

        return redirect("/")



    if request.method == "POST":


        nuevo = Evento(

            titulo=request.form.get("titulo"),

            descripcion=request.form.get("descripcion"),

            fecha=request.form.get("fecha"),

            hora=request.form.get("hora"),

            lugar=request.form.get("lugar"),

            creador_id=current_user.id

        )


        db.session.add(nuevo)

        db.session.commit()



        flash(
            "Evento creado correctamente.",
            "success"
        )


        return redirect("/eventos")



    return render_template(
        "crear_evento.html"
    )
@eventos.route("/admin/evento/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar(id):

    if not current_user.administrador:
        return redirect("/")


    evento = Evento.query.get_or_404(id)


    db.session.delete(evento)

    db.session.commit()


    flash(
        "Evento eliminado correctamente.",
        "success"
    )


    return redirect("/eventos")