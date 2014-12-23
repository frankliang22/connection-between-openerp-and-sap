import sapnwrfc

sapnwrfc.base.config_location = 'sap.yml'
sapnwrfc.base.load_config()

print "making a new connection:"
try:
    conn = sapnwrfc.base.rfc_connect()
    print "Connection attributes: ", conn.connection_attributes()
    conn.close()
except sapnwrfc.RFCCommunicationError:
    print "not able to connect!"

