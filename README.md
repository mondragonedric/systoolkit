# SysToolkit

SysToolkit es una herramienta de línea de comandos (CLI) escrita en Python. Con comandos sencillos permite consultar el estado de una computadora desde la terminal: CPU, memoria RAM, discos, red, procesos activos y un análisis básico de archivos de log.

## Requisitos

- Python 3.8 o superior
- Windows (probado en Windows 11)
- La librería `psutil` (se instala sola con el proyecto)

## Instalación

```
git clone https://github.com/mondragonedric/systoolkit.git
cd systoolkit
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Uso

```
systoolkit system
systoolkit disk
systoolkit network
systoolkit processes
systoolkit logs <archivo>
```

## Comandos

### system

Muestra el nombre del equipo, el sistema operativo y el estado del CPU y la RAM:

- `cpu_count` cuenta los núcleos físicos y lógicos.
- `cpu_percent` mide el porcentaje de uso actual del CPU durante 1 segundo.
- `virtual_memory` devuelve la memoria RAM total, usada y disponible, y el porcentaje que se está usando.

### disk

Recorre todos los discos y particiones del equipo (internos y externos, como una USB):

- `disk_partitions` entrega la lista de discos y un ciclo `for` los recorre uno por uno.
- `disk_usage` obtiene, para cada disco, el espacio total, usado y libre, y el porcentaje de uso.
- Los valores se convierten de bytes a GB.
- Si un disco supera el 90% de uso, se muestra una advertencia.
- Los discos que no se pueden leer (por ejemplo, una unidad sin disco) se omiten con `try/except`.

### network

Muestra el estado de la red del equipo:

- `net_if_addrs` lista las interfaces de red con sus direcciones IPv4.
- `net_if_stats` indica si cada interfaz está activa o apagada.
- Con `socket` se intenta una conexión al DNS de Google (`8.8.8.8`, puerto 53) para comprobar si hay internet. Si falla, muestra "sin conexión".

### processes

Muestra los 10 procesos que más memoria usan:

- `process_iter` recorre todos los procesos activos y de cada uno se guarda el PID, el nombre y el porcentaje de memoria.
- La lista se ordena de mayor a menor con `sort`, usando una función `lambda` para indicar que se ordene por memoria.

### logs

Analiza un archivo de log y cuenta los mensajes por nivel:

- Lee el archivo línea por línea y cuenta cuántas son `INFO`, `WARNING` y `ERROR`.
- Muestra el total de líneas y la cantidad de cada nivel.
- Para los errores, guarda el mensaje (el texto que viene después de la palabra `ERROR`) en un diccionario y cuenta cuántas veces se repite cada uno.
- Los ordena con `sorted` y muestra los 3 más frecuentes.

Incluye un archivo de ejemplo para probarlo: `systoolkit logs ejemplo.log`

## Ejemplo de salida

`systoolkit system`

```
Equipo: MI-PC
Sistema: Windows 11

--- CPU ---
Núcleos físicos: 8
Núcleos lógicos: 16
Uso actual: 20.1%

--- RAM ---
Total: 13.8 GB
Usada: 8.5 GB
Disponible: 5.4 GB
Porcentaje usado: 61.1%
```

`systoolkit logs ejemplo.log`

```
Líneas totales: 10
INFO: 3
WARNING: 1
ERROR: 6

Errores más frecuentes:
  2x  No se pudo conectar a la base de datos
  1x  Tiempo de espera agotado
  1x  Permiso denegado
```

## Limitaciones y mejoras futuras

- Solo ha sido probado en Windows 11.
- El análisis de logs busca las palabras `INFO`, `WARNING` y `ERROR` en mayúsculas dentro de cada línea, así que los logs deben usar ese formato.
- La prueba de conexión depende de que se pueda alcanzar `8.8.8.8`.
- Mejoras posibles: elegir cuántos procesos mostrar, filtrar los logs por fecha y exportar los resultados a un archivo