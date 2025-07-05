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

# NOTA IMPORTANTE: La definición de 'equipo_dobles' como objeto Table ha sido eliminada.
# La clase declarativa 'EquipoDobles(Base)' es la forma correcta de definirla.
# Si esta sección estaba descomentada, causaba el error "Table 'equipo_dobles' is already defined".

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

    posicion_llave = Column(Integer, nullable=True)  
    partido_ganador_id = Column(Integer, ForeignKey("partido.id"), nullable=True)  # siguiente partido al que avanza el ganador
    partido_ganador = relationship("Partido", remote_side=[id])

    # Para individuales
    jugador1_id = Column(Integer, ForeignKey("jugador.id"), nullable=True)
    jugador2_id = Column(Integer, ForeignKey("jugador.id"), nullable=True)

    # Para dobles
    equipo1_id = Column(Integer, ForeignKey("equipo_dobles.id"), nullable=True)
    equipo2_id = Column(Integer, ForeignKey("equipo_dobles.id"), nullable=True)

    jugador1 = relationship("Jugador", foreign_keys=[jugador1_id])
    jugador2 = relationship("Jugador", foreign_keys=[jugador2_id])
    equipo1 = relationship("EquipoDobles", foreign_keys=[equipo1_id])
    equipo2 = relationship("EquipoDobles", foreign_keys=[equipo2_id])

    # Movido dentro de la clase Partido para consistencia
    grupo_id = Column(Integer, ForeignKey("grupo.id"), nullable=True)
    grupo = relationship("Grupo", backref="partidos")

    @validates("tipo")
    def validate_tipo(self, key, tipo):
        if tipo == "individual" and (self.jugador1_id is None or self.jugador2_id is None):
            raise ValueError("Partido individual debe tener dos jugadores.")
        elif tipo == "dobles" and (self.equipo1_id is None or self.equipo2_id is None):
            raise ValueError("Partido de dobles debe tener dos equipos.")
        return tipo

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

class Grupo(Base):
    __tablename__ = "grupo"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)  # Ej: Grupo A, Grupo B
    torneo_id = Column(Integer, ForeignKey("torneo.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)

    torneo = relationship("Torneo", backref="grupos")
    categoria = relationship("Categoria", backref="grupos")

# Participantes en un grupo (individuales)
grupo_participante = Table("grupo_participante", Base.metadata,
    Column("grupo_id", ForeignKey("grupo.id"), primary_key=True),
    Column("jugador_id", ForeignKey("jugador.id"), primary_key=True)
)

class EquipoDobles(Base):
    __tablename__ = "equipo_dobles"
    id = Column(Integer, primary_key=True)
    jugador1_id = Column(Integer, ForeignKey("jugador.id"), nullable=False)
    jugador2_id = Column(Integer, ForeignKey("jugador.id"), nullable=False)

    jugador1 = relationship("Jugador", foreign_keys=[jugador1_id])
    jugador2 = relationship("Jugador", foreign_keys=[jugador2_id])

    __table_args__ = (
        CheckConstraint("jugador1_id != jugador2_id", name="check_jugadores_distintos"),
    )

    @validates("jugador2_id")
    def validate_distintos(self, key, jugador2_id):
        if self.jugador1_id == jugador2_id:
            raise ValueError("Un equipo no puede estar compuesto por el mismo jugador dos veces.")
        return jugador2_id
    
inscripcion_dobles = Table("inscripcion_dobles", Base.metadata,
    Column("equipo_id", ForeignKey("equipo_dobles.id"), primary_key=True),
    Column("torneo_id", ForeignKey("torneo.id"), primary_key=True),
    Column("categoria_id", ForeignKey("categoria.id"), primary_key=True)
)
