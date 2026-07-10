from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user

from models import db, Sugerencia, Usuario, Noticia, Evento, Notificacion


admin = Blueprint(
    "admin",
    __name__
)

# ==========================
# CAMBIAR ROL DE USUARIO
# ==========================

@admin.route("/admin/usuario/<int:id>/rol", methods=["POST"])
@login_required
def cambiar_rol(id):

    if not current_user.administrador:
        return redirect("/")

    usuario = Usuario.query.get_or_404(id)

    usuario.administrador = not usuario.administrador

    if usuario.administrador:
        usuario.rol = "Administrador"
    else:
        usuario.rol = "Estudiante"

    db.session.commit()

    flash(
        "Rol actualizado correctamente.",
        "success"
    )

    return redirect(
        url_for("admin.usuarios")
    )
# ==========================
# ELIMINAR USUARIO
# ==========================

@admin.route("/admin/usuario/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_usuario(id):

    if not current_user.administrador:
        return redirect("/")


    usuario = Usuario.query.get_or_404(id)


    # Evitar que el admin se elimine a sí mismo
    if usuario.id == current_user.id:

        flash(
            "No puedes eliminar tu propia cuenta.",
            "danger"
        )

        return redirect(
            url_for("admin.usuarios")
        )


    db.session.delete(usuario)

    db.session.commit()


    flash(
        "Usuario eliminado correctamente.",
        "success"
    )


    return redirect(
        url_for("admin.usuarios")
    )

# ==========================
# PANEL ADMIN
# ==========================

@admin.route("/admin/")
@admin.route("/admin")
@login_required
def panel():

    if not current_user.administrador:

        flash(
            "No tienes permisos para entrar.",
            "danger"
        )

        return redirect("/")

    usuarios = Usuario.query.count()

    sugerencias = Sugerencia.query.order_by(
        Sugerencia.fecha.desc()
    ).all()

    total_sugerencias = Sugerencia.query.count()

    aprobadas = Sugerencia.query.filter_by(
        estado="Aprobada"
    ).count()

    pendientes = Sugerencia.query.filter_by(
        estado="Pendiente"
    ).count()

    rechazadas = Sugerencia.query.filter_by(
        estado="Rechazada"
    ).count()

    total_noticias = Noticia.query.count()

    ultimos_usuarios = Usuario.query.order_by(  
        Usuario.fecha_registro.desc()
    ).limit(5).all()

    ultimas_noticias = Noticia.query.order_by(
        Noticia.fecha.desc()
    ).limit(5).all()

    ultimos_eventos = Evento.query.limit(5).all()

    total_eventos = Evento.query.count()

    datos_grafico = {
        "aprobadas": aprobadas,
        "pendientes": pendientes,
        "rechazadas": rechazadas
    }

    return render_template(
        "admin.html",
        usuarios=usuarios,
        sugerencias=sugerencias,
        total_sugerencias=total_sugerencias,
        aprobadas=aprobadas,
        pendientes=pendientes,
        rechazadas=rechazadas,
        total_noticias=total_noticias,
        total_eventos=total_eventos,
        ultimos_usuarios=ultimos_usuarios,
        ultimas_noticias=ultimas_noticias,
        ultimos_eventos=ultimos_eventos,
        datos_grafico=datos_grafico
    )



@admin.route("/admin/usuarios")
@admin.route("/admin/usuarios/")
@login_required
def usuarios():

    if not current_user.administrador:

        flash(
            "No tienes permisos para entrar.",
            "danger"
        )

        return redirect("/")

    lista_usuarios = Usuario.query.all()

    return render_template(
        "admin/usuarios.html",
        usuarios=lista_usuarios
    )


# ==========================
# CAMBIAR ESTADO
# ==========================

@admin.route("/admin/sugerencia/<int:id>/estado", methods=["POST"])
@login_required
def cambiar_estado(id):

    if not current_user.administrador:
        return redirect("/")


    sugerencia = Sugerencia.query.get_or_404(id)


    nuevo_estado = request.form.get("estado")


    sugerencia.estado = nuevo_estado



    notificacion = Notificacion(
        mensaje=f"Tu sugerencia '{sugerencia.titulo}' fue {nuevo_estado.lower()}.",
        usuario_id=sugerencia.usuario_id
    )


    db.session.add(notificacion)


    db.session.commit()


    flash(
        "Estado actualizado correctamente.",
        "success"
    )


    return redirect(
        url_for("admin.panel")
    )
# ==========================
# ELIMINAR SUGERENCIA
# ==========================


@admin.route("/admin/sugerencia/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_sugerencia(id):

    print("LLEGÓ A ELIMINAR:", id)

    sugerencia = Sugerencia.query.get_or_404(id)

    print("ENCONTRADA:", sugerencia.titulo)

    db.session.delete(sugerencia)
    db.session.commit()

    print("BORRADA")

    flash("Sugerencia eliminada correctamente", "success")

    return redirect(url_for("admin.panel"))