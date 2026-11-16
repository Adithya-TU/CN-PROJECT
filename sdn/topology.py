from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def run():
    net = Mininet(controller=None, switch=OVSSwitch, autoSetMacs=True)

    info("*** Adding remote SDN controller\n")
    net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6653
    )

    info("*** Adding switch\n")
    s1 = net.addSwitch('s1', protocols='OpenFlow13')

    info("*** Adding hosts\n")
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')

    info("*** Connecting hosts to switch\n")
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    info("*** Starting network\n")
    net.start()

    info("*** Network ready\n")
    info("*** h1 = 10.0.0.1\n")
    info("*** h2 = 10.0.0.2\n")
    info("*** h3 = 10.0.0.3\n")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
