
#!/usr/bin/env /usr/bin/python
import sys
from openerp.osv import osv,fields

if sys.version < '2.2':
  print "\n\n   You Must Have Python Version >= 2.2  To run saprfc \n\n"
  sys.exit(1)
import os
path = ""
if 'build' in os.listdir(os.getcwd()):
  path = os.path.join(os.getcwd(), 'build')
elif os.listdir(os.path.join(os.getcwd(), './')):
  path = os.path.join(os.getcwd(), '/opt/openerp/openerp/addons/sap/sapnwrfc/build')
else:
  print "cant find ./build directory to load the saprfc module, try runnig from the package root dir"
  print "   looked in:", os.getcwd(), " and ", os.path.join(os.getcwd(), '../')
  sys.exit(1)
libdir = ""
for i in  os.listdir(path):
  if i.startswith("lib"):
    libdir = os.path.join(path, i)
if libdir == "":
  print "cant find ./build directory to load the saprfc module, try runnig from the package root dir"
  print "   looked in:", os.getcwd(), " and ", os.path.join(os.getcwd(), '../')
  sys.exit(1)
sys.path.append(libdir)


import sapnwrfc


sapnwrfc.base.config_location = '/opt/openerp/openerp/addons/sap/sapnwrfc/examples/sap.yml'
sapnwrfc.base.load_config()



#conn = sapnwrfc.base.rfc_connect({'user': 'developer', 'passwd': 'developer'})
conn = sapnwrfc.base.rfc_connect()

fd = conn.discover("RFC_READ_TABLE")



f = fd.create_function_call()
f.QUERY_TABLE("MARA_MATNR")
f.ROWCOUNT(10)
#f.OPTIONS( [{ 'TEXT': "MATNR LIKE \'"+str(i.newfield)+"%\'"}] )
f.OPTIONS( [{ 'TEXT': "MATNR LIKE 'A%'"}] )

f.invoke()
d = f.DATA.value
print  d[0]
conn.close()
 
