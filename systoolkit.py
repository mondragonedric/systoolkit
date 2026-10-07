import sys
import socket
import platform
import psutil

def cmd_logs():
    if len(sys.argv) < 3:
        print("Uso: systoolkit logs <archivo>")
        return

    ruta = sys.argv[2]
    conteo = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    errores = {}
    total = 0

    try:
        with open(ruta, "r", encoding="utf-8", errors="replace") as archivo:
            for linea in archivo:
                total += 1
                for nivel in conteo:
                    if nivel in linea:
                        conteo[nivel] += 1
                if "ERROR" in linea:
                    mensaje = linea.split("ERROR", 1)[1].strip()
                    errores[mensaje] = errores.get(mensaje, 0) + 1
    except FileNotFoundError:
        print(f"No encontré el archivo: {ruta}")
        return

    print(f"Líneas totales: {total}")
    for nivel, cantidad in conteo.items():
        print(f"{nivel}: {cantidad}")

    if errores:
        print()
        print("Errores más frecuentes:")
        ordenados = sorted(errores.items(), key=lambda x: x[1], reverse=True)
        for mensaje, veces in ordenados[:3]:
            print(f"  {veces}x  {mensaje}")

def cmd_system():
    print(f"Equipo: {platform.node()}")
    print(f"Sistema: {platform.system()} {platform.release()}")
    print()
    print("--- CPU ---")
    print(f"Núcleos físicos: {psutil.cpu_count(logical=False)}")
    print(f"Núcleos lógicos: {psutil.cpu_count()}")
    print(f"Uso actual: {psutil.cpu_percent(interval=1)}%")
    print()
    print("--- RAM ---")
    mem = psutil.virtual_memory()
    print(f"Total: {mem.total / (1024 ** 3):.1f} GB")
    print(f"Usada: {mem.used / (1024 ** 3):.1f} GB")
    print(f"Disponible: {mem.available / (1024 ** 3):.1f} GB")
    print(f"Porcentaje usado: {mem.percent}%")


def cmd_disk():
    for particion in psutil.disk_partitions():
        try:
            uso = psutil.disk_usage(particion.mountpoint)
        except (PermissionError, OSError):
            continue

        print(f"Disco {particion.device} ({particion.fstype})")
        print(f"  Total: {uso.total / (1024 ** 3):.1f} GB")
        print(f"  Usado: {uso.used / (1024 ** 3):.1f} GB")
        print(f"  Libre: {uso.free / (1024 ** 3):.1f} GB")
        print(f"  Porcentaje usado: {uso.percent}%")
        if uso.percent > 90:
            print("  Memoria del disco casi llena, favor de revisar")
        print()


def cmd_processes():
    procesos = []
    for p in psutil.process_iter(["pid", "name", "memory_percent"]):
        procesos.append(p.info)

    procesos.sort(key=lambda x: x["memory_percent"] or 0, reverse=True)

    print(f"Procesos activos: {len(procesos)}")
    print()
    print(f"{'PID':<8}{'Nombre':<30}{'Memoria %'}")
    for p in procesos[:10]:
        print(f"{p['pid']:<8}{(p['name'] or '?'):<30}{(p['memory_percent'] or 0):.1f}")


def cmd_network():
    print(f"Equipo: {socket.gethostname()}")
    print()
    print("--- Interfaces ---")
    estados = psutil.net_if_stats()
    for nombre, direcciones in psutil.net_if_addrs().items():
        estado = "apagada"
        if nombre in estados and estados[nombre].isup:
            estado = "activa"
        for d in direcciones:
            if d.family == socket.AF_INET:
                print(f"{nombre} ({estado}): {d.address}")
    print()
    print("--- Conectividad ---")
    try:
        with socket.create_connection(("8.8.8.8", 53), timeout=3):
            print("Internet: conectado")
    except OSError:
        print("Internet: sin conexión")


def main():
    if len(sys.argv) < 2:
        print("Uso: python systoolkit.py [system|network|processes|disk|logs]")
        sys.exit()

    comando = sys.argv[1]

    if comando == "system":
        cmd_system()
    elif comando == "logs":
        cmd_logs()
    elif comando == "disk":
        cmd_disk()
    elif comando == "processes":
        cmd_processes()
    elif comando == "network":
        cmd_network()
    else:
        print("No conozco ese comando")


if __name__ == "__main__":
    main()