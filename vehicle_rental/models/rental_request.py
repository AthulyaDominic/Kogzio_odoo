
from odoo import models, fields , api
from odoo.exceptions import ValidationError



class RentalRequest(models.Model):
    _name= 'rental.request'
    _description= 'vehicle rental request'
    _rec_name = 'rental_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    rental_id=fields.Char(string="Rental ID",default="New",readonly=True,copy=False,
                          help="Unique sequence number generated automatically for each rental request.",tracking=True)
    #who is renting the vehicle
    customer_id=fields.Many2one('res.partner',string="Customer ID",help="Select the customer who is renting the vehicle.",required=True,tracking=True)
    customer_name=fields.Char(string="Customer Name",tracking=True)
    customer_email=fields.Char(string="Email" ,tracking=True)
    customer_phone=fields.Char(string="Phone",tracking=True)
    #who created the request
    user_id=fields.Many2one(
    'res.users',
    string='Created By',
    default=lambda self: self.env.user,
    readonly=True
    )
    request_date=fields.Date(string="Request Date",readonly=True,default=fields.Date.today,
                             help="Date on which the rental request is created.",tracking=True)
    vehicle_id=fields.Many2one('rental.vehicle',string='Vehicle',help="Select the vehicle requested for rental.",
                               domain="[('status','=',   'available')]",required=True,tracking=True)
    rent_date = fields.Date(string="Rent Date",help="Date on which the vehicle will be rented to the customer.",required=True,tracking=True)

    return_date = fields.Date( string="Return Date", help="Expected date for returning the rented vehicle.",required=True,tracking=True)

    period = fields.Integer(
        string="Rental Period",
        compute="_compute_period",
        store=True,
        readonly=True,
        help="Automatically calculates total rental duration in days.",tracking=True
    )
    warning = fields.Boolean(string="Warning", compute="_compute_warning",tracking=True)
    late = fields.Boolean(string="Late", compute="_compute_late",tracking=True)
    service_ids=fields.One2many('rental.service.line','request_id',string="Services",
    help="List of additional services added to this rental request.",tracking=True)
    status=fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('invoiced','Invoiced'),
        ('returned', 'Returned')
    ],string="Status",default="draft",help = "Current status of the rental request.")
    invoice_id=fields.Many2one(comodel_name='account.move',string="Invoices",copy=False,tracking=True)

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:

            if vals.get('rental_id', 'New') == 'New':
                vals['rental_id'] = self.env['ir.sequence'].next_by_code(
                    'rental.request'
                ) or 'New'

        return super().create(vals_list)

    @api.depends('rent_date', 'return_date')
    def _compute_period(self):

        for record in self:

            if record.rent_date and record.return_date:

                days = (record.return_date - record.rent_date).days

                record.period = days

            else:

                record.period = 0
#checks rent date and return date validation
    @api.constrains('rent_date', 'return_date')
    def _check_return_date(self):

        for record in self:

            if record.rent_date and record.return_date:

                if record.return_date <= record.rent_date:
                    raise ValidationError(
                        "Return date must be greater than rent date."
                    )
     #create button method to rental status become draft->confirm the vehicle status becomes available->rented automatically

    def action_confirm(self):

        for record in self:
            record.status = 'confirm'

            record.vehicle_id.status = 'rented'

    # create button method to rental status become confirm->returned the vehicle status becomes rented->available automatically
    def action_return(self):

        for record in self:
            record.status = 'returned'

            record.vehicle_id.status = 'available'


    @api.depends('return_date','status')
    def _compute_warning(self):
        today = fields.Date.today()

        for record in self:
            if record.return_date:
               remaining_days = record.return_date - today
               if 0<=remaining_days.days<=2 and record.status!='returned':
                 record.warning=True
               else:
                 record.warning=False
            else:
                record.warning = False

    @api.depends('return_date','status')
    def _compute_late(self):
        today=fields.Date.today()
        for record in self:
            if record.return_date:
                remaining_days=record.return_date-today
                if remaining_days.days<0 and record.status!='returned':
                    record.late=True
                else:
                    record.late=False
            else:
                record.late=False

    def action_create_invoice(self):

        for record in self:

            if record.invoice_id:
                raise ValidationError("Invoice already created.")

            amount_paid = record.vehicle_id.price * record.period

            total_service_charge = 0

            if record.service_ids:

                for service in record.service_ids:
                    total_service_charge += service.price

            total_amount = amount_paid + total_service_charge
            service_product = self.env.ref('vehicle_rental.product_service_charge', raise_if_not_found=False)
            if not service_product:
                raise ValidationError("Default Service Charge product not found. Please update module.")

            invoice_vals = {

                'partner_id': record.customer_id.id,

                'move_type': 'out_invoice',

                'invoice_date': fields.Date.today(),
                'invoice_date_due': fields.Date.today(),

                'invoice_line_ids': [(0, 0, {
                     'name': f"Vehicle Rental - {record.vehicle_id.name}",
                      'quantity': 1,
                       'price_unit': total_amount,
                         'product_id': service_product.id,
                })]

            }

            invoice = self.env['account.move'].create(invoice_vals)

            record.invoice_id = invoice.id

            record.status = 'invoiced'
            return {
                'type': 'ir.actions.act_window',
                'name': 'Invoice',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoice.id,
            }

    def action_view_invoice(self):
        return{
            'type':'ir.actions.act_window',
            'name':'Invoice',
            'res_model':'account.move',
            'view_mode':'form',
            'res_id':self.invoice_id.id
        }

    # Fetching data using sql query function



