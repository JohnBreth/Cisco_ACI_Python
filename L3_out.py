#!/usr/bin/env python

from acitoolkit.acitoolkit import *
"""
Create a tenant with a single EPG and assign it statically to 2 interfaces.
This is the minimal configuration necessary to enable packet forwarding
within the ACI fabric.
"""
# Create the Tenant
tenant = Tenant('CyberInsight-PY')

# Create VRF
context = Context('VRF_CyberInsight-PY', tenant)

# Create L3 Out with OSPF (connection to external network outside of APIC domain)
outside_l3 = OutsideL3('out-1', tenant)
    outside_l3.add_context(context)
    phyif = Interface('eth', '1', '101', '1', '46')
    phyif.speed = '1G'
    l2if = L2Interface('eth 1/101/1/46', 'vlan', '1')
    l2if.attach(phyif)
    l3if = L3Interface('l3if')
    l3if.set_l3if_type('l3-port')
    l3if.set_mtu('1500')
    l3if.set_addr('1.1.1.2/30')
    l3if.add_context(context)
    l3if.attach(l2if)
    rtr = OSPFRouter('rtr-1')
    rtr.set_router_id('10.10.10.10')
    rtr.set_node_id('101')
    ifpol = OSPFInterfacePolicy('myospf-pol', tenant)
    ifpol.set_nw_type('p2p')
    ospfif = OSPFInterface('ospfif-1', router=rtr, area_id='1')
    ospfif.set_area_type('nssa')
    ospfif.auth_key = 'password'
    ospfif.int_policy_name = ifpol.name
    ospfif.auth_keyid = '1'
    ospfif.auth_type = 'simple'
    tenant.attach(ospfif)
    ospfif.networks.append('0.0.0.0/0')
    ospfif.attach(l3if)
    contract1 = Contract('contract-1')
    outside_epg = OutsideEPG('outepg', outside_l3)
    outside_epg.provide(contract1)
    contract2 = Contract('contract-2')
    outside_epg.consume(contract2)
    outside_l3.attach(ospfif)


# Create Application Profile
app = AppProfile('AP_CyberInsight-PY', tenant)

# Create Bridge Domain
bd = BridgeDomain('BD_Security', tenant)
bd1 = BridgeDomain('BD_Linux', tenant)

# Add Bridge Domain to VRF
bd.add_context(context)

# Create subnet and attach it to BD
subnet = Subnet('Security', bd)
subnet.set_addr('192.168.1.1/24')
bd.add_subnet(subnet)

# Create EPGs and add it to Bridge Domain
epg = EPG('epg_CyberInsight-PY', app)
epg1 = EPG('epg_CyberInsight1-P', app)
epg2 = EPG('epg_CyberInsight2-P', app)
epg.add_bd(bd)
epg1.add_bd(bd1)
# Set EPG isolation
epg.set_intra_epg_isolation(False)
epg1.set_intra_epg_isolation(True)

# Define a contract and attach 2 entries to it
contract = Contract('Syslog', tenant)
TCPSyslog = FilterEntry('TCPSyslog',
                         applyToFrag='no',
                         arpOpc='unspecified',
                         dFromPort='512',
                         dToPort='512',
                         etherT='ip',
                         prot='tcp',
                         sFromPort='1',
                         sToPort='65535',
                         tcpRules='unspecified',
                         parent=contract)
UDPSyslog = FilterEntry('UDPSyslog',
                         applyToFrag='no',
                         arpOpc='unspecified',
                         dFromPort='512',
                         dToPort='512',
                         etherT='ip',
                         prot='UDP',
                         sFromPort='1',
                         sToPort='65535',
                         tcpRules='unspecified',
                         parent=contract)

# Declare 2 physical interfaces
if1 = Interface('eth', '1', '101', '1', '20')
if2 = Interface('eth', '1', '101', '1', '21')

# Provide the contract from 1 EPG and consume from the other(Linux server(provider) sending syslog traffic to security servers(consumer))
epg.consume(contract)
epg1.provide(contract)

# Create port channel
pc1 = PortChannel('pc1')
pc1.attach(if1)
pc1.attach(if2)

# Create VLAN 100 on the port channel
vlan100_on_pc1 = L2Interface('vlan100_on_pc1', 'vlan', '100')
vlan100_on_pc1.attach(pc1)

# Attach the EPG to the VLANs
epg.attach(vlan100_on_pc1)


# Get the APIC login credentials
description = 'acitoolkit tutorial application'
creds = Credentials('apic', description)
creds.add_argument('--delete', action='store_true',
                   help='Delete the configuration from the APIC')
args = creds.get()

# Delete the configuration if desired
if args.delete:
    tenant.mark_as_deleted()

# Login to APIC and push the config
session = Session(args.url, args.login, args.password)
session.login()
resp = tenant.push_to_apic(session)
if resp.ok:
    print('Success')

# Print what was sent
print('Pushed the following JSON to the APIC')
print('URL:', tenant.get_url())
print('JSON:', tenant.get_json())