from flask_appbuilder import ModelView
from flask_appbuilder import aggregate_count
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from . import appbuilder, db
from .models import Especialidad, Medico, Paciente, Cita, Consulta, Receta, Factura


# ===================== VISTAS CRUD =====================

class EspecialidadView(ModelView):
    datamodel = SQLAInterface(Especialidad)
    list_columns = ['nombre', 'descripcion']


class MedicoView(ModelView):
    datamodel = SQLAInterface(Medico)
    list_columns = ['nombre', 'ci', 'telefono', 'especialidad']


class PacienteView(ModelView):
    datamodel = SQLAInterface(Paciente)
    list_columns = ['nombre', 'ci', 'genero', 'telefono']


class CitaView(ModelView):
    datamodel = SQLAInterface(Cita)
    list_columns = ['paciente', 'medico', 'fecha', 'hora', 'estado']
    search_columns = ['paciente', 'medico', 'fecha', 'estado']


class ConsultaView(ModelView):
    datamodel = SQLAInterface(Consulta)
    list_columns = ['cita', 'diagnostico', 'fecha']


class RecetaView(ModelView):
    datamodel = SQLAInterface(Receta)
    list_columns = ['consulta', 'medicamento', 'dosis']


class FacturaView(ModelView):
    datamodel = SQLAInterface(Factura)
    list_columns = ['consulta', 'monto', 'estado']


appbuilder.add_view(EspecialidadView, "Especialidades", icon="fa-folder-open-o", category="Clínica")
appbuilder.add_view(MedicoView, "Médicos", icon="fa-user-md", category="Clínica")
appbuilder.add_view(PacienteView, "Pacientes", icon="fa-user", category="Clínica")
appbuilder.add_view(CitaView, "Citas", icon="fa-calendar", category="Clínica")
appbuilder.add_view(ConsultaView, "Consultas", icon="fa-stethoscope", category="Clínica")
appbuilder.add_view(RecetaView, "Recetas", icon="fa-medkit", category="Clínica")
appbuilder.add_view(FacturaView, "Facturas", icon="fa-money", category="Clínica")


# ===================== GRÁFICAS =====================

class CitaChartView(GroupByChartView):
    datamodel = SQLAInterface(Cita)
    chart_title = 'Citas por Estado'
    definitions = [
        {
            'group': 'estado',
            'series': [(aggregate_count, 'estado')]
        }
    ]


class MedicoChartView(GroupByChartView):
    datamodel = SQLAInterface(Medico)
    chart_title = 'Médicos por Especialidad'
    definitions = [
        {
            'group': 'especialidad',
            'series': [(aggregate_count, 'especialidad')]
        }
    ]


class FacturaChartView(GroupByChartView):
    datamodel = SQLAInterface(Factura)
    chart_title = 'Facturas por Estado'
    definitions = [
        {
            'group': 'estado',
            'series': [(aggregate_count, 'estado')]
        }
    ]


appbuilder.add_view_no_menu(CitaChartView)
appbuilder.add_link("Citas por Estado", href="/citachartview/chart/", icon="fa-bar-chart", category="Reportes")

appbuilder.add_view_no_menu(MedicoChartView)
appbuilder.add_link("Médicos por Especialidad", href="/medicochartview/chart/", icon="fa-bar-chart", category="Reportes")

appbuilder.add_view_no_menu(FacturaChartView)
appbuilder.add_link("Facturas por Estado", href="/facturachartview/chart/", icon="fa-bar-chart", category="Reportes")
