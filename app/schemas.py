from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List

# Esquemas para Asociacion
class AsociacionBase(BaseModel):
    nombre: str
    ciudad: str
    pais: str

class AsociacionCreate(AsociacionBase):
    pass

class AsociacionUpdate(AsociacionBase):
    nombre: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None

class AsociacionOut(AsociacionBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para Categoria
class CategoriaBase(BaseModel):
    nombre: str
    edad_min: int = Field(..., ge=0) 
    edad_max: int = Field(..., ge=0)
    genero: str = Field(..., pattern="^(M|F)$") #"M" o "F"
    sets_por_partido: int = Field(..., gt=0) 
    puntos_por_set: int = Field(..., gt=0)

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(CategoriaBase):
    nombre: Optional[str] = None
    edad_min: Optional[int] = Field(None, ge=0)
    edad_max: Optional[int] = Field(None, ge=0)
    genero: Optional[str] = Field(None, pattern="^(M|F)$")
    sets_por_partido: Optional[int] = Field(None, gt=0)
    puntos_por_set: Optional[int] = Field(None, gt=0)

class CategoriaOut(CategoriaBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para Jugador
class JugadorBase(BaseModel):
    nombre: str
    fecha_nacimiento: date
    genero: str = Field(..., pattern="^(M|F)$")
    ciudad: str
    pais: str
    asociacion_id: Optional[int] = None # puede ser nulo

class JugadorCreate(JugadorBase):
    pass

class JugadorUpdate(JugadorBase):
    nombre: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = Field(None, pattern="^(M|F)$")
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    asociacion_id: Optional[int] = None

class JugadorOut(JugadorBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para Torneo
class TorneoBase(BaseModel):
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    mesas_disponibles: int = Field(..., gt=0)
    fecha_inscripcion_inicio: date
    fecha_inscripcion_fin: date

class TorneoCreate(TorneoBase):
    pass

class TorneoUpdate(TorneoBase):
    nombre: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    mesas_disponibles: Optional[int] = Field(None, gt=0)
    fecha_inscripcion_inicio: Optional[date] = None
    fecha_inscripcion_fin: Optional[date] = None

class TorneoOut(TorneoBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para EquipoDobles
class EquipoDoblesBase(BaseModel):
    jugador1_id: int
    jugador2_id: int

class EquipoDoblesCreate(EquipoDoblesBase):
    pass

class EquipoDoblesUpdate(EquipoDoblesBase):
    jugador1_id: Optional[int] = None
    jugador2_id: Optional[int] = None

class EquipoDoblesOut(EquipoDoblesBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para Partido
class PartidoBase(BaseModel):
    tipo: str = Field(..., pattern="^(individual|dobles)$") # individual o doble
    torneo_id: int
    categoria_id: int
    horario: datetime
    mesa: int = Field(..., gt=0)
    ronda: Optional[str] = None
    bye: bool = False
    posicion_llave: Optional[int] = None
    partido_ganador_id: Optional[int] = None
    jugador1_id: Optional[int] = None
    jugador2_id: Optional[int] = None
    equipo1_id: Optional[int] = None
    equipo2_id: Optional[int] = None
    grupo_id: Optional[int] = None

class PartidoCreate(PartidoBase):
    pass

class PartidoUpdate(PartidoBase):
    tipo: Optional[str] = Field(None, pattern="^(individual|dobles)$")
    torneo_id: Optional[int] = None
    categoria_id: Optional[int] = None
    horario: Optional[datetime] = None
    mesa: Optional[int] = Field(None, gt=0)
    ronda: Optional[str] = None
    bye: Optional[bool] = None
    posicion_llave: Optional[int] = None
    partido_ganador_id: Optional[int] = None
    jugador1_id: Optional[int] = None
    jugador2_id: Optional[int] = None
    equipo1_id: Optional[int] = None
    equipo2_id: Optional[int] = None
    grupo_id: Optional[int] = None

class PartidoOut(PartidoBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para ResultadoSet
class ResultadoSetBase(BaseModel):
    partido_id: int
    numero_set: int = Field(..., gt=0) # Número de set debe ser mayor a 0
    puntos_jugador1: int = Field(..., ge=0) # Puntos no pueden ser negativos
    puntos_jugador2: int = Field(..., ge=0) # Puntos no pueden ser negativos

class ResultadoSetCreate(ResultadoSetBase):
    pass

class ResultadoSetUpdate(ResultadoSetBase):
    partido_id: Optional[int] = None # No se deberia cambiar el partido_id de un resultado de set
    numero_set: Optional[int] = Field(None, gt=0)
    puntos_jugador1: Optional[int] = Field(None, ge=0)
    puntos_jugador2: Optional[int] = Field(None, ge=0)

class ResultadoSetOut(ResultadoSetBase):
    id: int

    class Config:
        from_attributes = True  

# Esquemas para Grupo
class GrupoBase(BaseModel):
    nombre: str
    torneo_id: int
    categoria_id: int

class GrupoCreate(GrupoBase):
    pass

class GrupoUpdate(GrupoBase):
    nombre: Optional[str] = None
    torneo_id: Optional[int] = None
    categoria_id: Optional[int] = None

class GrupoOut(GrupoBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para Inscripción Individual (tabla de asociación inscripcion)
class InscripcionCreate(BaseModel):
    jugador_id: int
    torneo_id: int
    categoria_id: int

class InscripcionOut(InscripcionCreate):

    class Config:
        from_attributes = True

# Esquemas para Inscripción Dobles (tabla de asociación inscripcion_dobles)
class InscripcionDoblesCreate(BaseModel):
    equipo_id: int
    torneo_id: int
    categoria_id: int

class InscripcionDoblesOut(InscripcionDoblesCreate):

    class Config:
        from_attributes = True

# Esquemas para Grupo Participante (tabla de asociación grupo_participante)
class GrupoParticipanteCreate(BaseModel):
    grupo_id: int
    jugador_id: int

class GrupoParticipanteOut(GrupoParticipanteCreate):

    class Config:
        from_attributes = True
