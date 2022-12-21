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

# Create Application Profile
app = AppProfile('AP_CyberInsight-PY', tenant)

# Create Bridge Domain
bd = BridgeDomain('BD_Security', tenant)
bd1 = BridgeDomain('BD_Linux', tenant)

# Add Bridge Domain to VRF
bd.add_context(context)

# Create EPGs and add it to Bridge Domain
epg = EPG('epg_CyberInsight-PY', app)
epg1 = EPG('epg_CyberInsight1-P', app)
epg2 = EPG('epg_CyberInsight2-P', app)
epg.add_bd(bd)
epg1.add_bd(bd1)

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