import time
from datetime import datetime
from osv import osv, fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class certificados(osv.osv):

    _name = 'certificados.certificados'
    _description = "Certificados de No Produccion"
    _inherit=['mail.thread', 'ir.needaction_mixin']
	
    
	
    _columns = {
        
        'Registro_Numero' : fields.char('Registro Numero'),
        'Fecha_de_Emision': fields.date('Fecha de Emision', required=True, select=True),
        'Fecha_de_Solicitud': fields.date('Fecha de Solicitud', required=True, select=True),
        'venci_': fields.date('Vencimiento del Documento', required=True, select=True),
        'vige_' : fields.char('Vigencia'), 'cert_ids' : fields.one2many('certificados.line', 'requisicion_id', 'Items del Certificado'),
        'descripcion' : fields.text('Descripcion'),
        'notas' : fields.text('Notas'),
    }


class certificados_line(osv.osv):
    
    _name = 'certificados.line'
    _description = "Items del Certificado"
    _inherit = "purchase.order.line"
	
    def _get_total_quantity(self, cr, uid, ids, field, args, context = None):
        res = {}
        for po in self.browse(cr, uid, ids, context = context):
            res[po.id] = sum([x.quantity for x in po.requisicion_id])
        return res
        	
    def multi_a_b(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids,context):
            res[record.id] = record.Cantidad * record.Precio_Unitario_Declarado
        return res
		
    def cert_rest(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for cert_v in product_id == True(cr, uid, ids, context):
            self.cr.execute("""SELECT 'purchase_qty' FROM 'purchase_order_line'
            UNION 
			SELECT 'Cantidad_Disponible' FROM 'certificados_line';""")
        return res
	
    _columns = {
        'item': fields.function(_get_total_quantity, type='integer', method = True, string = 'Items', readonly = True),
        'codigo_n' : fields.related('product_id', 'codigo_n', type='char', size=64, string='Codigo Arancelario', store=True, readonly=True),
        'product_id' : fields.many2one('product.product', 'Material'),
        'arandesc' : fields.related('product_id', 'arandesc', type='char', size=128, string='Descripcion Arancelaria', store=True, readonly=True), 
        'tec_esp': fields.related('product_id', 'tec_esp', type='char', size=64, string='Especificaciones tecnicas', store=True, readonly=True),
        'Cantidad' : fields.float('Cantidad'), 'Unidad_de_Medida' : fields.many2one('product.uom', 'Unidad de Medida'),
        'Precio_Unitario_Declarado' : fields.float('Precio Unitario Declarado'), 'Moneda' : fields.many2one('res.currency', 'Moneda'),
        'Valor_En_Divisas' : fields.function(multi_a_b, type='integer', string='Valor En Divisas'),
        'requisicion_id' : fields.many2one('certificados.certificados', 'Certificados de No Produccion', ondelete='cascade'),
        'Cantidad_Consumida' : fields.related('product_id', 'outgoing_qty', type='float', string='Cantidad Consumida', store=True, readonly=True), 'Cantidad_Disponible' : fields.function(cert_rest, type='float', string='Cantidad Disponible'), # 'Cantidad_Disponible' : fields.related('product_id', 'qty_available', type='float', string='Cantidad Disponible', store=True, readonly=True),
    }	
certificados_line()