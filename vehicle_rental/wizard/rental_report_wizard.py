from odoo import models,fields,api
from odoo.exceptions import ValidationError




class RentalReportWizard(models.TransientModel):
    _name='rental.report.wizard'
    _description = 'Rental Report Wizard'

    from_date=fields.Date()
    to_date=fields.Date()

    vehicle_id=fields.Many2one('rental.vehicle',string='vehicle',required=True)

    @api.constrains('from_date', 'to_date')
    def _check_dates(self):
        for rec in self:

            # One date entered, other missing
            if (rec.from_date and not rec.to_date) or \
                    (rec.to_date and not rec.from_date):
                raise ValidationError(
                    "Please enter both From Date and To Date."
                )

            # From Date greater than To Date
            if rec.from_date and rec.to_date:
                if rec.from_date > rec.to_date:
                    raise ValidationError(
                        "From Date must be less than or equal to To Date."
                    )



    def action_generate_pdf(self):
        data = {
            'vehicle_ids': self.vehicle_id.id,

            'from_date': self.from_date,
            'to_date': self.to_date,


        }

        return self.env.ref(
            'vehicle_rental.action_rental_request_report'
        ).report_action([], data=data)