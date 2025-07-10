from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas, db
from app.db import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# dependencia para obtener sesión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JUGADORES
@app.post("/jugadores/", response_model=schemas.JugadorOut)
def crear_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
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
def actualizar_jugador(jugador_id: int, jugador: schemas.JugadorUpdate, db: Session = Depends(get_db)):
    db_jugador = crud.update_jugador(db, jugador_id, jugador)
    if db_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return db_jugador

@app.delete("/jugadores/{jugador_id}", response_model=schemas.JugadorOut)
def eliminar_jugador(jugador_id: int, db: Session = Depends(get_db)):
    db_jugador = crud.delete_jugador(db, jugador_id)
    if db_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return db_jugador


# TORNEOS
@app.post("/torneos/", response_model=schemas.TorneoOut)
def crear_torneo(torneo: schemas.TorneoCreate, db: Session = Depends(get_db)):
    return crud.create_torneo(db, torneo)

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
def actualizar_torneo(torneo_id: int, torneo: schemas.TorneoUpdate, db: Session = Depends(get_db)):
    db_torneo = crud.update_torneo(db, torneo_id, torneo)
    if db_torneo is None:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return db_torneo

@app.delete("/torneos/{torneo_id}", response_model=schemas.TorneoOut)
def eliminar_torneo(torneo_id: int, db: Session = Depends(get_db)):
    db_torneo = crud.delete_torneo(db, torneo_id)
    if db_torneo is None:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return db_torneo
# CATEGORIAS
@app.post("/categorias/", response_model=schemas.CategoriaOut)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.create_categoria(db, categoria)

@app.get("/categorias/", response_model=list[schemas.CategoriaOut])
def listar_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categorias(db, skip=skip, limit=limit)

@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaOut)
def leer_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.get_categoria(db, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@app.put("/categorias/{categoria_id}", response_model=schemas.CategoriaOut)
def actualizar_categoria(categoria_id: int, categoria: schemas.CategoriaUpdate, db: Session = Depends(get_db)):
    db_categoria = crud.update_categoria(db, categoria_id, categoria)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@app.delete("/categorias/{categoria_id}", response_model=schemas.CategoriaOut)
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = crud.delete_categoria(db, categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria
# ASOCIACIÓN
@app.post("/asociaciones/", response_model=schemas.AsociacionOut)
def crear_asociacion(asociacion: schemas.AsociacionCreate, db: Session = Depends(get_db)):
    return crud.create_asociacion(db, asociacion)

@app.get("/asociaciones/", response_model=list[schemas.AsociacionOut])
def listar_asociaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_asociaciones(db, skip=skip, limit=limit)

@app.get("/asociaciones/{asociacion_id}", response_model=schemas.AsociacionOut)
def leer_asociacion(asociacion_id: int, db: Session = Depends(get_db)):
    asociacion = crud.get_asociacion(db, asociacion_id)
    if asociacion is None:
        raise HTTPException(status_code=404, detail="Asociación no encontrada")
    return asociacion

@app.put("/asociaciones/{asociacion_id}", response_model=schemas.AsociacionOut)
def actualizar_asociacion(asociacion_id: int, asociacion: schemas.AsociacionUpdate, db: Session = Depends(get_db)):
    db_asociacion = crud.update_asociacion(db, asociacion_id, asociacion)
    if db_asociacion is None:
        raise HTTPException(status_code=404, detail="Asociación no encontrada")
    return db_asociacion

@app.delete("/asociaciones/{asociacion_id}", response_model=schemas.AsociacionOut)
def eliminar_asociacion(asociacion_id: int, db: Session = Depends(get_db)):
    db_asociacion = crud.delete_asociacion(db, asociacion_id)
    if db_asociacion is None:
        raise HTTPException(status_code=404, detail="Asociación no encontrada")
    return db_asociacion
# PARTIDOS
@app.post("/partidos/", response_model=schemas.PartidoOut)
def crear_partido(partido: schemas.PartidoCreate, db: Session = Depends(get_db)):
    creado = crud.create_partido(db, partido)
    if not creado:
        raise HTTPException(status_code=400, detail="Jugador(es) o equipo(s) no válidos")
    return creado

@app.get("/partidos/", response_model=list[schemas.PartidoOut])
def listar_partidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_partidos(db, skip=skip, limit=limit)

@app.get("/partidos/{partido_id}", response_model=schemas.PartidoOut)
def leer_partido(partido_id: int, db: Session = Depends(get_db)):
    partido = crud.get_partido(db, partido_id)
    if partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

@app.put("/partidos/{partido_id}", response_model=schemas.PartidoOut)
def actualizar_partido(partido_id: int, partido: schemas.PartidoUpdate, db: Session = Depends(get_db)):
    db_partido = crud.update_partido(db, partido_id, partido)
    if db_partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return db_partido

@app.delete("/partidos/{partido_id}", response_model=schemas.PartidoOut)
def eliminar_partido(partido_id: int, db: Session = Depends(get_db)):
    db_partido = crud.delete_partido(db, partido_id)
    if db_partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return db_partido

# RESULTADO SET
@app.post("/resultadoset/", response_model=schemas.ResultadoSetOut)
def crear_resultado_set(data: schemas.ResultadoSetCreate, db: Session = Depends(db.SessionLocal)):
    return crud.create_resultado_set(db, data)

@app.get("/resultadoset/", response_model=List[schemas.ResultadoSetOut])
def listar_resultados_set(skip: int = 0, limit: int = 100, db: Session = Depends(db.SessionLocal)):
    return crud.get_resultados_set(db, skip, limit)

@app.get("/resultadoset/{resultado_id}", response_model=schemas.ResultadoSetOut)
def obtener_resultado_set(resultado_id: int, db: Session = Depends(db.SessionLocal)):
    resultado = crud.get_resultado_set(db, resultado_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    return resultado

@app.put("/resultadoset/{resultado_id}", response_model=schemas.ResultadoSetOut)
def actualizar_resultado_set(resultado_id: int, data: schemas.ResultadoSetUpdate, db: Session = Depends(db.SessionLocal)):
    resultado = crud.update_resultado_set(db, resultado_id, data)
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    return resultado

@app.delete("/resultadoset/{resultado_id}", response_model=schemas.ResultadoSetOut)
def eliminar_resultado_set(resultado_id: int, db: Session = Depends(db.SessionLocal)):
    resultado = crud.delete_resultado_set(db, resultado_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    return resultado
# GRUPO
@app.post("/grupos/", response_model=schemas.GrupoOut)
def crear_grupo(grupo: schemas.GrupoCreate, db: Session = Depends(get_db)):
    return crud.create_grupo(db, grupo)

@app.get("/grupos/", response_model=list[schemas.GrupoOut])
def listar_grupos(db: Session = Depends(get_db)):
    return crud.get_grupos(db)

@app.put("/grupos/{grupo_id}", response_model=schemas.GrupoOut)
def actualizar_grupo(grupo_id: int, update: schemas.GrupoUpdate, db: Session = Depends(get_db)):
    grupo_actualizado = crud.update_grupo(db, grupo_id, update)
    if not grupo_actualizado:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo_actualizado

@app.delete("/grupos/{grupo_id}")
def eliminar_grupo(grupo_id: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_grupo(db, grupo_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return {"mensaje": "Grupo eliminado correctamente"}

# EQUIPO DOBLES
@app.post("/equiposdobles/", response_model=schemas.EquipoDoblesOut)
def crear_equipo_dobles(equipo: schemas.EquipoDoblesCreate, db: Session = Depends(get_db)):
    return crud.create_equipo_dobles(db, equipo)

@app.get("/equiposdobles/", response_model=List[schemas.EquipoDoblesOut])
def listar_equipos_dobles(db: Session = Depends(get_db)):
    return crud.get_equipos_dobles(db)

@app.get("/equiposdobles/{equipo_id}", response_model=schemas.EquipoDoblesOut)
def obtener_equipo_dobles(equipo_id: int, db: Session = Depends(get_db)):
    equipo = crud.get_equipo_dobles(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

@app.delete("/equiposdobles/{equipo_id}", response_model=schemas.EquipoDoblesOut)
def eliminar_equipo_dobles(equipo_id: int, db: Session = Depends(get_db)):
    equipo = crud.delete_equipo_dobles(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

# INSCRIPCIONES
@app.post("/inscripciones/")
def inscribir_jugador(inscripcion: schemas.InscripcionCreate, db: Session = Depends(get_db)):
    resultado = crud.create_inscripcion(db, inscripcion)
    if resultado is None:
        raise HTTPException(status_code=400, detail="Jugador ya está inscrito en este torneo y categoría")
    return resultado

@app.delete("/inscripciones/")
def eliminar_inscripcion(jugador_id: int, torneo_id: int, categoria_id: int, db: Session = Depends(get_db)):
    resultado = crud.delete_inscripcion(db, jugador_id, torneo_id, categoria_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return {"mensaje": "Inscripción eliminada correctamente"}

@app.get("/inscripciones/")
def listar_inscripciones(db: Session = Depends(get_db)):
    return crud.get_inscripciones(db)

# INSCRIPCIONES DOBLES
@app.post("/inscripcionesdobles/")
def inscribir_equipo(inscripcion: schemas.InscripcionDobles, db: Session = Depends(get_db)):
    resultado = crud.create_inscripcion_dobles(db, inscripcion.equipo_id, inscripcion.torneo_id, inscripcion.categoria_id)
    if resultado is None:
        raise HTTPException(status_code=400, detail="El equipo ya está inscrito en este torneo y categoría")
    return resultado

@app.delete("/inscripcionesdobles/")
def eliminar_inscripcion_dobles(equipo_id: int, torneo_id: int, categoria_id: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_inscripcion_dobles(db, equipo_id, torneo_id, categoria_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return {"mensaje": "Inscripción de equipo eliminada correctamente"}

@app.get("/inscripcionesdobles/")
def listar_inscripciones_dobles(db: Session = Depends(get_db)):
    return crud.get_inscripciones_dobles(db)




