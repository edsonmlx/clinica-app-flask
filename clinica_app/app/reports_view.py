from flask_appbuilder import BaseView, expose, has_access
from sqlalchemy import func


class ReportesView(BaseView):
    route_base = "/reportes"
    default_view = "citas_por_medico"

    @expose('/citas-por-medico')
    @has_access
    def citas_por_medico(self):
        from app import db
        from app.models import Cita, Medico

        resultados = (
            db.session.query(Medico.nombre, func.count(Cita.id).label('total'))
            .join(Cita, Cita.medico_id == Medico.id)
            .group_by(Medico.nombre)
            .all()
        )
        return self.render_template(
            'reporte_tabla.html',
            titulo='Reporte: Citas por Médico',
            columnas=['Médico', 'Total de Citas'],
            filas=resultados
        )

    @expose('/pacientes-atendidos')
    @has_access
    def pacientes_atendidos(self):
        from app import db
        from app.models import Paciente, Consulta, Cita

        resultados = (
            db.session.query(Paciente.nombre, func.count(Consulta.id).label('total'))
            .join(Cita, Cita.paciente_id == Paciente.id)
            .join(Consulta, Consulta.cita_id == Cita.id)
            .group_by(Paciente.nombre)
            .all()
        )
        return self.render_template(
            'reporte_tabla.html',
            titulo='Reporte: Pacientes Atendidos (Consultas)',
            columnas=['Paciente', 'Consultas Realizadas'],
            filas=resultados
        )

    @expose('/facturacion')
    @has_access
    def facturacion(self):
        from app import db
        from app.models import Factura

        resultados = (
            db.session.query(Factura.estado, func.count(Factura.id).label('total'), func.sum(Factura.monto).label('monto_total'))
            .group_by(Factura.estado)
            .all()
        )
        return self.render_template(
            'reporte_facturacion.html',
            titulo='Reporte: Facturación por Estado',
            resultados=resultados
        )