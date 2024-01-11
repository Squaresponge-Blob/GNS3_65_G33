def configuration():
    conf = f"""!
!
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname {node.name}
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
ipv6 unicast-routing
ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
!
interface {interface}
 no ip address
 negotiation auto
 ipv6 address {str(sub[k] + 1)}/64
 ipv6 enable
 ipv6 rip 1 enable
!                         
no cdp log mismatch duplex
!
line con 0
 exec-timeout 0 0
 logging synchronous
 privilege level 15
 no login
line aux 0
 exec-timeout 0 0
 logging synchronous
 privilege level 15
 no login
!
!
end
"""