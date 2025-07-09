from pydantic import BaseModel
from datetime import date
from typing import Optional
from datetime import datetime
from typing import List


# Schemas para Jugador

class JugadorBase(BaseModel):
    nombre: str
    fecha_nacimiento: date
    genero: str
    ciudad: str
    pais: str
    asociacion_id: Optional[int]

class JugadorCreate(JugadorBase):
    pass

class JugadorUpdate(BaseModel):
    nombre: Optional[str]
    fecha_nacimiento: Optional[date]
    genero: Optional[str]
    ciudad: Optional[str]
    pais: Optional[str]
    asociacion_id: Optional[int]

class JugadorOut(JugadorBase):
    id: int

    class Config:
        orm_mode = True

# Schemas para Torneo

class TorneoBase(BaseModel):
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    mesas_disponibles: int

class TorneoCreate(TorneoBase):
    pass

class TorneoUpdate(BaseModel):
    nombre: Optional[str]
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    mesas_disponibles: Optional[int]

class TorneoOut(TorneoBase):
    id: int

    class Config:
        orm_mode = True

class CategoriaBase(BaseModel):
    nombre: str
    edad_min: int
    edad_max: int
    genero: str
    sets_por_partido: int
    puntos_por_set: int

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str]
    edad_min: Optional[int]
    edad_max: Optional[int]
    genero: Optional[str]
    sets_por_partido: Optional[int]
    puntos_por_set: Optional[int]

class CategoriaOut(CategoriaBase):
    id: int

    class Config:
        orm_mode = True

class AsociacionBase(BaseModel):
    nombre: str
    ciudad: str
    pais: str

class AsociacionCreate(AsociacionBase):
    pass

class AsociacionUpdate(BaseModel):
    nombre: Optional[str]
    ciudad: Optional[str]
    pais: Optional[str]

class AsociacionOut(AsociacionBase):
    id: int

    class Config:
        orm_mode = True

class PartidoBase(BaseModel):
    tipo: str  # "individual" o "dobles"
    torneo_id: int
    categoria_id: int
    horario: datetime
    mesa: int
    ronda: Optional[str] = None
    bye: Optional[bool] = False
    posicion_llave: Optional[int] = None
    partido_ganador_id: Optional[int] = None
    jugador1_id: Optional[int] = None
    jugador2_id: Optional[int] = None
    equipo1_id: Optional[int] = None
    equipo2_id: Optional[int] = None
    grupo_id: Optional[int] = None

class PartidoCreate(PartidoBase):
    pass

class PartidoUpdate(BaseModel):
    tipo: Optional[str]
    torneo_id: Optional[int]
    categoria_id: Optional[int]
    horario: Optional[datetime]
    mesa: Optional[int]
    ronda: Optional[str]
    bye: Optional[bool]
    posicion_llave: Optional[int]
    partido_ganador_id: Optional[int]
    jugador1_id: Optional[int]
    jugador2_id: Optional[int]
    equipo1_id: Optional[int]
    equipo2_id: Optional[int]
    grupo_id: Optional[int]

class PartidoOut(PartidoBase):
    id: int

    class Config:
        orm_mode = True

class ResultadoSetBase(BaseModel):
    partido_id: int
    numero_set: int
    puntos_jugador1: int
    puntos_jugador2: int

class ResultadoSetCreate(ResultadoSetBase):
    pass

class ResultadoSetUpdate(BaseModel):
    puntos_jugador1: Optional[int]
    puntos_jugador2: Optional[int]

class ResultadoSetOut(ResultadoSetBase):
    id: int

    class Config:
        from_attributes = True  # usar en lugar de orm_mode en Pydantic v2

class InscripcionDobles(BaseModel):
    equipo_id: int
    torneo_id: int
    categoria_id: int

    class Config:
        orm_mode = True

class GrupoBase(BaseModel):
    nombre: str
    torneo_id: int
    categoria_id: int

class GrupoCreate(GrupoBase):
    pass

class GrupoUpdate(BaseModel):
    nombre: Optional[str]
    torneo_id: Optional[int]
    categoria_id: Optional[int]

class GrupoOut(GrupoBase):
    id: int

    class Config:
        orm_mode = True

class EquipoDoblesBase(BaseModel):
    jugador1_id: int
    jugador2_id: int

class EquipoDoblesCreate(EquipoDoblesBase):
    pass

class EquipoDoblesOut(EquipoDoblesBase):
    id: int

    class Config:
        orm_mode = True

class InscripcionCreate(BaseModel):
    jugador_id: int
    torneo_id: int
    categoria_id: int

    class Config:
        orm_mode = True

class InscripcionDoblesCreate(BaseModel):
    equipo_id: int
    torneo_id: int
    categoria_id: int

    class Config:
        orm_mode = True

class InscripcionDoblesOut(BaseModel):
    equipo_id: int
    torneo_id: int
    categoria_id: int

    class Config:
        orm_mode = True

