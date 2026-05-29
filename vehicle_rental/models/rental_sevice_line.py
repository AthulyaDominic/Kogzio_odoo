from odoo import models, fields

class RentalServiceLine(models.Model):
    _name="rental.service.line"
    _description="vehicle rental service lines"
    service_name=fields.Char(string="Service Name",help="Enter the name of the additional rental service.",required=True)
    price=fields.Float(string="Service Charge",help="Specify the amount charged for the selected extra service.",required=True)
    request_id=fields.Many2one('rental.request',string="Rental Request",help="Rental request to which this extra service belongs.",required=True)