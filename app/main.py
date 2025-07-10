from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime


from . import crud, models, schemas
from .db import get_db 


from dotenv import load_dotenv
load_dotenv()


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API de Gestión de Torneos de Tenis de Mesa",
    description="API para gestionar jugadores, torneos, partidos y resultados de tenis de mesa.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)


# Endpoint de prueba
@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Gestión de Torneos de Tenis de Mesa!"}

# endpoints para jugadores
@app.post("/jugadores/", response_model=schemas.JugadorOut, status_code=status.HTTP_201_CREATED)
def crear_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):

    if jugador.asociacion_id:
        asociacion = crud.get_asociacion(db, jugador.asociacion_id)
        if not asociacion:
            raise HTTPException(status_code=400, detail=f"Asociación con ID {jugador.asociacion_id} no encontrada.")
    return crud.create_jugador(db, jugador)

@app.get("/jugadores/{jugador_id}", response_model=schemas.JugadorOut)
def leer_jugador(jugador_id: int, db: Session = Depends(get_db)):
    db_jugador = crud.get_jugador(db, jugador_id)
    if db_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return db_jugador

@app.get("/jugadores/", response_model=List[schemas.JugadorOut])
def listar_jugadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_jugadores(db, skip, limit)

@app.put("/jugadores/{jugador_id}", response_model=schemas.JugadorOut)
def actualizar_jugador(jugador_id: int, jugador_data: schemas.JugadorUpdate, db: Session = Depends(get_db)):
    if jugador_data.asociacion_id:
        asociacion = crud.get_asociacion(db, jugador_data.asociacion_id)
        if not asociacion:
            raise HTTPException(status_code=400, detail=f"Asociación con ID {jugador_data.asociacion_id} no encontrada.")
    db_jugador = crud.update_jugador(db, jugador_id, jugador_data)
    if db_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return db_jugador

@app.delete("/jugadores/{jugador_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_jugador(jugador_id: int, db: Session = Depends(get_db)):
    db_jugador = crud.delete_jugador(db, jugador_id)
    if db_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"message": "Jugador eliminado exitosamente"} 

# endpoints para TORNEOS
@app.post("/torneos/", response_model=schemas.TorneoOut, status_code=status.HTTP_201_CREATED)
def crear_torneo(torneo: schemas.TorneoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_torneo(db, torneo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/torneos/{torneo_id}", response_model=schemas.TorneoOut)
def leer_torneo(torneo_id: int, db: Session = Depends(get_db)):
    db_torneo = crud.get_torneo(db, torneo_id)
    if db_torneo is None:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return db_torneo

@app.get("/torneos/", response_model=List[schemas.TorneoOut])
def listar_torneos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_torneos(db, skip, limit)

@app.put("/torneos/{torneo_id}", response_model=schemas.TorneoOut)
def actualizar_torneo(torneo_id: int, torneo_data: schemas.TorneoUpdate, db: Session = Depends(get_db)):
    try:
        db_torneo = crud.update_torneo(db, torneo_id, torneo_data)
        if db_torneo is None:
            raise HTTPException(status_code=404, detail="Torneo no encontrado")
        return db_torneo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/torneos/{torneo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_torneo(torneo_id: int, db: Session = Depends(get_db)):
    db_torneo = crud.delete_torneo(db, torneo_id)
    if db_torneo is None:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return {"message": "Torneo eliminado exitosamente"}

# endpoints para CATEGORIAS
@app.post("/categorias/", response_model=schemas.CategoriaOut, status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_categoria(db, categoria)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/categorias/", response_model=List[schemas.CategoriaOut])
def listar_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categorias(db, skip=skip, limit=limit)

@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaOut)
def leer_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = crud.get_categoria(db, categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@app.put("/categorias/{categoria_id}", response_model=schemas.CategoriaOut)
def actualizar_categoria(categoria_id: int, categoria_data: schemas.CategoriaUpdate, db: Session = Depends(get_db)):
    try:
        db_categoria = crud.update_categoria(db, categoria_id, categoria_data)
        if db_categoria is None:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return db_categoria
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/categorias/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = crud.delete_categoria(db, categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"message": "Categoría eliminada exitosamente"}

# endpoints para ASOCIACIONES
@app.post("/asociaciones/", response_model=schemas.AsociacionOut, status_code=status.HTTP_201_CREATED)
def crear_asociacion(asociacion: schemas.AsociacionCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_asociacion(db, asociacion)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/asociaciones/", response_model=List[schemas.AsociacionOut])
def listar_asociaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_asociaciones(db, skip=skip, limit=limit)

@app.get("/asociaciones/{asociacion_id}", response_model=schemas.AsociacionOut)
def leer_asociacion(asociacion_id: int, db: Session = Depends(get_db)):
    asociacion = crud.get_asociacion(db, asociacion_id)
    if asociacion is None:
        raise HTTPException(status_code=404, detail="Asociación no encontrada")
    return asociacion

@app.put("/asociaciones/{asociacion_id}", response_model=schemas.AsociacionOut)
def actualizar_asociacion(asociacion_id: int, asociacion_data: schemas.AsociacionUpdate, db: Session = Depends(get_db)):
    try:
        db_asociacion = crud.update_asociacion(db, asociacion_id, asociacion_data)
        if db_asociacion is None:
            raise HTTPException(status_code=404, detail="Asociación no encontrada")
        return db_asociacion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/asociaciones/{asociacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_asociacion(asociacion_id: int, db: Session = Depends(get_db)):
    db_asociacion = crud.delete_asociacion(db, asociacion_id)
    if db_asociacion is None:
        raise HTTPException(status_code=404, detail="Asociación no encontrada")
    return {"message": "Asociación eliminada exitosamente"}

# endpoints para PARTIDOS
@app.post("/partidos/", response_model=schemas.PartidoOut, status_code=status.HTTP_201_CREATED)
def crear_partido(partido: schemas.PartidoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_partido(db, partido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/partidos/", response_model=List[schemas.PartidoOut])
def listar_partidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_partidos(db, skip=skip, limit=limit)

@app.get("/partidos/{partido_id}", response_model=schemas.PartidoOut)
def leer_partido(partido_id: int, db: Session = Depends(get_db)):
    partido = crud.get_partido(db, partido_id)
    if partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

@app.put("/partidos/{partido_id}", response_model=schemas.PartidoOut)
def actualizar_partido(partido_id: int, partido_data: schemas.PartidoUpdate, db: Session = Depends(get_db)):
    try:
        db_partido = crud.update_partido(db, partido_id, partido_data)
        if db_partido is None:
            raise HTTPException(status_code=404, detail="Partido no encontrado")
        return db_partido
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/partidos/{partido_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_partido(partido_id: int, db: Session = Depends(get_db)):
    db_partido = crud.delete_partido(db, partido_id)
    if db_partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return {"message": "Partido eliminado exitosamente"}

# endpoints para RESULTADO SET
@app.post("/resultados-set/", response_model=schemas.ResultadoSetOut, status_code=status.HTTP_201_CREATED)
def crear_resultado_set(resultado_set: schemas.ResultadoSetCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_resultado_set(db, resultado_set)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/resultados-set/", response_model=List[schemas.ResultadoSetOut])
def listar_resultados_set(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_resultados_set(db, skip, limit)

@app.get("/resultados-set/{resultado_id}", response_model=schemas.ResultadoSetOut)
def obtener_resultado_set(resultado_id: int, db: Session = Depends(get_db)):
    resultado = crud.get_resultado_set(db, resultado_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado de set no encontrado")
    return resultado

@app.put("/resultados-set/{resultado_id}", response_model=schemas.ResultadoSetOut)
def actualizar_resultado_set(resultado_id: int, resultado_data: schemas.ResultadoSetUpdate, db: Session = Depends(get_db)):
    try:
        resultado = crud.update_resultado_set(db, resultado_id, resultado_data)
        if not resultado:
            raise HTTPException(status_code=404, detail="Resultado de set no encontrado")
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/resultados-set/{resultado_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_resultado_set(resultado_id: int, db: Session = Depends(get_db)):
    resultado = crud.delete_resultado_set(db, resultado_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado de set no encontrado")
    return {"message": "Resultado de set eliminado exitosamente"}

# endpoints para GRUPOS
@app.post("/grupos/", response_model=schemas.GrupoOut, status_code=status.HTTP_201_CREATED)
def crear_grupo(grupo: schemas.GrupoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_grupo(db, grupo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/grupos/", response_model=List[schemas.GrupoOut])
def listar_grupos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_grupos(db, skip=skip, limit=limit)

@app.get("/grupos/{grupo_id}", response_model=schemas.GrupoOut)
def leer_grupo(grupo_id: int, db: Session = Depends(get_db)):
    grupo = crud.get_grupo(db, grupo_id)
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo

@app.put("/grupos/{grupo_id}", response_model=schemas.GrupoOut)
def actualizar_grupo(grupo_id: int, grupo_data: schemas.GrupoUpdate, db: Session = Depends(get_db)):
    try:
        grupo_actualizado = crud.update_grupo(db, grupo_id, grupo_data)
        if not grupo_actualizado:
            raise HTTPException(status_code=404, detail="Grupo no encontrado")
        return grupo_actualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/grupos/{grupo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_grupo(grupo_id: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_grupo(db, grupo_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return {"message": "Grupo eliminado correctamente"}

# endpoints para EQUIPOS DOBLES
@app.post("/equipos-dobles/", response_model=schemas.EquipoDoblesOut, status_code=status.HTTP_201_CREATED)
def crear_equipo_dobles(equipo: schemas.EquipoDoblesCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_equipo_dobles(db, equipo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/equipos-dobles/", response_model=List[schemas.EquipoDoblesOut])
def listar_equipos_dobles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_equipos_dobles(db, skip=skip, limit=limit)

@app.get("/equipos-dobles/{equipo_id}", response_model=schemas.EquipoDoblesOut)
def obtener_equipo_dobles(equipo_id: int, db: Session = Depends(get_db)):
    equipo = crud.get_equipo_dobles(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo de dobles no encontrado")
    return equipo

@app.put("/equipos-dobles/{equipo_id}", response_model=schemas.EquipoDoblesOut)
def actualizar_equipo_dobles(equipo_id: int, equipo_data: schemas.EquipoDoblesUpdate, db: Session = Depends(get_db)):
    try:
        db_equipo = crud.update_equipo_dobles(db, equipo_id, equipo_data)
        if db_equipo is None:
            raise HTTPException(status_code=404, detail="Equipo de dobles no encontrado")
        return db_equipo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/equipos-dobles/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipo_dobles(equipo_id: int, db: Session = Depends(get_db)):
    equipo = crud.delete_equipo_dobles(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo de dobles no encontrado")
    return {"message": "Equipo de dobles eliminado exitosamente"}

# endpoints para INSCRIPCIONES INDIVIDUALES
@app.post("/inscripciones/individual/", response_model=schemas.InscripcionOut, status_code=status.HTTP_201_CREATED)
def inscribir_jugador(inscripcion: schemas.InscripcionCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_inscripcion(db, inscripcion)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/inscripciones/individual/", response_model=List[schemas.InscripcionOut])
def listar_inscripciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_inscripciones(db, skip=skip, limit=limit)

@app.get("/inscripciones/individual/{jugador_id}/{torneo_id}/{categoria_id}", response_model=schemas.InscripcionOut)
def obtener_inscripcion(jugador_id: int, torneo_id: int, categoria_id: int, db: Session = Depends(get_db)):
    db_inscripcion = crud.get_inscripcion(db, jugador_id, torneo_id, categoria_id)
    if db_inscripcion is None:
        raise HTTPException(status_code=404, detail="Inscripción individual no encontrada")
    return db_inscripcion

@app.delete("/inscripciones/individual/{jugador_id}/{torneo_id}/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_inscripcion(jugador_id: int, torneo_id: int, categoria_id: int, db: Session = Depends(get_db)):
    success = crud.delete_inscripcion(db, jugador_id, torneo_id, categoria_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inscripción individual no encontrada")
    return {"message": "Inscripción individual eliminada correctamente"}

# endpoints para INSCRIPCIONES DOBLES
@app.post("/inscripciones/dobles/", response_model=schemas.InscripcionDoblesOut, status_code=status.HTTP_201_CREATED)
def inscribir_equipo_dobles(inscripcion: schemas.InscripcionDoblesCreate, db: Session = Depends(get_db)):
    try:
        # pasa el schema directamente a la función crud
        return crud.create_inscripcion_dobles(db, inscripcion)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/inscripciones/dobles/", response_model=List[schemas.InscripcionDoblesOut])
def listar_inscripciones_dobles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_inscripciones_dobles(db, skip=skip, limit=limit)

@app.get("/inscripciones/dobles/{equipo_id}/{torneo_id}/{categoria_id}", response_model=schemas.InscripcionDoblesOut)
def obtener_inscripcion_dobles(equipo_id: int, torneo_id: int, categoria_id: int, db: Session = Depends(get_db)):
    db_inscripcion = crud.get_inscripcion_dobles(db, equipo_id, torneo_id, categoria_id)
    if db_inscripcion is None:
        raise HTTPException(status_code=404, detail="Inscripción de dobles no encontrada")
    return db_inscripcion

@app.delete("/inscripciones/dobles/{equipo_id}/{torneo_id}/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_inscripcion_dobles(equipo_id: int, torneo_id: int, categoria_id: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_inscripcion_dobles(db, equipo_id, torneo_id, categoria_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Inscripción de dobles no encontrada")
    return {"message": "Inscripción de equipo eliminada correctamente"}

# endpoints para Participantes en Grupos
@app.post("/grupos/{grupo_id}/participantes/", response_model=schemas.GrupoParticipanteOut, status_code=status.HTTP_201_CREATED)
def add_jugador_to_grupo_endpoint(grupo_id: int, participante: schemas.GrupoParticipanteCreate, db: Session = Depends(get_db)):
    if grupo_id != participante.grupo_id:
        raise HTTPException(status_code=400, detail="El ID del grupo en la URL no coincide con el ID del grupo en el cuerpo de la solicitud.")
    try:
        return crud.create_grupo_participante(db=db, grupo_participante=participante)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/grupos/{grupo_id}/participantes/", response_model=List[schemas.GrupoParticipanteOut])
def read_grupo_participantes_endpoint(grupo_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    participantes = crud.get_grupo_participantes(db, skip=skip, limit=limit)
    # filtra los participantes por el grupo_id si el crud no lo hace
    filtered_participantes = [p for p in participantes if p.grupo_id == grupo_id]
    return filtered_participantes

@app.delete("/grupos/{grupo_id}/participantes/{jugador_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grupo_participante_endpoint(grupo_id: int, jugador_id: int, db: Session = Depends(get_db)):
    success = crud.delete_grupo_participante(db, grupo_id, jugador_id)
    if not success:
        raise HTTPException(status_code=404, detail="Participante no encontrado en este grupo")
    return {"message": "Participante eliminado del grupo exitosamente"}

# endpoints de Lógica de Negocio
@app.post("/grupos/{grupo_id}/generar-partidos/", response_model=List[schemas.PartidoOut], status_code=status.HTTP_201_CREATED)
def generate_group_matches_endpoint(grupo_id: int, db: Session = Depends(get_db)):
    try:
        partidos = crud.generar_partidos_grupo(db, grupo_id)
        if not partidos:
            raise HTTPException(status_code=400, detail="No se pudieron generar partidos para el grupo. Verifique participantes o si ya existen.")
        return partidos
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/torneos/{torneo_id}/categorias/{categoria_id}/generar-llave-individual/", response_model=List[schemas.PartidoOut], status_code=status.HTTP_201_CREATED)
def generate_elimination_bracket_individual_endpoint(torneo_id: int, categoria_id: int, db: Session = Depends(get_db)):
    # Obtener participantes inscritos individualmente en esta categora para este torneo
    inscripciones_individuales = db.query(models.inscripcion).filter(
        models.inscripcion.c.torneo_id == torneo_id,
        models.inscripcion.c.categoria_id == categoria_id
    ).all()
    
    participantes_ids = [insc.jugador_id for insc in inscripciones_individuales]

    if not participantes_ids:
        raise HTTPException(status_code=400, detail="No hay jugadores inscritos en esta categoría para generar la llave individual.")

    try:
        partidos = crud.generar_llave_eliminacion(db, torneo_id, categoria_id, participantes_ids, tipo_partido="individual")
        if not partidos:
            raise HTTPException(status_code=400, detail="No se pudieron generar partidos para la llave de eliminación individual.")
        return partidos
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/torneos/{torneo_id}/categorias/{categoria_id}/generar-llave-dobles/", response_model=List[schemas.PartidoOut], status_code=status.HTTP_201_CREATED)
def generate_elimination_bracket_dobles_endpoint(torneo_id: int, categoria_id: int, db: Session = Depends(get_db)):
    # obtener equipos inscritos en esta categoria para este torneo
    inscripciones_dobles = db.query(models.inscripcion_dobles).filter(
        models.inscripcion_dobles.c.torneo_id == torneo_id,
        models.inscripcion_dobles.c.categoria_id == categoria_id
    ).all()
    
    participantes_ids = [insc.equipo_id for insc in inscripciones_dobles]

    if not participantes_ids:
        raise HTTPException(status_code=400, detail="No hay equipos inscritos en esta categoría para generar la llave de dobles.")

    try:
        partidos = crud.generar_llave_eliminacion(db, torneo_id, categoria_id, participantes_ids, tipo_partido="dobles")
        if not partidos:
            raise HTTPException(status_code=400, detail="No se pudieron generar partidos para la llave de eliminación de dobles.")
        return partidos
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/partidos/{partido_id}/asignar-horario-mesa/", response_model=schemas.PartidoOut)
def assign_match_schedule_table_endpoint(partido_id: int, horario: datetime, mesa: int, db: Session = Depends(get_db)):
    try:
        partido_actualizado = crud.asignar_horario_mesa(db, partido_id, horario, mesa)
        return partido_actualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/partidos/{partido_id}/registrar-set/", response_model=schemas.ResultadoSetOut, status_code=status.HTTP_201_CREATED)
def register_set_result_endpoint(partido_id: int, resultado_set: schemas.ResultadoSetCreate, db: Session = Depends(get_db)):
    if partido_id != resultado_set.partido_id:
        raise HTTPException(status_code=400, detail="El ID del partido en la URL no coincide con el ID del partido en el cuerpo de la solicitud.")
    try:
        return crud.registrar_resultado_set(db, resultado_set)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/partidos/{partido_id}/ganador/", response_model=Optional[int]) # devuelve int de id de jugador o none
def get_match_winner_endpoint(partido_id: int, db: Session = Depends(get_db)):
    try:
        ganador_id = crud.determinar_ganador_partido(db, partido_id)
        if ganador_id is None:
            return None 
        return ganador_id
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/partidos/{partido_id}/avanzar-ganador/", response_model=schemas.PartidoOut)
def advance_winner_endpoint(partido_id: int, ganador_id: int, es_equipo: bool = False, db: Session = Depends(get_db)):
    try:
        partido_siguiente = crud.avanzar_ganador(db, partido_id, ganador_id, es_equipo)
        return partido_siguiente
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
