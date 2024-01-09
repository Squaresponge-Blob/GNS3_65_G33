def Config_adresse(RX, adresse, int) :
    """
    Configuration de l'adresse (str) du routeur RX (str) sur l'interface int (str)
    """
    tn.write(bytes("int "+int+"\r",encoding= 'ascii'))
    tn.write(bytes("ipv6 enable\r",encoding= 'ascii'))
    tn.write(bytes("ipv6 address " + adresse + "\r",encoding= 'ascii'))
    tn.write(bytes("no shutdown\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))

def Config_loopback(RX,loopback) : 
    """
    Configuration de l'adresse loopback (str) du routeur RX (str)
    """
    tn.write(bytes("int l0\r",encoding= 'ascii'))
    tn.write(bytes("ipv6 enable\r",encoding= 'ascii'))
    tn.write(bytes("ipv6 address " + adresse + "\r",encoding= 'ascii'))
    tn.write(bytes("no shutdown\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))

def RIP(RX) : 
    """
    Fait les configurations nécessaires pour lancer RIP sur le routeur RX
    """
    tn.write(bytes("ipv6 router rip ripng\r",encoding= 'ascii'))
    tn.write(bytes("redistribute connected\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))

def RIP_int(RX, int) :
    """
    Configure RIP sur l'interface int du routeur RX
    """
    tn.write(bytes("int "+int+"\r",encoding= 'ascii'))
    tn.write(bytes("ipv6 rip ripng enable\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))

def ID_BGP(RX, id) :
    """
    Config le routeur id pour BGP
    """


def ID_OSPF(RX,id) :
     """
    Config le routeur id pour OSPF
    """