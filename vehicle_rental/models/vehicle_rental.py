from odoo import models,fields,api

class VehicleRental(models.Model):
    _name = 'rental.vehicle'
    _description = 'vehicle rental'


    vehicle_id=fields.Char(string="Vehicle ID",readonly=True,copy=False,
                           default="New",help="Unique sequence number generated automatically for each vehicle.")
    name=fields.Char(string="Vehicle Name",help="Enter the name of the vehicle.",required=True)
    brand=fields.Char(string="Brand",help="Specify the vehicle brand.",required=True)
    registration_date=fields.Date(string="Registration Date",help="Date on which the vehicle was registered.",required=True)
    model_year=fields.Char(
        string="Model Year",
        help="Registered manufacturing year of the vehicle.",
        compute="_compute_model_year",

        readonly=True
    )
    price=fields.Float(string="Daily Rental Rate", help="Daily rental amount for the vehicle.",required=True)
    # rental_history=fields.One2many('rental.request','vehicle_id',string="Rental History")
    status=fields.Selection([
        ('available','For Available'),

        ('rented','Rented'),

        ('sold', 'Sold')
    ],string="Status",default='available',help="Current availability status of the vehicle.")
    feature_ids = fields.Many2many(
        'vehicle.feature',
        string="Features",
        help="Choose the additional features available in the vehicle such as AC, Bluetooth, GPS, etc."
    )

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:

            if vals.get('vehicle_id', 'New') == 'New':
                vals['vehicle_id'] = self.env['ir.sequence'].next_by_code(
                    'rental.vehicle'
                ) or 'New'

        return super().create(vals_list)

    @api.depends('registration_date')
    def _compute_model_year(self):
        print(self)
        for record in self:

            if record.registration_date:
                record.model_year=str(record.registration_date.year)
            else:
                record.model_year=False

    #name format changes
    def name_get(self):
        result=[]
        for record in self:
            brand=record.brand or ''
            name=record.name or ''
            year=record.model_year or ''
            vehicle_name=f"{brand} {name}/{year}"
            result.append((record.id,vehicle_name))
        return result

    def action_rental_history(self):

        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Rental History',
            'res_model': 'rental.request',
            'view_mode': 'list,form',
            'domain': [('vehicle_id', '=', self.id)],
    'context': {
        'create': False,
        'edit': False,
        'delete': False,
    }
        }