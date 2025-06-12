from .base import Base

from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, Table, DateTime, Boolean,
    CheckConstraint
)
from sqlalchemy.orm import relationship, validates


# tabla para jugadores inscritos a torneos en las categorías
inscripcion = Table("inscripcion", Base.metadata,
    Column("jugador_id", ForeignKey("jugador.id"), primary_key=True),
    Column("torneo_id", ForeignKey("torneo.id"), primary_key=True),
    Column("categoria_id", ForeignKey("categoria.id"), primary_key=True)
)

# parejas de jugadores
equipo_dobles = Table("equipo_dobles", Base.metadata,
    Column("jugador1_id", ForeignKey("jugador.id"), primary_key=True),
    Column("jugador2_id", ForeignKey("jugador.id"), primary_key=True)
)

class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    edad_min = Column(Integer, nullable=False)
    edad_max = Column(Integer, nullable=False)
    genero = Column(String, nullable=False)  # "M" o "F"
    sets_por_partido = Column(Integer, nullable=False)
    puntos_por_set = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("edad_min <= edad_max"),
        CheckConstraint("sets_por_partido > 0"),
        CheckConstraint("puntos_por_set > 0"),
    )

class Asociacion(Base):
    __tablename__ = "asociacion"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    pais = Column(String, nullable=False)

class Jugador(Base):
    __tablename__ = "jugador"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    genero = Column(String, nullable=False)  # "M" o "F"
    ciudad = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    asociacion_id = Column(Integer, ForeignKey("asociacion.id"), nullable=True)

    asociacion = relationship("Asociacion", backref="jugadores")
    categorias = relationship("Categoria", secondary=inscripcion, backref="jugadores")
    torneos = relationship("Torneo", secondary=inscripcion, backref="jugadores")

class Torneo(Base):
    __tablename__ = "torneo"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    mesas_disponibles = Column(Integer, nullable=False)

class Partido(Base):
    __tablename__ = "partido"
    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)  # "individual" o "dobles"
    torneo_id = Column(Integer, ForeignKey("torneo.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    horario = Column(DateTime, nullable=False)
    mesa = Column(Integer, nullable=False)
    ronda = Column(String, nullable=True)  # Ej: "Octavos", "Final"
    bye = Column(Boolean, default=False)

    torneo = relationship("Torneo", backref="partidos")
    categoria = relationship("Categoria")

class ResultadoSet(Base):
    __tablename__ = "resultado_set"
    id = Column(Integer, primary_key=True)
    partido_id = Column(Integer, ForeignKey("partido.id"), nullable=False)
    numero_set = Column(Integer, nullable=False)
    puntos_jugador1 = Column(Integer, nullable=False)
    puntos_jugador2 = Column(Integer, nullable=False)

    partido = relationship("Partido", backref="resultados")

    __table_args__ = (
        CheckConstraint("puntos_jugador1 >= 0"),
        CheckConstraint("puntos_jugador2 >= 0"),
    )
