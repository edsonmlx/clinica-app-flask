from app import db
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Float, Text
from sqlalchemy.orm import relationship


class Especialidad(db.Model):
    __tablename__ = 'especialidad'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(200))

    def __repr__(self):
        return self.nombre

    def __lt__(self, other):
        return self.nombre < other.nombre


class Medico(db.Model):
    __tablename__ = 'medico'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    ci = Column(String(20))
    telefono = Column(String(20))
    especialidad_id = Column(Integer, ForeignKey('especialidad.id'))
    especialidad = relationship('Especialidad')

    def __repr__(self):
        return self.nombre


class Paciente(db.Model):
    __tablename__ = 'paciente'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    ci = Column(String(20))
    fecha_nacimiento = Column(Date)
    genero = Column(String(10))
    telefono = Column(String(20))
    direccion = Column(String(200))

    def __repr__(self):
        return self.nombre


class Cita(db.Model):
    __tablename__ = 'cita'
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('paciente.id'))
    medico_id = Column(Integer, ForeignKey('medico.id'))
    paciente = relationship('Paciente')
    medico = relationship('Medico')
    fecha = Column(Date, nullable=False)
    hora = Column(String(10))
    estado = Column(String(20), default='Pendiente')

    def __repr__(self):
        return f"Cita {self.id} - {self.paciente}"


class Consulta(db.Model):
    __tablename__ = 'consulta'
    id = Column(Integer, primary_key=True)
    cita_id = Column(Integer, ForeignKey('cita.id'))
    cita = relationship('Cita')
    diagnostico = Column(Text)
    observaciones = Column(Text)
    fecha = Column(Date)

    def __repr__(self):
        return f"Consulta {self.id}"


class Receta(db.Model):
    __tablename__ = 'receta'
    id = Column(Integer, primary_key=True)
    consulta_id = Column(Integer, ForeignKey('consulta.id'))
    consulta = relationship('Consulta')
    medicamento = Column(String(100))
    dosis = Column(String(100))
    duracion = Column(String(50))

    def __repr__(self):
        return self.medicamento


class Factura(db.Model):
    __tablename__ = 'factura'
    id = Column(Integer, primary_key=True)
    consulta_id = Column(Integer, ForeignKey('consulta.id'))
    consulta = relationship('Consulta')
    monto = Column(Float)
    fecha_pago = Column(Date)
    estado = Column(String(20), default='Pendiente')

    def __repr__(self):
        return f"Factura {self.id}"