from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy.exc import IntegrityError
from app.models import inscripcion_dobles

# CRUD para jugador
def get_jugador(db: Session, jugador_id: int):
    return db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()

def get_jugadores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Jugador).offset(skip).limit(limit).all()

def create_jugador(db: Session, jugador: schemas.JugadorCreate):
    db_jugador = models.Jugador(**jugador.dict())
    db.add(db_jugador)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

def update_jugador(db: Session, jugador_id: int, jugador_data: schemas.JugadorUpdate):
    db_jugador = get_jugador(db, jugador_id)
    if not db_jugador:
        return None
    for key, value in jugador_data.dict(exclude_unset=True).items():
        setattr(db_jugador, key, value)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

def delete_jugador(db: Session, jugador_id: int):
    db_jugador = get_jugador(db, jugador_id)
    if not db_jugador:
        return None
    db.delete(db_jugador)
    db.commit()
    return db_jugador

#CRUD para torneo
def get_torneo(db: Session, torneo_id: int):
    return db.query(models.Torneo).filter(models.Torneo.id == torneo_id).first()

def get_torneos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Torneo).offset(skip).limit(limit).all()

def create_torneo(db: Session, torneo: schemas.TorneoCreate):
    db_torneo = models.Torneo(**torneo.dict())
    db.add(db_torneo)
    db.commit()
    db.refresh(db_torneo)
    return db_torneo

def update_torneo(db: Session, torneo_id: int, torneo_data: schemas.TorneoUpdate):
    db_torneo = get_torneo(db, torneo_id)
    if not db_torneo:
        return None
    for key, value in torneo_data.dict(exclude_unset=True).items():
        setattr(db_torneo, key, value)
    db.commit()
    db.refresh(db_torneo)
    return db_torneo

def delete_torneo(db: Session, torneo_id: int):
    db_torneo = get_torneo(db, torneo_id)
    if not db_torneo:
        return None
    db.delete(db_torneo)
    db.commit()
    return db_torneo

#CRUD para categoria
def get_categoria(db: Session, categoria_id: int):
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Categoria).offset(skip).limit(limit).all()

def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def update_categoria(db: Session, categoria_id: int, categoria_data: schemas.CategoriaUpdate):
    db_categoria = get_categoria(db, categoria_id)
    if not db_categoria:
        return None
    for key, value in categoria_data.dict(exclude_unset=True).items():
        setattr(db_categoria, key, value)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, categoria_id: int):
    db_categoria = get_categoria(db, categoria_id)
    if not db_categoria:
        return None
    db.delete(db_categoria)
    db.commit()
    return db_categoria

# CRUD para aasociacion
def get_asociacion(db: Session, asociacion_id: int):
    return db.query(models.Asociacion).filter(models.Asociacion.id == asociacion_id).first()

def get_asociaciones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Asociacion).offset(skip).limit(limit).all()

def create_asociacion(db: Session, asociacion: schemas.AsociacionCreate):
    db_asociacion = models.Asociacion(**asociacion.dict())
    db.add(db_asociacion)
    db.commit()
    db.refresh(db_asociacion)
    return db_asociacion

def update_asociacion(db: Session, asociacion_id: int, asociacion_data: schemas.AsociacionUpdate):
    db_asociacion = get_asociacion(db, asociacion_id)
    if not db_asociacion:
        return None
    for key, value in asociacion_data.dict(exclude_unset=True).items():
        setattr(db_asociacion, key, value)
    db.commit()
    db.refresh(db_asociacion)
    return db_asociacion

def delete_asociacion(db: Session, asociacion_id: int):
    db_asociacion = get_asociacion(db, asociacion_id)
    if not db_asociacion:
        return None
    db.delete(db_asociacion)
    db.commit()
    return db_asociacion

#CRUD para partido
def get_partido(db: Session, partido_id: int):
    return db.query(models.Partido).filter(models.Partido.id == partido_id).first()

def get_partidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Partido).offset(skip).limit(limit).all()

def create_partido(db: Session, partido: schemas.PartidoCreate):
    # verificaciones simples
    if partido.tipo == "individual":
        jugador1 = db.query(models.Jugador).filter_by(id=partido.jugador1_id).first()
        jugador2 = db.query(models.Jugador).filter_by(id=partido.jugador2_id).first()
        if not jugador1 or not jugador2:
            return None
    elif partido.tipo == "dobles":
        equipo1 = db.query(models.EquipoDobles).filter_by(id=partido.equipo1_id).first()
        equipo2 = db.query(models.EquipoDobles).filter_by(id=partido.equipo2_id).first()
        if not equipo1 or not equipo2:
            return None

    db_partido = models.Partido(**partido.dict())
    db.add(db_partido)
    db.commit()
    db.refresh(db_partido)
    return db_partido


def update_partido(db: Session, partido_id: int, partido_data: schemas.PartidoUpdate):
    db_partido = get_partido(db, partido_id)
    if not db_partido:
        return None
    for key, value in partido_data.dict(exclude_unset=True).items():
        setattr(db_partido, key, value)
    db.commit()
    db.refresh(db_partido)
    return db_partido

def delete_partido(db: Session, partido_id: int):
    db_partido = get_partido(db, partido_id)
    if not db_partido:
        return None
    db.delete(db_partido)
    db.commit()
    return db_partido

#CRUD resultadoSet
def create_resultado_set(db: Session, data: schemas.ResultadoSetCreate):
    resultado = models.ResultadoSet(**data.dict())
    db.add(resultado)
    db.commit()
    db.refresh(resultado)
    return resultado

def get_resultado_set(db: Session, resultado_id: int):
    return db.query(models.ResultadoSet).filter_by(id=resultado_id).first()

def get_resultados_set(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ResultadoSet).offset(skip).limit(limit).all()

def update_resultado_set(db: Session, resultado_id: int, data: schemas.ResultadoSetUpdate):
    resultado = get_resultado_set(db, resultado_id)
    if not resultado:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(resultado, key, value)
    db.commit()
    db.refresh(resultado)
    return resultado

def delete_resultado_set(db: Session, resultado_id: int):
    resultado = get_resultado_set(db, resultado_id)
    if not resultado:
        return None
    db.delete(resultado)
    db.commit()
    return resultado

#CRUD para grupo
def create_grupo(db: Session, grupo: schemas.GrupoCreate):
    nuevo = models.Grupo(**grupo.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def get_grupos(db: Session):
    return db.query(models.Grupo).all()

def update_grupo(db: Session, grupo_id: int, update: schemas.GrupoUpdate):
    grupo = db.query(models.Grupo).filter_by(id=grupo_id).first()
    if not grupo:
        return None
    for key, value in update.dict(exclude_unset=True).items():
        setattr(grupo, key, value)
    db.commit()
    db.refresh(grupo)
    return grupo

def delete_grupo(db: Session, grupo_id: int):
    grupo = db.query(models.Grupo).filter_by(id=grupo_id).first()
    if grupo:
        db.delete(grupo)
        db.commit()
    return grupo

# CRUD para equipoDobles
def create_equipo_dobles(db: Session, equipo: schemas.EquipoDoblesCreate):
    nuevo = models.EquipoDobles(**equipo.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def get_equipos_dobles(db: Session):
    return db.query(models.EquipoDobles).all()

def get_equipo_dobles(db: Session, equipo_id: int):
    return db.query(models.EquipoDobles).filter(models.EquipoDobles.id == equipo_id).first()

def delete_equipo_dobles(db: Session, equipo_id: int):
    equipo = get_equipo_dobles(db, equipo_id)
    if not equipo:
        return None
    db.delete(equipo)
    db.commit()
    return equipo

# CRUD para incripcion
def create_inscripcion(db: Session, inscripcion: schemas.InscripcionCreate):
    existe = db.execute(
        models.inscripcion.select().where(
            (models.inscripcion.c.jugador_id == inscripcion.jugador_id) &
            (models.inscripcion.c.torneo_id == inscripcion.torneo_id) &
            (models.inscripcion.c.categoria_id == inscripcion.categoria_id)
        )
    ).fetchone()

    if existe:
        return None  # ya esta inscrito

    stmt = models.inscripcion.insert().values(**inscripcion.dict())
    db.execute(stmt)
    db.commit()
    return inscripcion


def delete_inscripcion(db: Session, jugador_id: int, torneo_id: int, categoria_id: int):
    stmt = models.inscripcion.delete().where(
        models.inscripcion.c.jugador_id == jugador_id,
        models.inscripcion.c.torneo_id == torneo_id,
        models.inscripcion.c.categoria_id == categoria_id
    )
    db.execute(stmt)
    db.commit()
    return True

def get_inscripciones(db: Session):
    return db.execute(models.inscripcion.select()).fetchall()

def create_inscripcion_dobles(db: Session, equipo_id: int, torneo_id: int, categoria_id: int):
    try:
        db.execute(inscripcion_dobles.insert().values(
            equipo_id=equipo_id,
            torneo_id=torneo_id,
            categoria_id=categoria_id
        ))
        db.commit()
        return {"mensaje": "Inscripción de equipo registrada correctamente"}
    except IntegrityError:
        db.rollback()
        return None

def delete_inscripcion_dobles(db: Session, equipo_id: int, torneo_id: int, categoria_id: int):
    result = db.execute(inscripcion_dobles.delete().where(
        (inscripcion_dobles.c.equipo_id == equipo_id) &
        (inscripcion_dobles.c.torneo_id == torneo_id) &
        (inscripcion_dobles.c.categoria_id == categoria_id)
    ))
    db.commit()
    return result.rowcount > 0

def get_inscripciones_dobles(db: Session):
    result = db.execute(inscripcion_dobles.select())
    return result.fetchall()

