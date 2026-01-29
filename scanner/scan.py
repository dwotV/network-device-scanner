from .vendor import get_vendor
from scapy.all import ARP, Ether, srp

def scan(ip):
    ip_range = ARP(pdst=ip)
    broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')
    final_packet = broadcast / ip_range

    answered = srp(final_packet, timeout=2, retry=1, verbose=False)[0]

    devices = []

    for received in answered:
        mac = received[1].hwsrc
        vendor = get_vendor(mac)
        devices.append({
            'ip': received[1].psrc,
            'mac': mac,
            'vendor': vendor,
        })

    return devices
