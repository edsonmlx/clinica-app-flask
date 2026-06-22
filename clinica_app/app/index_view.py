from flask_appbuilder import IndexView, expose


class ClinicaIndexView(IndexView):
    index_template = 'index_clinica.html'

    @expose('/')
    def index(self):
        from app import db
        from app.models import Paciente, Medico, Cita, Consulta, Factura
        import datetime

        total_pacientes = db.session.query(Paciente).count()
        total_medicos = db.session.query(Medico).count()
        total_citas = db.session.query(Cita).count()
        citas_hoy = db.session.query(Cita).filter(
            Cita.fecha == datetime.date.today()
        ).count()
        total_consultas = db.session.query(Consulta).count()
        facturas_pendientes = db.session.query(Factura).filter(
            Factura.estado == 'Pendiente'
        ).count()

        return self.render_template(
            self.index_template,
            total_pacientes=total_pacientes,
            total_medicos=total_medicos,
            total_citas=total_citas,
            citas_hoy=citas_hoy,
            total_consultas=total_consultas,
            facturas_pendientes=facturas_pendientes
        )