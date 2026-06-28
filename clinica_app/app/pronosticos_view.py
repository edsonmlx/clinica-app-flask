from flask_appbuilder import BaseView, expose, has_access
from openai import OpenAI


class PronosticosView(BaseView):
    route_base = "/pronosticos"
    default_view = "citas"

    def _generar_pronosticos(self, contexto, datos):
        from flask import current_app

        client = OpenAI(
            api_key=current_app.config['GROQ_API_KEY'],
            base_url="https://api.groq.com/openai/v1"
        )

        prompt = f"""
        Eres un analista de datos para una clinica medica.
        Contexto: {contexto}
        Datos actuales: {datos}

        Genera EXACTAMENTE 3 pronosticos breves (maximo 2 lineas cada uno)
        sobre el futuro comportamiento de estos datos en la clinica.
        Numera cada pronostico del 1 al 3. No agregues introduccion ni conclusion.
        """
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            texto = response.choices[0].message.content

            import re
            partes = re.split(r'\n?\s*\d+[\.\)]\s*', texto)
            pronosticos = [p.strip() for p in partes if p.strip()]
            return pronosticos[:3] if len(pronosticos) >= 3 else [texto]
        except Exception as e:
            return [f"Error generando pronostico: {str(e)}"]
        
    @expose('/citas')
    @has_access
    def citas(self):
        from app import db
        from app.models import Cita
        from sqlalchemy import func

        datos = db.session.query(Cita.estado, func.count(Cita.id)).group_by(Cita.estado).all()
        contexto = "Distribucion de citas medicas por estado (Pendiente, Confirmada, Cancelada, etc.)"
        pronostico = self._generar_pronosticos(contexto, datos)

        return self.render_template(
            'pronostico.html',
            titulo='Pronosticos: Citas por Estado',
            pronostico=pronostico
        )

    @expose('/medicos')
    @has_access
    def medicos(self):
        from app import db
        from app.models import Medico, Especialidad
        from sqlalchemy import func

        datos = (
            db.session.query(Especialidad.nombre, func.count(Medico.id))
            .join(Medico, Medico.especialidad_id == Especialidad.id)
            .group_by(Especialidad.nombre)
            .all()
        )
        contexto = "Cantidad de medicos disponibles por especialidad en la clinica"
        pronostico = self._generar_pronosticos(contexto, datos)

        return self.render_template(
            'pronostico.html',
            titulo='Pronosticos: Medicos por Especialidad',
            pronostico=pronostico
        )

    @expose('/facturas')
    @has_access
    def facturas(self):
        from app import db
        from app.models import Factura
        from sqlalchemy import func

        datos = db.session.query(Factura.estado, func.count(Factura.id), func.sum(Factura.monto)).group_by(Factura.estado).all()
        contexto = "Estado de facturacion (pagado/pendiente) y montos totales de la clinica"
        pronostico = self._generar_pronosticos(contexto, datos)

        return self.render_template(
            'pronostico.html',
            titulo='Pronosticos: Facturacion',
            pronostico=pronostico
        )