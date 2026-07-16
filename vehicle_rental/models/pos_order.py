from odoo import models,fields
print("========== POS ORDER LOADED ==========")

class PosOrder(models.Model):
    _inherit='pos.order'
    rental_id=fields.Many2one("rental.request",string="Rental Request")