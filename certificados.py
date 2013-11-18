# -*- coding: utf-8 -*-
import time
from datetime import datetime
from osv import osv, fields
from openerp.osv import osv, fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class certificados(osv.osv):

    _name = 'certificados.certificados'
    _description = "Certificados de No Produccion"
    _inherit=['mail.thread', 'ir.needaction_mixin']
	
    def _get_total_quantity(self, cr, uid, ids, field, args, context = None):
        res = {}
        cc = None
        for cc in self.browse(cr, uid, ids, context = context):
            res[cc.id] = sum([x.itom for x in cc.cert_ids])
        return res
			
    _columns = {
        # 'item' : fields.integer('Items'), Numero'),
        'item': fields.function(_get_total_quantity, type='integer', method = True, string = 'Items', readonly = True),
        'Registro_Numero' : fields.char('Registro Numero'),
        'Fecha_de_Emision': fields.date('Fecha de Emision', required=True, select=True),
        'Fecha_de_Solicitud': fields.date('Fecha de Solicitud', required=True, select=True),
        'venci_': fields.date('Vencimiento del Documento', required=True, select=True),
        'vige_' : fields.char('Vigencia'), 
        'user_id': fields.many2one('res.users', 'Responsible'),
        'cert_ids' : fields.one2many('certificados.line', 'requisicion_id', 'Items del Certificado'),
        'descripcion' : fields.text('Descripcion'),
        'company_id': fields.many2one('res.company', 'Compañia', required=True, select=1, help="Compañia relacionada con éste certificado"),
        'notas' : fields.text('Notas'),
    }
	
    _defaults = {
    'user_id': lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).id ,
    }
	

class certificados_line(osv.osv):
    
    _name = 'certificados.line'
    _description = "Items del Certificado"
    	
    def multi_a_b(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids,context):
            res[record.id] = record.Cantidad * record.Precio_Unitario_Declarado
        return res
		
    def multi_c_d(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids,context):
            res[record.id] = record.Cantidad - record.canti_cert
        return res
	
    _columns = {
        'itom' : fields.boolean('N', required=True),
        'codigo_n' : fields.related('product_id', 'codigo_n', type='char', size=64, string='Codigo Arancelario', store=True, readonly=True),
        'product_id' : fields.many2one('product.product', 'Material'),
        'canti_cert' : fields.related('product_id', 'canti_cert', type='float', string='Cantidad Consumida'),
        'order_line' : fields.many2one('purchase.order', 'Linea de pedido'),
        'arandesc' : fields.related('product_id', 'arandesc', type='char', size=128, string='Descripcion Arancelaria', store=True, readonly=True), 
        'tec_esp': fields.related('product_id', 'tec_esp', type='char', size=64, string='Especificaciones tecnicas', store=True, readonly=True),
        'Cantidad' : fields.float('Cantidad'), 'Unidad_de_Medida': fields.many2one('product.uom', 'Unidad de Medida'),
        'Precio_Unitario_Declarado' : fields.float('Precio Unitario Declarado'), 'Moneda' : fields.many2one('res.currency', 'Moneda'),
        'Valor_En_Divisas' : fields.function(multi_a_b, type='integer', string='Valor En Divisas'),
        'Cantidad_Disponible' : fields.function(multi_c_d, type='float', string='Cantidad Disponible'),
        'requisicion_id' : fields.many2one('certificados.certificados', 'Certificados de No Produccion', ondelete='cascade'),
    }	
certificados_line()