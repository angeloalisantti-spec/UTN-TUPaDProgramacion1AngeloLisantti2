# Informe Teórico

### Listas
Las listas (`list`) almacenan la colección de países. Cada elemento es un diccionario.
Permiten agregar, recorrer y ordenar registros. Se usan para filtrar y mostrar resultados.

### Diccionarios
Cada país se representa como un diccionario con claves: `nombre`, `poblacion`,
`superficie`, `continente`. Facilitan el acceso por nombre de campo.

### Funciones
El código se modulariza en funciones con una responsabilidad única:
- `leer_csv`, `guardar_csv` (archivos)
- `agregar_pais`, `actualizar_pais`, `buscar_por_nombre`, filtros, `ordenar_paises`
- Estadísticas en módulo separado.

### Condicionales
Se usan para validar entradas, controlar opciones del menú, verificar resultados
vacíos y decidir mensajes de éxito/error.

### Ordenamientos
Se utiliza `list.sort()` con `key` y `reverse` para ordenar por nombre, población
o superficie, ascendente o descendente.

### Estadísticas básicas
Se calculan máximo/mínimo de población, promedios y conteo por continente usando
`max`, `min`, `sum` y diccionarios de acumulación.

### Archivos CSV
Se lee con `csv.DictReader` y se escribe con `csv.DictWriter`, validando columnas
y tipos de datos. Se manejan errores de formato y archivos inexistentes.

## Flujo principal
1. Cargar CSV al iniciar.
2. Mostrar menú.
3. Según opción: alta, actualización, búsqueda, filtros, ordenamiento, estadísticas, listado, guardar.
4. Validar entradas y mostrar resultados.
5. Repetir hasta salir.