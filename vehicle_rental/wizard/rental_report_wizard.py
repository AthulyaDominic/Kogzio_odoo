import json

from odoo import models,fields,api
from odoo.exceptions import ValidationError







class RentalReportWizard(models.TransientModel):
    _name='rental.report.wizard'
    _description = 'Rental Report Wizard'

    from_date=fields.Date(string='From Date')
    to_date=fields.Date(string='To Date')

    vehicle_id=fields.Many2one('rental.vehicle',string='Vehicle',required=True)

    #fetching data using query through a function

    def get_report_data(self, vehicle_id=False, from_date=False, to_date=False):

        query = """
                        SELECT rr.*,
                               rp.name AS customer_name,
                                rv.name AS vehicle_name
                               FROM rental_request rr
                                INNER JOIN res_partner rp ON
                                rr.customer_id = rp.id
                                 INNER JOIN rental_vehicle rv
                                 ON rr.vehicle_id = rv.id
                        WHERE 1=1
                    """

        if vehicle_id:
            query += f" AND rr.vehicle_id = {vehicle_id}"

        if from_date:
            query += f" AND rr.request_date >= '{from_date}'"

        if to_date:
            query += f" AND rr.request_date <= '{to_date}'"
        print(query)
        self.env.cr.execute(query)
        result= self.env.cr.dictfetchall()
        print(result)
        return result

    @api.constrains('from_date', 'to_date')
    def _check_dates(self):
        for rec in self:

            # From Date greater than To Date
            if rec.from_date and rec.to_date:
                if rec.from_date > rec.to_date:
                    raise ValidationError(
                        "From Date must be less than or equal to To Date."
                    )



    def action_generate_pdf(self):
        result = self.get_report_data(
            self.vehicle_id.id,
            self.from_date,
            self.to_date
        )
        data = {

            'result':result,
            'from_date': self.from_date,
            'to_date': self.to_date,


        }

        return self.env.ref(
            'vehicle_rental.action_rental_request_report'
        ).report_action([], data=data)


    def action_generate_excel(self):
        result = self.get_report_data(
            self.vehicle_id.id,
            self.from_date,
            self.to_date
        )

        data = {
            'result': result,
            'vehicle_id': self.vehicle_id.id,
            'from_date': self.from_date,
            'to_date': self.to_date,
        }
        return {
            'type': 'ir.actions.report',
            'data':{
                'model':'rental.request',
                'options':json.dumps(data,default=str),#here default=str we converting the dates to string format.
                'output_format':'xlsx',
                'report_name':'Rental Request Report'
            },
            'report_type':'xlsx'
        }


