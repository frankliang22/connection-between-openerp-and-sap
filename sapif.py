from openerp.osv import osv,fields
import os
import subprocess
from subprocess import Popen, PIPE
import sapnwrfc
import sys
import basic

class sapif(osv.Model):
    _name = "sapif.part1"
  
    def _for_test_hans(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        path = ""
        if 'build' in os.listdir(os.getcwd()):
          path = os.path.join(os.getcwd(), 'build')
        elif os.listdir(os.path.join(os.getcwd(), './')):
          path =  os.path.join(os.getcwd(),'/opt/openerp/openerp/addons/sap/sapnwrfc/build')
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
        sapnwrfc.base.config_location = '/opt/openerp/openerp/addons/sap/sapnwrfc/examples/sap.yml'
        sapnwrfc.base.load_config()
        for i in self.browse(cr,uid,ids,context=context): 
            conn = sapnwrfc.base.rfc_connect()
            fd = conn.discover("RFC_READ_TABLE")
            f = fd.create_function_call()
            f.QUERY_TABLE("MARA_MATNR")
            f.ROWCOUNT(10)
            f.OPTIONS( [{ 'TEXT': "MATNR LIKE \'"+str(i.newfield)+"%\'"}] )
           # f.OPTIONS( [{ 'TEXT': "MATNR LIKE 'A%'"}] )
            f.invoke()
            d = f.DATA.value 
            conn.close()
            string = str(d[0]).translate(None,"{}")
            #string = str(d[0]).replace("{","")
            #string = string.replace("}","")
            res[i.id] = string
        return res
        

   # def _for_test(self, cr, uid, ids, field_names, arg, context=None):
       # res = {}
       # for i in self.browse(cr,uid,ids,context=context): 
           # p = subprocess.Popen(['python','/opt/openerp/openerp/addons/sap/basic.py'],stdout=subprocess.PIPE,shell=False)
           # stdout = p.communicate()[0]
           # string = str(stdout)
           # string = string.replace("{","")
           # string = string.replace("}","")
           # res[i.id] = string
       # return res

   
    _columns = {
        'material' : fields.char(string="Material"),
        'industry_sector' : fields.selection([('Chemical industry','Chemical industry'),('Mechanical Engineering','Mechanical Engineering'),('Pharmaceuticals','Pharmaceuticals'),('Plant engin / Construction','Plant engin / Construction'),('Retail','Retail')],'Industry Sector'),
        'material_type' : fields.selection([('Additionals','Additionals'),('Apparel (seasonal)','Apparel (seasonal)'),('Beverages','Beverages'),('CH Contact Handling','CH Contact Handling'),('Competitive Product','Competitive Product'),('Configurable Material','Configurable Material'),('Coupons','Coupons'),('Empties','Empties'),('Empties (retail)','Empties (retail)'),('Equipment Package','Equipment Package'),('Finished Product','Finished Product'),('Foods','Foods'),('Full Products','Full Products'),('Indirect Material','Indirect Material'),('Intra Material','Intra Material'),('KANBAN container','KANBAN container'),('Maintenance Assembly','Maintenance Assembly'),('Manufacturer Parts','Manufacturer Parts'),('Material Planning Object','Material Planning Object'),('Non-stock material','Non-stock material'),('Non-valuated material','Non-valuated material'),('Nonfoods','Nonfoods'),('Operating supplies','Operating supplies'),('Packaging','Packaging'),('Perishables','Perishables'),('Pipeline materials','Pipeline materials'),('Process material','Process material'),('Prod. Resources/ tools','Prod. Resources/ tools'),('Product catalogs','Product catalogs'),('Product group','Product group'),('Raw material','Raw material'),('Returnable packaging','Returnable packaging'),('Semifinished product','Semifinished product'),('Service','Service'),('Spare Parts','Spare Parts'),('Trading goods','Trading goods'),('Trading goods (planned)','Trading goods (planned)'),('Value-only materials','Value-only materials'),('Waste','Waste')],'Material Type'),
        'change_number' : fields.char('Change Number'),
        'x_material' : fields.char('Material'),
        'test': fields.function(_for_test_hans, string="test", type="char"),
        'newfield':fields.char(string="test"),
        
    }
