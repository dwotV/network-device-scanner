from scapy.all import conf

gateway_ip = conf.route.route('0.0.0.0')[2]
