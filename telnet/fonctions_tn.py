import time 

def Config_adresse(RX, adresse, int,tn) :
    """
    Configuration de l'adresse (str) du routeur RX (str) sur l'interface int (str)
    """
    tn.write(bytes("int "+int+"\r",encoding= 'ascii'))
    tn.read_until(bytes("#",encoding= 'ascii'))
    tn.write(bytes("ipv6 enable\r",encoding= 'ascii'))
    tn.write(bytes("ipv6 address " + adresse + "\r",encoding= 'ascii'))
    tn.write(bytes("no shutdown\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    
def Config_loopback(RX,loopback,tn) : 
    """
    Configuration de l'adresse loopback (str) du routeur RX (str)
    """
    tn.write(bytes("int l0\r",encoding= 'ascii'))
    tn.read_until(bytes("#",encoding= 'ascii'))
    tn.write(bytes("ipv6 enable\r",encoding= 'ascii'))
    tn.write(bytes("ipv6 address " + loopback + "\r",encoding= 'ascii'))
    tn.write(bytes("no shutdown\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))

def RIP(RX,tn) : 
    """
    Fait les configurations nécessaires pour lancer RIP sur le routeur RX
    """
    tn.write(bytes("ipv6 router rip ripng\r",encoding= 'ascii'))
    tn.write(bytes("redistribute connected\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    time.sleep(0.1)


def RIP_int(RX, int,tn) :
    """
    Configure RIP sur l'interface int du routeur RX
    """
    tn.write(bytes("int "+ int +"\r",encoding= 'ascii'))
    tn.read_until(bytes("#",encoding= 'ascii'))
    tn.write(bytes("ipv6 rip ripng enable\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    time.sleep(0.1)

    
def ID_OSPF(RX,id,tn) :
    """
    Config le routeur id pour OSPF
    """
    tn.write(bytes("ipv6 router ospf 1\r",encoding= 'ascii'))
    tn.write(bytes("router-id "+ id +"\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    time.sleep(0.1)
    
def OSPF(RX,int,tn) :
    """
    Configure OSPF sur l'interface int du routeur RX
    """
    tn.write(bytes("int "+ int +"\r",encoding= 'ascii'))
    tn.read_until(bytes("#",encoding= 'ascii'))
    tn.write(bytes("ipv6 ospf 1 area 0\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    time.sleep(0.5)

def OSPF_cost(RX,int,cost,tn) :
    """
    Configure OSPF sur l'interface int du routeur RX
    """
    tn.write(bytes("int "+ int +"\r",encoding= 'ascii'))
    tn.read_until(bytes("#",encoding= 'ascii'))
    tn.write(bytes("ipv6 ospf cost "+ cost +"\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    

def OSPF_passif(RX,int,tn) :
    """
    Met l'interface int du routeur RX configurée avec OSPF en passif
    """
    tn.write(bytes("ipv6 router ospf 1\r",encoding= 'ascii'))
    tn.write(bytes("passive-interface "+ int +"\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    

def ID_BGP(RX, id, AS,tn) :
    """
    Config le routeur id pour BGP
    """
    tn.write(bytes("router bgp "+ AS +"\r",encoding= 'ascii'))
    tn.write(bytes("no bgp default ipv4-unicast\r",encoding= 'ascii'))
    tn.write(bytes("bgp router-id "+ id +"\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    time.sleep(0.1)

def iBGP(RX, ad_n, AS,tn) :
    """
    Configure iBGP sur l'interface loopback du routeur RX
    """
    tn.write(bytes("router bgp "+ AS +"\r",encoding= 'ascii'))
    tn.read_until(bytes("#",encoding= 'ascii'))
    tn.write(bytes("neighbor "+ ad_n +" remote-as "+ AS +"\r",encoding= 'ascii'))
    tn.write(bytes("neighbor "+ ad_n +" update-source l0\r",encoding= 'ascii'))
    tn.write(bytes("address-family ipv6 unicast\r",encoding= 'ascii'))
    tn.write(bytes("neighbor "+ ad_n +" activate\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))    
    time.sleep(0.1)

def eBGP(RX, ad_n, AS_n, AS,tn) :
    """
    Configure eBGP sur l'interface loopback du routeur RX
    """
    tn.write(bytes("router bgp "+ AS +"\r",encoding= 'ascii'))
    tn.write(bytes("neighbor "+ ad_n +" remote-as "+ AS_n +"\r",encoding= 'ascii'))
    tn.write(bytes("address-family ipv6 unicast\r",encoding= 'ascii'))
    tn.write(bytes("neighbor "+ ad_n +" activate\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii')) 
    time.sleep(0.1)

def eBGP_adv(RX, AS, prefix,tn) :
    """
    Configure advertissement pour le routeur RX en eBGP
    """ 
    tn.write(bytes("router bgp "+ AS +"\r",encoding= 'ascii'))
    tn.write(bytes("address-family ipv6 unicast\r",encoding= 'ascii'))
    tn.write(bytes("network "+ prefix +"\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii'))
    tn.write(bytes("exit\r",encoding= 'ascii')) 
    time.sleep(0.1)