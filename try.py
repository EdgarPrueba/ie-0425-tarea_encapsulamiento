#!/usr/bin/python3


"""
Simulación de comunicación en red entre dos PCs a través de switches y routers.


Este programa permite simular el proceso de comunicación de mensajes entre PC1
y PC2.
El usuario puede elegir la dirección de la comunicación, seleccionar
la aplicación y puerto de destino, y observar las etapas de encapsulación,
paso por switches/routers y desencapsulación de los datos.

Tareas principales:
- Mostrar un menú para elegir la dirección de la comunicación
    (PC1 -> PC2 o PC2 -> PC1).
- Solicitar al usuario un mensaje a enviar.
- Permitir seleccionar la aplicación y puerto correspondientes.
- Simular la encapsulación del mensaje con direcciones IP y MAC.
- Simular el paso del mensaje a través de switches y routers.
- Simular la desencapsulación del mensaje en el destino.

Autores: Edgar Alvarado, Josue Garcia, Wilber Hernandez
Grupo: Los Pecadores
Fecha: 01/09/2025
"""

# =========================
# Parámetros de red
# =========================
DISPOSITIVOS = {
    "PC1": {
        "IP": "110",
        "MAC": "07",
        "PuertoTCP": "443",  # Puerto TCP de la app cifrada cuando se usa HTTPS
        "MAC_ROUTER": "03"   # MAC del router vista desde PC1
    },
    "PC2": {
        "IP": "100",
        "MAC": "04",
        "PuertoTCP": "443",  # Puerto TCP de la app cifrada cuando se usa HTTPS
        "MAC_ROUTER": "08"   # MAC del router vista desde PC2
    },
    "Router": {
        "IP_PC1": "110",  # red de PC1
        "IP_PC2": "100",  # red de PC2
        "MAC_PC1": "03",  # interfaz hacia PC1
        "MAC_PC2": "08"   # interfaz hacia PC2
    }
}


def menu():
    """ Muestra el menú de opciones y retorna la opción seleccionada """

    print("Menú de Comunicación")
    print("1. PC1 a PC2")
    print("2. PC2 a PC1")
    return input("Selecciona una opción: ")


def seleccionar_app():
    """ Muestra el menú de aplicaciones y retorna la
    app seleccionada y su puerto asociado """

    print("Ingrese por medio de cual App se va a enviar el mensaje:")
    print("1. Telegram")
    print("2. Whatsapp")
    print("3. Facebook")
    opcion = input("Selecciona una opción: ")
    if opcion == "1":
        return "Telegram", 23
    elif opcion == "2":
        return "Whatsapp", 53
    else:
        return "Facebook", 93


def to_bin(value, bits):
    """Convierte un valor numérico a binario con padding de n bits"""

    return format(int(value), f'0{bits}b')


def encapsular(mensaje, puerto, puertotcp, src_ip, dst_ip, src_mac, dst_mac):
    """ Realiza el proceso de encapsulamiento y muestra las capas """

    print("Iniciando encapsulamiento.")
    # Mensaje e identidicador de la app (puerto).
    print(f"Capa 5 (Aplicación): {puerto} __ {mensaje}")
    # Agrega el puerto TCP.
    print(f"Capa 4 (Transporte): {puertotcp} __ {puerto} __ {mensaje}")
    # Agrega IP origen y destino.
    print(f"Capa 3 (Red): {src_ip} __ {dst_ip} __{puertotcp} __"
          f"{puerto} __ {mensaje}")
    # Agrega MAC origen y destino.
    print(f"Capa 2 (Enlace de Datos): {src_mac} __ {dst_mac} __ {src_ip} __"
          f"{dst_ip} __ {puertotcp} __ {puerto} __ {mensaje}")

    #  Construcción del frame binario:
    mac_src_bin = to_bin(src_mac, 8)
    mac_dst_bin = to_bin(dst_mac, 8)
    ip_src_bin = to_bin(src_ip, 8)
    ip_dst_bin = to_bin(dst_ip, 8)
    port_tco_bin = to_bin(puertotcp, 8)
    port_bin = to_bin(puerto, 8)
    msg_bin = ''.join(format(ord(c), '08b') for c in mensaje)

    # Concatenar todo en la Capa 1
    bits = (mac_src_bin + mac_dst_bin + ip_src_bin
            + ip_dst_bin + port_tco_bin + port_bin + msg_bin)

    print(f"Capa 1 (Física): {bits}")
    return mensaje


def switches_y_router(mensaje, puerto, puertotcp, src_ip, dst_ip,
                      router_left, router_right, src_mac, dst_mac):

    print("En Switch de la RED 1")
    if opcion == "1":
        sw_port_1 = "1"
        sw_port_2 = "2"
        sw_port_3 = "5"
        sw_port_4 = "6"
    else:
        sw_port_1 = "6"
        sw_port_2 = "5"
        sw_port_3 = "2"
        sw_port_4 = "1"

    print(f"En el switch entra por el puerto {sw_port_1}")
    print(f"En el switch sale por el puerto {sw_port_2}")
    print("Llega a Router")
    print("En el Router:")

    #  Frame que llega al router (PC origen -> Router entrada)
    mac_src_bin = to_bin(src_mac, 8)   # MAC origen PC1
    mac_dst_bin = to_bin(dst_mac, 8)   # MAC destino Router entrada
    ip_src_bin = to_bin(src_ip, 8)
    ip_dst_bin = to_bin(dst_ip, 8)
    port_bin = to_bin(puerto, 8)
    port_tcp_bin = to_bin(puertotcp, 8)
    msg_bin = ''.join(format(ord(c), '08b') for c in mensaje)
    bits_in = (mac_src_bin + mac_dst_bin + ip_src_bin
               + ip_dst_bin + port_tcp_bin + port_bin + msg_bin)

    print(f"Capa 1 (Física): {bits_in}")
    print(f"Capa 2 (Enlace de Datos):  {src_mac} __"
          f"{dst_mac} __ {src_ip} __ {dst_ip}"
          f"__ {puertotcp} __ {puerto} __ {mensaje}")
    print(f"Capa 3 (Red): {src_ip} __ {dst_ip}"
          f"__ {puertotcp} __  {puerto} __ {mensaje}")

    #  Router reencapsula (Router salida -> PC destino)
    mac_src_bin = to_bin(router_left, 8)
    mac_dst_bin = to_bin(router_right, 8)
    bits_out = (mac_src_bin + mac_dst_bin + ip_src_bin +
                ip_dst_bin + port_tcp_bin + port_bin + msg_bin)

    print(f"Capa 2 (Enlace de Datos): {router_left} __ {router_right}"
          f"__ {src_ip} __ {dst_ip} __ {puertotcp} __ {puerto} __ {mensaje}")
    print(f"Capa 1 (Física): {bits_out}")

    print("Sale de Router:")
    print("En Switch de la RED 2")
    print(f"En el switch entra por el puerto {sw_port_3}")
    print(f"En el switch sale por el puerto {sw_port_4}")


def desencapsular(mensaje, puerto, puertotcp,
                  src_ip, dst_ip, src_mac, dst_mac):
    # Frame que llega a la PC destino (Router -> PC destino)
    mac_src_bin = to_bin(src_mac, 8)
    mac_dst_bin = to_bin(dst_mac, 8)
    ip_src_bin = to_bin(src_ip, 8)
    ip_dst_bin = to_bin(dst_ip, 8)
    port_bin = to_bin(puerto, 8)
    port_tcp_bin = to_bin(puertotcp, 8)
    msg_bin = ''.join(format(ord(c), '08b') for c in mensaje)
    bits_out = (mac_src_bin + mac_dst_bin + ip_src_bin +
                ip_dst_bin + port_tcp_bin + port_bin + msg_bin)

    print("Llega a PC destino")
    print(f"Capa 1 (Física): {bits_out}")
    print(f"Capa 2 (Enlace de Datos): {src_mac} __ {dst_mac}"
          f"__ {src_ip} __ {dst_ip} __ {puertotcp} __  {puerto} __ {mensaje}")
    print(f"Capa 3 (Red): {src_ip} __ {dst_ip} __ {puertotcp}"
          f"__  {puerto} __ {mensaje}")
    print(f"Capa 4 (Transporte): {puertotcp} __ {puerto} __ {mensaje}")
    print(f"Capa 5 (Aplicación): {puerto} __ {mensaje}")


if __name__ == "__main__":
    opcion = menu()
    mensaje = input("Ingrese el mensaje que desea enviar: ")
    app, puerto = seleccionar_app()
    print(f"Has seleccionado {app}.")

    if opcion == "1":
        print("Has seleccionado comunicar de PC1 a PC2.")
        src, dst, rou = (DISPOSITIVOS["PC1"], DISPOSITIVOS["PC2"],
                         DISPOSITIVOS["Router"])
        encapsular(mensaje, puerto, src["PuertoTCP"], src["IP"],
                   dst["IP"], src["MAC"], src["MAC_ROUTER"])
        switches_y_router(mensaje, puerto, src["PuertoTCP"], src["IP"],
                          dst["IP"], rou["MAC_PC1"], rou["MAC_PC2"],
                          src["MAC"], src["MAC_ROUTER"])
        desencapsular(mensaje, puerto, src["PuertoTCP"], src["IP"],
                      dst["IP"], rou["MAC_PC1"], rou["MAC_PC2"])
    else:
        print("Has seleccionado comunicar de PC2 a PC1.")
        src, dst, rou = (DISPOSITIVOS["PC2"], DISPOSITIVOS["PC1"],
                         DISPOSITIVOS["Router"])
        encapsular(mensaje, puerto, src["PuertoTCP"], src["IP"], dst["IP"],
                   src["MAC"], src["MAC_ROUTER"])
        switches_y_router(mensaje, puerto, src["PuertoTCP"], src["IP"],
                          dst["IP"], rou["MAC_PC2"], rou["MAC_PC1"],
                          src["MAC"], src["MAC_ROUTER"])
        desencapsular(mensaje, puerto, src["PuertoTCP"], src["IP"], dst["IP"],
                      rou["MAC_PC2"], rou["MAC_PC1"])
