from odoo import models, fields

class VehicleFeatures(models.Model):
    _name='vehicle.feature'
    _description = 'Vehicle Features'
    _rec_name = 'name'

    name=fields.Char(string="Feature Name",help="Enter the name of the vehicle feature.",required=True)
    description = fields.Text(string="Description",help="Provide a short description about the feature.",required=True)