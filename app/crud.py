from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from . import models, schemas 
from datetime import date, datetime
from typing import List, Optional
import random

# funciones crud para jugador
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
    return db_jugador # retorna el objeto eliminado si se encontro

# funciones crud para torneo
def get_torneo(db: Session, torneo_id: int):
    return db.query(models.Torneo).filter(models.Torneo.id == torneo_id).first()

def get_torneos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Torneo).offset(skip).limit(limit).all()

def create_torneo(db: Session, torneo: schemas.TorneoCreate):
    # validasiones de fechas
    if torneo.fecha_inscripcion_inicio > torneo.fecha_inscripcion_fin:
        raise ValueError("La fecha de inicio de inscripción no puede ser despues a la fecha de fin de inscripción.")
    if torneo.fecha_inicio > torneo.fecha_fin:
        raise ValueError("La fecha de inicio del torneo no puede ser despues a la fecha de fin del torneo.")
    if torneo.fecha_inscripcion_fin > torneo.fecha_inicio:
        raise ValueError("La fecha de fin de inscripción no puede ser despues a la fecha de inicio del torneo.")

    db_torneo = models.Torneo(**torneo.dict())
    db.add(db_torneo)
    db.commit()
    db.refresh(db_torneo)
    return db_torneo

def update_torneo(db: Session, torneo_id: int, torneo_data: schemas.TorneoUpdate):
    db_torneo = get_torneo(db, torneo_id)
    if not db_torneo:
        return None
    
    update_data = torneo_data.dict(exclude_unset=True)

    # validaciones de fechas durante la actualizacion
    if 'fecha_inscripcion_inicio' in update_data and 'fecha_inscripcion_fin' in update_data:
        if update_data['fecha_inscripcion_inicio'] > update_data['fecha_inscripcion_fin']:
            raise ValueError("La fecha de inicio de inscripción no puede ser posterior a la fecha de fin de inscripción.")
    elif 'fecha_inscripcion_inicio' in update_data and db_torneo.fecha_inscripcion_fin:
        if update_data['fecha_inscripcion_inicio'] > db_torneo.fecha_inscripcion_fin:
            raise ValueError("La fecha de inicio de inscripción no puede ser posterior a la fecha de fin de inscripción existente.")
    elif 'fecha_inscripcion_fin' in update_data and db_torneo.fecha_inscripcion_inicio:
        if db_torneo.fecha_inscripcion_inicio > update_data['fecha_inscripcion_fin']:
            raise ValueError("La fecha de fin de inscripción no puede ser anterior a la fecha de inicio de inscripción existente.")

    if 'fecha_inicio' in update_data and 'fecha_fin' in update_data:
        if update_data['fecha_inicio'] > update_data['fecha_fin']:
            raise ValueError("La fecha de inicio del torneo no puede ser posterior a la fecha de fin del torneo.")
    elif 'fecha_inicio' in update_data and db_torneo.fecha_fin:
        if update_data['fecha_inicio'] > db_torneo.fecha_fin:
            raise ValueError("La fecha de inicio del torneo no puede ser posterior a la fecha de fin del torneo existente.")
    elif 'fecha_fin' in update_data and db_torneo.fecha_inicio:
        if db_torneo.fecha_inicio > update_data['fecha_fin']:
            raise ValueError("La fecha de fin del torneo no puede ser anterior a la fecha de inicio del torneo existente.")

    # validación cruzada entre fechas de inscripción y torneo
    if ('fecha_inscripcion_fin' in update_data and db_torneo.fecha_inicio and update_data['fecha_inscripcion_fin'] > db_torneo.fecha_inicio) or \
       ('fecha_inicio' in update_data and db_torneo.fecha_inscripcion_fin and db_torneo.fecha_inscripcion_fin > update_data['fecha_inicio']):
        raise ValueError("La fecha de fin de inscripción no puede ser posterior a la fecha de inicio del torneo.")


    for key, value in update_data.items():
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

# funciones crudf para categoria
def get_categoria(db: Session, categoria_id: int):
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Categoria).offset(skip).limit(limit).all()

def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    # validaciones de reglas de categoria
    if categoria.edad_min > categoria.edad_max:
        raise ValueError("La edad mínima no puede ser mayor que la edad máxima.")
    if categoria.sets_por_partido <= 0:
        raise ValueError("Los sets por partido deben ser mayores a 0.")
    if categoria.puntos_por_set <= 0:
        raise ValueError("Los puntos por set deben ser mayores a 0.")

    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def update_categoria(db: Session, categoria_id: int, categoria_data: schemas.CategoriaUpdate):
    db_categoria = get_categoria(db, categoria_id)
    if not db_categoria:
        return None
    
    update_data = categoria_data.dict(exclude_unset=True)

    # validaciones de reglas de categoria durante la actualización
    if 'edad_min' in update_data and 'edad_max' in update_data:
        if update_data['edad_min'] > update_data['edad_max']:
            raise ValueError("La edad mínima no puede ser mayor que la edad máxima.")
    elif 'edad_min' in update_data and db_categoria.edad_max:
        if update_data['edad_min'] > db_categoria.edad_max:
            raise ValueError("La edad mínima no puede ser mayor que la edad máxima existente.")
    elif 'edad_max' in update_data and db_categoria.edad_min:
        if db_categoria.edad_min > update_data['edad_max']:
            raise ValueError("La edad máxima no puede ser menor que la edad mínima existente.")

    if 'sets_por_partido' in update_data and update_data['sets_por_partido'] <= 0:
        raise ValueError("Los sets por partido deben ser mayores a 0.")
    if 'puntos_por_set' in update_data and update_data['puntos_por_set'] <= 0:
        raise ValueError("Los puntos por set deben ser mayores a 0.")

    for key, value in update_data.items():
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

# funciones crud para asociacion
def get_asociacion(db: Session, asociacion_id: int):
    return db.query(models.Asociacion).filter(models.Asociacion.id == asociacion_id).first()

def get_asociacion_by_nombre(db: Session, nombre: str):
    return db.query(models.Asociacion).filter(models.Asociacion.nombre == nombre).first()

def get_asociaciones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Asociacion).offset(skip).limit(limit).all()

def create_asociacion(db: Session, asociacion: schemas.AsociacionCreate):
    db_asociacion = models.Asociacion(**asociacion.dict())
    db.add(db_asociacion)
    try:
        db.commit()
        db.refresh(db_asociacion)
        return db_asociacion
    except IntegrityError:
        db.rollback()
        raise ValueError("Ya existe una asociación con este nombre.") 

def update_asociacion(db: Session, asociacion_id: int, asociacion_data: schemas.AsociacionUpdate):
    db_asociacion = get_asociacion(db, asociacion_id)
    if not db_asociacion:
        return None
    for key, value in asociacion_data.dict(exclude_unset=True).items():
        setattr(db_asociacion, key, value)
    try:
        db.commit()
        db.refresh(db_asociacion)
        return db_asociacion
    except IntegrityError:
        db.rollback()
        raise ValueError("Ya existe otra asociación con el nombre proporcionado.")

def delete_asociacion(db: Session, asociacion_id: int):
    db_asociacion = get_asociacion(db, asociacion_id)
    if not db_asociacion:
        return None
    db.delete(db_asociacion)
    db.commit()
    return db_asociacion

# funciones crud para partido
def get_partido(db: Session, partido_id: int):
    return db.query(models.Partido).filter(models.Partido.id == partido_id).first()

def get_partidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Partido).offset(skip).limit(limit).all()

def create_partido(db: Session, partido: schemas.PartidoCreate):
    # verificaciones de existencia de participantes
    if partido.tipo == "individual":
        jugador1 = db.query(models.Jugador).filter_by(id=partido.jugador1_id).first()
        jugador2 = db.query(models.Jugador).filter_by(id=partido.jugador2_id).first()
        if not jugador1:
            raise ValueError(f"Jugador 1 con ID {partido.jugador1_id} no encontrado.")
        if not jugador2:
            raise ValueError(f"Jugador 2 con ID {partido.jugador2_id} no encontrado.")
        if jugador1.id == jugador2.id:
            raise ValueError("Los jugadores de un partido individual no pueden ser el mismo.")
    elif partido.tipo == "dobles":
        equipo1 = db.query(models.EquipoDobles).filter_by(id=partido.equipo1_id).first()
        equipo2 = db.query(models.EquipoDobles).filter_by(id=partido.equipo2_id).first()
        if not equipo1:
            raise ValueError(f"Equipo 1 con ID {partido.equipo1_id} no encontrado.")
        if not equipo2:
            raise ValueError(f"Equipo 2 con ID {partido.equipo2_id} no encontrado.")
        if equipo1.id == equipo2.id:
            raise ValueError("Los equipos de un partido de dobles no pueden ser el mismo.")
    else:
        raise ValueError("Tipo de partido inválido. Debe ser 'individual' o 'dobles'.")

    # verificación de existencia de torneo y categoria
    torneo = get_torneo(db, partido.torneo_id)
    if not torneo:
        raise ValueError(f"Torneo con ID {partido.torneo_id} no encontrado.")
    categoria = get_categoria(db, partido.categoria_id)
    if not categoria:
        raise ValueError(f"Categoría con ID {partido.categoria_id} no encontrada.")
    
    # verificación de mesa disponible
    if partido.mesa <= 0 or partido.mesa > torneo.mesas_disponibles:
        raise ValueError(f"Mesa {partido.mesa} no válida para el torneo. Mesas disponibles: 1 a {torneo.mesas_disponibles}.")

    db_partido = models.Partido(**partido.dict())
    db.add(db_partido)
    db.commit()
    db.refresh(db_partido)
    return db_partido


def update_partido(db: Session, partido_id: int, partido_data: schemas.PartidoUpdate):
    db_partido = get_partido(db, partido_id)
    if not db_partido:
        return None
    
    update_dict = partido_data.dict(exclude_unset=True)

    # validaciones para cambios de tipo o participantes
    if 'tipo' in update_dict and update_dict['tipo'] != db_partido.tipo:
        raise ValueError("El tipo de partido no puede ser modificado después de la creación.")
    if 'jugador1_id' in update_dict or 'jugador2_id' in update_dict or \
       'equipo1_id' in update_dict or 'equipo2_id' in update_dict:
        raise ValueError("Los participantes de un partido no pueden ser modificados directamente. Crea un nuevo partido si es necesario.")

    # validaciones de existencia de torneo y categoría si se actualizan (aunque no deberían cambiar)
    if 'torneo_id' in update_dict:
        torneo = get_torneo(db, update_dict['torneo_id'])
        if not torneo:
            raise ValueError(f"Torneo con ID {update_dict['torneo_id']} no encontrado.")
    if 'categoria_id' in update_dict:
        categoria = get_categoria(db, update_dict['categoria_id'])
        if not categoria:
            raise ValueError(f"Categoría con ID {update_dict['categoria_id']} no encontrada.")
    
    # Verificacion de mesa disponible si se actualiza
    if 'mesa' in update_dict and db_partido.torneo: 
        if update_dict['mesa'] <= 0 or update_dict['mesa'] > db_partido.torneo.mesas_disponibles:
            raise ValueError(f"Mesa {update_dict['mesa']} no válida para el torneo. Mesas disponibles: 1 a {db_partido.torneo.mesas_disponibles}.")


    for key, value in update_dict.items():
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

# funciones crud para ResultadoSet
def create_resultado_set(db: Session, data: schemas.ResultadoSetCreate):
    # Validaciones adicionales:
    partido = get_partido(db, data.partido_id)
    if not partido:
        raise ValueError(f"Partido con ID {data.partido_id} no encontrado.")
    
    categoria = get_categoria(db, partido.categoria_id)
    if not categoria:
        raise ValueError(f"Categoría del partido con ID {partido.categoria_id} no encontrada.")
    
    # Validar que el numero de set sea consecutivo y no exceda el máximo
    sets_existentes = get_resultados_set_by_partido(db, partido.id)
    if data.numero_set > len(sets_existentes) + 1:
        raise ValueError(f"El set número {data.numero_set} no es el siguiente set consecutivo. El siguiente set esperado es {len(sets_existentes) + 1}.")
    if data.numero_set > categoria.sets_por_partido:
        raise ValueError(f"Número de set inválido ({data.numero_set}). La categoría '{categoria.nombre}' solo permite hasta {categoria.sets_por_partido} sets.")
    
    # Validar puntos 
    if data.puntos_jugador1 < 0 or data.puntos_jugador2 < 0:
        raise ValueError("Los puntos no pueden ser negativos.")
    

    resultado = models.ResultadoSet(**data.dict())
    db.add(resultado)
    try:
        db.commit()
        db.refresh(resultado)
        return resultado
    except IntegrityError:
        db.rollback()
        raise ValueError(f"El set número {data.numero_set} ya ha sido registrado para el partido {data.partido_id}.")


def get_resultado_set(db: Session, resultado_id: int):
    return db.query(models.ResultadoSet).filter_by(id=resultado_id).first()

def get_resultados_set(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ResultadoSet).offset(skip).limit(limit).all()

def get_resultados_set_by_partido(db: Session, partido_id: int):
    return db.query(models.ResultadoSet).filter(models.ResultadoSet.partido_id == partido_id).order_by(models.ResultadoSet.numero_set).all()

def update_resultado_set(db: Session, resultado_id: int, data: schemas.ResultadoSetUpdate):
    resultado = get_resultado_set(db, resultado_id)
    if not resultado:
        return None
    
    update_dict = data.dict(exclude_unset=True)

    # Validaciones para numero de set y puntos al actualizar
    if 'numero_set' in update_dict and update_dict['numero_set'] <= 0:
        raise ValueError("El número de set debe ser mayor a 0.")
    if 'puntos_jugador1' in update_dict and update_dict['puntos_jugador1'] < 0:
        raise ValueError("Los puntos del jugador 1 no pueden ser negativos.")
    if 'puntos_jugador2' in update_dict and update_dict['puntos_jugador2'] < 0:
        raise ValueError("Los puntos del jugador 2 no pueden ser negativos.")

    for key, value in update_dict.items():
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

# funciones crud para Grupo
def create_grupo(db: Session, grupo: schemas.GrupoCreate):
    # validar que torneo y categoria existan
    torneo = get_torneo(db, grupo.torneo_id)
    if not torneo:
        raise ValueError(f"Torneo con ID {grupo.torneo_id} no encontrado para el grupo.")
    categoria = get_categoria(db, grupo.categoria_id)
    if not categoria:
        raise ValueError(f"Categoría con ID {grupo.categoria_id} no encontrada para el grupo.")

    nuevo = models.Grupo(**grupo.dict())
    db.add(nuevo)
    try:
        db.commit()
        db.refresh(nuevo)
        return nuevo
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Ya existe un grupo con el nombre '{grupo.nombre}' para este torneo y categoría.")


def get_grupo(db: Session, grupo_id: int):
    return db.query(models.Grupo).filter_by(id=grupo_id).first()

def get_grupos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Grupo).offset(skip).limit(limit).all()

def update_grupo(db: Session, grupo_id: int, update: schemas.GrupoUpdate):
    grupo = get_grupo(db, grupo_id)
    if not grupo:
        return None
    
    update_dict = update.dict(exclude_unset=True)

    # Validar que torneo y categoria existan si se actualizan
    if 'torneo_id' in update_dict:
        torneo = get_torneo(db, update_dict['torneo_id'])
        if not torneo:
            raise ValueError(f"Torneo con ID {update_dict['torneo_id']} no encontrado para el grupo.")
    if 'categoria_id' in update_dict:
        categoria = get_categoria(db, update_dict['categoria_id'])
        if not categoria:
            raise ValueError(f"Categoría con ID {update_dict['categoria_id']} no encontrada para el grupo.")

    for key, value in update_dict.items():
        setattr(grupo, key, value)
    try:
        db.commit()
        db.refresh(grupo)
        return grupo
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Ya existe otro grupo con el nombre '{update.nombre}' para este torneo y categoría.")


def delete_grupo(db: Session, grupo_id: int):
    grupo = get_grupo(db, grupo_id)
    if not grupo:
        return None
    db.delete(grupo)
    db.commit()
    return grupo

# funciones crud para EquipoDobles 
def create_equipo_dobles(db: Session, equipo: schemas.EquipoDoblesCreate):
    # Validar que los jugadores existan
    jugador1 = get_jugador(db, equipo.jugador1_id)
    jugador2 = get_jugador(db, equipo.jugador2_id)
    if not jugador1:
        raise ValueError(f"Jugador 1 con ID {equipo.jugador1_id} no encontrado.")
    if not jugador2:
        raise ValueError(f"Jugador 2 con ID {equipo.jugador2_id} no encontrado.")
    
    if equipo.jugador1_id == equipo.jugador2_id:
        raise ValueError("Un equipo no puede estar compuesto por el mismo jugador dos veces.")

    nuevo = models.EquipoDobles(**equipo.dict())
    db.add(nuevo)
    try:
        db.commit()
        db.refresh(nuevo)
        return nuevo
    except IntegrityError:
        db.rollback()
        raise ValueError("Ya existe un equipo con estos jugadores.")

def get_equipos_dobles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.EquipoDobles).offset(skip).limit(limit).all()

def get_equipo_dobles(db: Session, equipo_id: int):
    return db.query(models.EquipoDobles).filter(models.EquipoDobles.id == equipo_id).first()

def update_equipo_dobles(db: Session, equipo_id: int, equipo_data: schemas.EquipoDoblesUpdate):
    db_equipo = get_equipo_dobles(db, equipo_id)
    if not db_equipo:
        return None
    
    update_dict = equipo_data.dict(exclude_unset=True)

    # Validar que los jugadores existan si se actualizan
    if 'jugador1_id' in update_dict:
        jugador1 = get_jugador(db, update_dict['jugador1_id'])
        if not jugador1:
            raise ValueError(f"Jugador 1 con ID {update_dict['jugador1_id']} no encontrado.")
    if 'jugador2_id' in update_dict:
        jugador2 = get_jugador(db, update_dict['jugador2_id'])
        if not jugador2:
            raise ValueError(f"Jugador 2 con ID {update_dict['jugador2_id']} no encontrado.")
    
    # Validar que los jugadores sean distintos
    final_jugador1_id = update_dict.get('jugador1_id', db_equipo.jugador1_id)
    final_jugador2_id = update_dict.get('jugador2_id', db_equipo.jugador2_id)
    if final_jugador1_id == final_jugador2_id:
        raise ValueError("Un equipo no puede estar compuesto por el mismo jugador dos veces.")

    for key, value in update_dict.items():
        setattr(db_equipo, key, value)
    try:
        db.commit()
        db.refresh(db_equipo)
        return db_equipo
    except IntegrityError:
        db.rollback()
        raise ValueError("Ya existe un equipo con estos jugadores después de la actualización.")


def delete_equipo_dobles(db: Session, equipo_id: int):
    equipo = get_equipo_dobles(db, equipo_id)
    if not equipo:
        return None
    db.delete(equipo)
    db.commit()
    return equipo

# funciones para inscripciones individuales 
def create_inscripcion(db: Session, inscripcion: schemas.InscripcionCreate):
    # Validar que jugador, torneo y categoría existan
    jugador = get_jugador(db, inscripcion.jugador_id)
    if not jugador:
        raise ValueError(f"Jugador con ID {inscripcion.jugador_id} no encontrado para la inscripción.")
    torneo = get_torneo(db, inscripcion.torneo_id)
    if not torneo:
        raise ValueError(f"Torneo con ID {inscripcion.torneo_id} no encontrado para la inscripción.")
    categoria = get_categoria(db, inscripcion.categoria_id)
    if not categoria:
        raise ValueError(f"Categoría con ID {inscripcion.categoria_id} no encontrada para la inscripción.")

    # Validar que la inscripcion esté dentro de las fechas de inscripción del torneo
    hoy = date.today()
    if not (torneo.fecha_inscripcion_inicio <= hoy <= torneo.fecha_inscripcion_fin):
        raise ValueError("El torneo no está en período de inscripción.")

    # Validar que el jugador cumpla con los requisitos de edad y género de la categoría
    edad_jugador = hoy.year - jugador.fecha_nacimiento.year - ((hoy.month, hoy.day) < (jugador.fecha_nacimiento.month, jugador.fecha_nacimiento.day))
    if not (categoria.edad_min <= edad_jugador <= categoria.edad_max):
        raise ValueError(f"El jugador no cumple con el rango de edad ({categoria.edad_min}-{categoria.edad_max}) de la categoría.")
    if jugador.genero != categoria.genero:
        raise ValueError(f"El género del jugador ('{jugador.genero}') no coincide con el género de la categoría ('{categoria.genero}').")

    # Verificar si ya está inscrito
    existe = db.execute(
        models.inscripcion.select().where(
            (models.inscripcion.c.jugador_id == inscripcion.jugador_id) &
            (models.inscripcion.c.torneo_id == inscripcion.torneo_id) &
            (models.inscripcion.c.categoria_id == inscripcion.categoria_id)
        )
    ).fetchone()

    if existe:
        raise ValueError("El jugador ya está inscrito en esta categoría para este torneo.")

    stmt = models.inscripcion.insert().values(**inscripcion.dict())
    try:
        db.execute(stmt)
        db.commit()
        return inscripcion
    except IntegrityError:
        db.rollback()
        raise ValueError("Error al registrar la inscripción. Podría ser una inscripción duplicada.")


def delete_inscripcion(db: Session, jugador_id: int, torneo_id: int, categoria_id: int):
    stmt = models.inscripcion.delete().where(
        models.inscripcion.c.jugador_id == jugador_id,
        models.inscripcion.c.torneo_id == torneo_id,
        models.inscripcion.c.categoria_id == categoria_id
    )
    result = db.execute(stmt)
    db.commit()
    return result.rowcount > 0 # retorna true si se elimino al menos una fila

def get_inscripciones(db: Session, skip: int = 0, limit: int = 100):

    results = db.execute(models.inscripcion.select().offset(skip).limit(limit)).fetchall()
    return [schemas.InscripcionOut(**r._asdict()) for r in results]

def get_inscripcion(db: Session, jugador_id: int, torneo_id: int, categoria_id: int):
    result = db.execute(
        models.inscripcion.select().where(
            (models.inscripcion.c.jugador_id == jugador_id) &
            (models.inscripcion.c.torneo_id == torneo_id) &
            (models.inscripcion.c.categoria_id == categoria_id)
        )
    ).fetchone()
    if result:
        return schemas.InscripcionOut(**result._asdict())
    return None

# funciones para Inscripciones Dobles 
def create_inscripcion_dobles(db: Session, inscripcion: schemas.InscripcionDoblesCreate):
    # Validar que equipo, torneo y categoría existan
    equipo = get_equipo_dobles(db, inscripcion.equipo_id)
    if not equipo:
        raise ValueError(f"Equipo de dobles con ID {inscripcion.equipo_id} no encontrado para la inscripción.")
    torneo = get_torneo(db, inscripcion.torneo_id)
    if not torneo:
        raise ValueError(f"Torneo con ID {inscripcion.torneo_id} no encontrado para la inscripción.")
    categoria = get_categoria(db, inscripcion.categoria_id)
    if not categoria:
        raise ValueError(f"Categoría con ID {inscripcion.categoria_id} no encontrada para la inscripción.")

    # Validar que la inscripción esté dentro de las fechas de inscripción del torneo
    hoy = date.today()
    if not (torneo.fecha_inscripcion_inicio <= hoy <= torneo.fecha_inscripcion_fin):
        raise ValueError("El torneo no está en período de inscripción.")

    # Verificar si ya está inscrito
    existe = db.execute(
        models.inscripcion_dobles.select().where(
            (models.inscripcion_dobles.c.equipo_id == inscripcion.equipo_id) &
            (models.inscripcion_dobles.c.torneo_id == inscripcion.torneo_id) &
            (models.inscripcion_dobles.c.categoria_id == inscripcion.categoria_id)
        )
    ).fetchone()

    if existe:
        raise ValueError("El equipo ya está inscrito en esta categoría para este torneo.")

    stmt = models.inscripcion_dobles.insert().values(**inscripcion.dict())
    try:
        db.execute(stmt)
        db.commit()
        return inscripcion
    except IntegrityError:
        db.rollback()
        raise ValueError("Error al registrar la inscripción de equipo. Podría ser una inscripción duplicada.")


def delete_inscripcion_dobles(db: Session, equipo_id: int, torneo_id: int, categoria_id: int):
    result = db.execute(models.inscripcion_dobles.delete().where(
        (models.inscripcion_dobles.c.equipo_id == equipo_id) &
        (models.inscripcion_dobles.c.torneo_id == torneo_id) &
        (models.inscripcion_dobles.c.categoria_id == categoria_id)
    ))
    db.commit()
    return result.rowcount > 0

def get_inscripciones_dobles(db: Session, skip: int = 0, limit: int = 100):
    results = db.execute(models.inscripcion_dobles.select().offset(skip).limit(limit)).fetchall()
    return [schemas.InscripcionDoblesOut(**r._asdict()) for r in results]

def get_inscripcion_dobles(db: Session, equipo_id: int, torneo_id: int, categoria_id: int):
    result = db.execute(
        models.inscripcion_dobles.select().where(
            (models.inscripcion_dobles.c.equipo_id == equipo_id) &
            (models.inscripcion_dobles.c.torneo_id == torneo_id) &
            (models.inscripcion_dobles.c.categoria_id == categoria_id)
        )
    ).fetchone()
    if result:
        return schemas.InscripcionDoblesOut(**result._asdict())
    return None

# funciones para Grupo Participante
def create_grupo_participante(db: Session, grupo_participante: schemas.GrupoParticipanteCreate):
    # Validar que grupo y jugador existan
    grupo = get_grupo(db, grupo_participante.grupo_id)
    if not grupo:
        raise ValueError(f"Grupo con ID {grupo_participante.grupo_id} no encontrado.")
    jugador = get_jugador(db, grupo_participante.jugador_id)
    if not jugador:
        raise ValueError(f"Jugador con ID {grupo_participante.jugador_id} no encontrado.")
    
    # Validar que el jugador no este ya en el grupo
    existe = db.execute(
        models.grupo_participante.select().where(
            (models.grupo_participante.c.grupo_id == grupo_participante.grupo_id) &
            (models.grupo_participante.c.jugador_id == grupo_participante.jugador_id)
        )
    ).fetchone()
    if existe:
        raise ValueError("El jugador ya está asignado a este grupo.")

    stmt = models.grupo_participante.insert().values(**grupo_participante.dict())
    try:
        db.execute(stmt)
        db.commit()
        return grupo_participante
    except IntegrityError:
        db.rollback()
        raise ValueError("Error al asignar jugador al grupo. Podría ser una asignación duplicada.")

def delete_grupo_participante(db: Session, grupo_id: int, jugador_id: int):
    result = db.execute(models.grupo_participante.delete().where(
        (models.grupo_participante.c.grupo_id == grupo_id) &
        (models.grupo_participante.c.jugador_id == jugador_id)
    ))
    db.commit()
    return result.rowcount > 0

def get_grupo_participantes(db: Session, skip: int = 0, limit: int = 100):
    results = db.execute(models.grupo_participante.select().offset(skip).limit(limit)).fetchall()
    return [schemas.GrupoParticipanteOut(**r._asdict()) for r in results]

def get_grupo_participante(db: Session, grupo_id: int, jugador_id: int):
    result = db.execute(
        models.grupo_participante.select().where(
            (models.grupo_participante.c.grupo_id == grupo_id) &
            (models.grupo_participante.c.jugador_id == jugador_id)
        )
    ).fetchone()
    if result:
        return schemas.GrupoParticipanteOut(**result._asdict())
    return None


def generar_partidos_grupo(db: Session, grupo_id: int):

    grupo = get_grupo(db, grupo_id)
    if not grupo:
        raise ValueError("Grupo no encontrado")

    # Obtener los jugadores en el grupo
    jugadores_en_grupo = db.query(models.Jugador).join(models.grupo_participante).filter(
        models.grupo_participante.c.grupo_id == grupo_id
    ).all()

    if len(jugadores_en_grupo) < 2:
        raise ValueError("Se necesitan al menos dos jugadores para generar partidos en el grupo.")

    partidos_generados = []
    # Generar partidos de todos contra todos
    for i in range(len(jugadores_en_grupo)):
        for j in range(i + 1, len(jugadores_en_grupo)):
            jugador1 = jugadores_en_grupo[i]
            jugador2 = jugadores_en_grupo[j]

            existing_match = db.query(models.Partido).filter(
                models.Partido.torneo_id == grupo.torneo_id,
                models.Partido.categoria_id == grupo.categoria_id,
                models.Partido.grupo_id == grupo.id,
                models.Partido.tipo == "individual",
                # Verificar ambos ordenes de jugadores
                ((models.Partido.jugador1_id == jugador1.id) & (models.Partido.jugador2_id == jugador2.id)) |
                ((models.Partido.jugador1_id == jugador2.id) & (models.Partido.jugador2_id == jugador1.id))
            ).first()

            if existing_match:
                print(f"Partido entre {jugador1.nombre} y {jugador2.nombre} ya existe en el grupo {grupo.nombre}. Saltando.")
                continue

            partido_data = schemas.PartidoCreate(
                tipo="individual",
                torneo_id=grupo.torneo_id,
                categoria_id=grupo.categoria_id,
                horario=datetime.now(), 
                mesa=1,                 
                ronda="Fase de Grupos",
                bye=False,
                jugador1_id=jugador1.id,
                jugador2_id=jugador2.id,
                equipo1_id=None, # no aplica para individuales
                equipo2_id=None, # No aplica para individuale
                grupo_id=grupo.id
            )
            try:
                db_partido = create_partido(db, partido_data)
                partidos_generados.append(db_partido)
            except ValueError as e:
                print(f"Error al crear partido en grupo: {e}")
                db.rollback() 

    return partidos_generados

def generar_llave_eliminacion(db: Session, torneo_id: int, categoria_id: int, participantes_ids: List[int], tipo_partido: str):

    if not participantes_ids:
        return []

    num_participantes = len(participantes_ids)
    
    # Determinar la potencia de 2 más cercana y mayor o igual al número de participantes
    llave_size = 2
    while llave_size < num_participantes:
        llave_size *= 2
    
    num_byes = llave_size - num_participantes

    # Mezcla participantes para una distribución aleatoria
    random.shuffle(participantes_ids)
    
    # crea un arreglo para la llave, inicializado con None (para Byes)
    llave_participantes = [None] * llave_size
    
    # Llenar las primeras posiciones con los participantes reales
    for i in range(num_participantes):
        llave_participantes[i] = participantes_ids[i]


    partidos_generados = []
    ronda_actual = "Ronda 1"
    
    # Crea partidos de la primera ronda
    for i in range(0, llave_size, 2):
        participante1_id = llave_participantes[i]
        participante2_id = llave_participantes[i+1] if i+1 < llave_size else None 

        is_bye_match = (participante1_id is None) or (participante2_id is None)

        partido_data_common = {
            "tipo": tipo_partido,
            "torneo_id": torneo_id,
            "categoria_id": categoria_id,
            "horario": datetime.now(), 
            "mesa": 1,                 
            "ronda": ronda_actual,
            "bye": is_bye_match,
            "posicion_llave": i // 2 + 1,
            "partido_ganador_id": None, # se llenará cuando se genere la siguiente ronda
            "grupo_id": None    # no aplica para eliminación directa
        }

        if tipo_partido == "individual":
            partido_data = schemas.PartidoCreate(
                jugador1_id=participante1_id,
                jugador2_id=participante2_id,
                equipo1_id=None,
                equipo2_id=None,
                **partido_data_common
            )
        elif tipo_partido == "dobles":
            partido_data = schemas.PartidoCreate(
                jugador1_id=None,
                jugador2_id=None,
                equipo1_id=participante1_id,
                equipo2_id=participante2_id,
                **partido_data_common
            )
        else:
            raise ValueError("Tipo de partido inválido para generación de llave. Debe ser 'individual' o 'dobles'.")

        try:
            db_partido = create_partido(db, partido_data)
            partidos_generados.append(db_partido)
        except ValueError as e:
            print(f"Error al crear partido en llave de eliminación: {e}")
            db.rollback()

    
    return partidos_generados

def avanzar_ganador(db: Session, partido_actual_id: int, ganador_id: int, es_equipo: bool = False):
  
    partido_actual = get_partido(db, partido_actual_id)
    if not partido_actual:
        raise ValueError("Partido actual no encontrado.")
    
    if not partido_actual.partido_ganador_id:
        raise ValueError("Este partido no tiene un siguiente partido en la llave (partido_ganador_id es nulo).")
    
    siguiente_partido = get_partido(db, partido_actual.partido_ganador_id)
    if not siguiente_partido:
        raise ValueError("Siguiente partido en la llave no encontrado.")

    # Determina si el ganador es jugador o equipo
    if es_equipo:
        if siguiente_partido.equipo1_id is None:
            siguiente_partido.equipo1_id = ganador_id
        elif siguiente_partido.equipo2_id is None:
            siguiente_partido.equipo2_id = ganador_id
        else:
            raise ValueError("El siguiente partido ya tiene ambos equipos asignados.")
    else: # Es jugador
        if siguiente_partido.jugador1_id is None:
            siguiente_partido.jugador1_id = ganador_id
        elif siguiente_partido.jugador2_id is None:
            siguiente_partido.jugador2_id = ganador_id
        else:
            raise ValueError("El siguiente partido ya tiene ambos jugadores asignados.")
    
    db.commit()
    db.refresh(siguiente_partido)
    return siguiente_partido

def asignar_horario_mesa(db: Session, partido_id: int, horario: datetime, mesa: int):
  
    #Asigna un horario y mesa a un partido existente.
   
    partido = get_partido(db, partido_id)
    if not partido:
        raise ValueError("Partido no encontrado.")
    
    # Validar que la mesa sea válida para el torneo
    torneo = get_torneo(db, partido.torneo_id)
    if not torneo:
        raise ValueError(f"Torneo asociado al partido con ID {partido.torneo_id} no encontrado.")
    if mesa <= 0 or mesa > torneo.mesas_disponibles:
        raise ValueError(f"Mesa {mesa} no válida para el torneo. Mesas disponibles: 1 a {torneo.mesas_disponibles}.")

    partido.horario = horario
    partido.mesa = mesa
    db.commit()
    db.refresh(partido)
    return partido

def registrar_resultado_set(db: Session, resultado_set_data: schemas.ResultadoSetCreate):

    #Registra el resultado de un set para un partido.

    partido = get_partido(db, resultado_set_data.partido_id)
    if not partido:
        raise ValueError(f"Partido con ID {resultado_set_data.partido_id} no encontrado.")
    
    categoria = get_categoria(db, partido.categoria_id)
    if not categoria:
        raise ValueError(f"Categoría del partido con ID {partido.categoria_id} no encontrada.")
    
    # Validar que el numero de set sea consecutivo y no exceda el máximo
    sets_existentes = get_resultados_set_by_partido(db, partido.id)
    if resultado_set_data.numero_set > len(sets_existentes) + 1:
        raise ValueError(f"El set número {resultado_set_data.numero_set} no es el siguiente set consecutivo. El siguiente set esperado es {len(sets_existentes) + 1}.")
    if resultado_set_data.numero_set > categoria.sets_por_partido:
        raise ValueError(f"Número de set inválido ({resultado_set_data.numero_set}). La categoría '{categoria.nombre}' solo permite hasta {categoria.sets_por_partido} sets.")
    
    # Validar puntos
    if resultado_set_data.puntos_jugador1 < 0 or resultado_set_data.puntos_jugador2 < 0:
        raise ValueError("Los puntos no pueden ser negativos.")
    
    resultado = models.ResultadoSet(**resultado_set_data.dict())
    db.add(resultado)
    try:
        db.commit()
        db.refresh(resultado)
        return resultado
    except IntegrityError:
        db.rollback()
        raise ValueError(f"El set número {resultado_set_data.numero_set} ya ha sido registrado para el partido {resultado_set_data.partido_id}.")


def determinar_ganador_partido(db: Session, partido_id: int):
   
    #Determina el ganador de un partido basándose en los resultados de los sets
    #y las reglas de la categoría.
    #Retorna el ID del ganador (jugador o equipo) o None si el partido no ha terminado.
   
    partido = get_partido(db, partido_id)
    if not partido:
        raise ValueError("Partido no encontrado.")
    
    categoria = get_categoria(db, partido.categoria_id)
    if not categoria:
        raise ValueError("Categoría del partido no encontrada.")

    sets_para_ganar = (categoria.sets_por_partido // 2) + 1
    
    resultados_sets = get_resultados_set_by_partido(db, partido_id)
    
    sets_ganados_j1 = 0
    sets_ganados_j2 = 0

    for rs in resultados_sets:
        # regla de tenis de mesa: ganar por al menos 2 puntos, y alcanzar el mínimo de puntos_por_set
        # si el set no ha alcanzado el mínimo de puntos, no cuenta como ganado (a menos que sea el último set y ya no haya más sets posibles)
        if rs.puntos_jugador1 >= categoria.puntos_por_set and (rs.puntos_jugador1 - rs.puntos_jugador2 >= 2):
            sets_ganados_j1 += 1
        elif rs.puntos_jugador2 >= categoria.puntos_por_set and (rs.puntos_jugador2 - rs.puntos_jugador1 >= 2):
            sets_ganados_j2 += 1
        # caso para sets con puntuación muy alta (ej. 11-10, 12-11)
        elif rs.puntos_jugador1 >= (categoria.puntos_por_set -1) and rs.puntos_jugador2 >= (categoria.puntos_por_set -1) and abs(rs.puntos_jugador1 - rs.puntos_jugador2) == 2:
            if rs.puntos_jugador1 > rs.puntos_jugador2: sets_ganados_j1 += 1
            else: sets_ganados_j2 += 1


    if sets_ganados_j1 >= sets_para_ganar:
        return partido.jugador1_id if partido.tipo == "individual" else partido.equipo1_id
    elif sets_ganados_j2 >= sets_para_ganar:
        return partido.jugador2_id if partido.tipo == "individual" else partido.equipo2_id
    
    return None # El partido aún no ha terminado o no hay un ganador claro
