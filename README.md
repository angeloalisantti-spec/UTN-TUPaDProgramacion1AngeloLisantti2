Requisitos previos
- Python 3.x instalado.
- El archivo paises.csv debe estar en la misma carpeta que los scripts (contiene el dataset base).
- Para la interfaz web se necesita conexión a internet para cargar Materialize desde CDN (opcional, solo afecta el estilo).
Modo terminal (consola)
1. Abrir una terminal en la carpeta del proyecto.
2. Ejecutar:
python main.py
3. Al iniciar se carga paises.csv y se muestra un resumen de registros cargados y posibles advertencias de formato.
4. Se presenta un menú con las siguientes opciones:
- 1 Agregar país (nombre, población, superficie, continente; no se permiten campos vacíos).
- 2 Actualizar población y/o superficie de un país (dejar vacío para no modificar).
- 3 Buscar país por nombre (coincidencia parcial, ignora mayúsculas y acentos).
- 4 Filtrar por continente.
- 5 Filtrar por rango de población (mínimo y máximo).
- 6 Filtrar por rango de superficie (mínimo y máximo).
- 7 Ordenar países por nombre, población o superficie (ascendente/descendente).
- 8 Mostrar estadísticas (mayor/menor población y superficie, promedios, cantidad por continente).
- 9 Listar todos los países.
- 10 Guardar cambios en paises.csv.
- 0 Salir.
5. Durante la carga de datos numéricos se puede escribir cancelar o dejar vacío para abortar la operación (según el campo).
6. Las validaciones evitan valores negativos, campos vacíos y duplicados por nombre.
Nota: los cambios en memoria solo se persisten si se usa la opción 10. Si se sale sin guardar, se pierden las modificaciones.
Modo web (interfaz gráfica)
1. Abrir una terminal en la carpeta del proyecto.
2. Ejecutar:
python app.py
3. El servidor se inicia en http://127.0.0.1:8000.
4. Abrir ese enlace en el navegador.
5. La página ofrece pestañas para:
- Listado (actualizar tabla).
- Agregar país.
- Actualizar país.
- Buscar país.
- Filtrar por continente y rangos.
- Ordenar por clave y orden.
- Estadísticas.
6. Toda la lógica se ejecuta en Python (servidor); la interfaz solo consume la API REST (/api/...).
API REST disponible (referencia)
- GET /api/paises → lista completa.
- GET /api/buscar?q=texto → búsqueda por nombre.
- GET /api/filtrar → filtros por continente/rangos.
- GET /api/ordenar?clave=...&asc=true|false → ordenamiento.
- GET /api/estadisticas → indicadores.
- POST /api/agregar → alta de país.
- POST /api/actualizar → actualización de población/superficie.
Recomendaciones
- Hacer una copia de paises.csv antes de pruebas masivas.
- En la web, los datos se mantienen en memoria del servidor; reiniciar app.py recarga el CSV base.
