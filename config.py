# config interface RIP

conf = f"""
    interface {int}
     no ip address
     negotiation auto
     ipv6 address {adresse}
     ipv6 enable
     ipv6 rip 1 enable
    """

conf = f"""
    ipv6 router rip 1
     redistribute connected
    """
# config interface OSPF

conf = f"""
    interface {int}
     no ip address
     negotiation auto
     ipv6 address {adresse}
     ipv6 enable
     ipv6 ospf 1 area 0
    """

conf = f"""
    ipv6 router ospf 1
     router-id {id}
    """

# config int loopback idem avec int = Loopback0 et adresse loopback

    #int OSPF passif
conf = f"""
    ipv6 router ospf 1
     router-id {id}
     passive-interface {int}
    """

#bgp
conf = f"""
    router bgp {AS}
     bgp router-id {id}
     bgp log-neighbor-changes
     no bgp default ipv4-unicast
     neighbor {ad_n} remote-as {AS_n}
     """
    #iBGP
     """
     neighbor {ad_n} update-source Loopback0
     """

    #trouver un moyen de rajouter tous les neighbors
    f"""
     !
     address-family ipv4
     exit-address-family
     !
     address-family ipv6
      neighbor {ad_n} activate
     exit-address-family
    """




