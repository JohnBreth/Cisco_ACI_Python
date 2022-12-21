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

# Create Application Profie
app = AppProfile('AP_CyberInsight-PY', tenant)

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