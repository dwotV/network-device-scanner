from scapy.all import conf, get_if_addr

def network():
    interface = conf.iface
    ip = get_if_addr(interface)
    ip = ip.rsplit(".", 1)[0] + '.0' + '/24'

    return [interface, ip]
