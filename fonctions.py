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
    tn.write(bytes("int "+ int +"\r",encoding= 'ascii'))
    tn.write(bytes("ipv6 rip ripng enable\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    
def ID_OSPF(RX,id) :
     """
    Config le routeur id pour OSPF
    """
    tn.write(bytes("ipv6 router ospf 1\r",encoding= 'ascii'))
    tn.write(bytes("router-id"+ id +"\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    
def OSPF(RX,int) :
    """
    Configure OSPF sur l'interface int du routeur RX
    """
    tn.write(bytes("int "+ int +"\r",encoding= 'ascii'))
    tn.write(bytes("ipv6 ospf 1 area 0\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))

def OSPF_passif(RX,int) :
    """
    Met l'interface int du routeur RX configurée avec OSPF en passif
    """
    tn.write(bytes("ipv6 router ospf 1\r",encoding= 'ascii'))
    tn.write(bytes("passive-interface"+ int +"\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))

def ID_BGP(RX, id, AS) :
    """
    Config le routeur id pour BGP
    """
    tn.write(bytes("router bgp"+ AS +"\r",encoding= 'ascii'))
    tn.write(bytes("no bgp default ipv4-unicast\r",encoding= 'ascii'))
    tn.write(bytes("bgp router-id"+ id +"\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))

def iBGP(RX, loopback, ad_n) :
    """
    Configure iBGP sur l'interface loopback du routeur RX
    """
    

def eBGP(RX, int, ad_n, AS_n) :
