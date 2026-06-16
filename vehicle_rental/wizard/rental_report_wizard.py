from odoo import models,fields,api
from odoo.exceptions import ValidationError
import io
import xlsxwriter




class RentalReportWizard(models.TransientModel):
    _name='rental.report.wizard'
    _description = 'Rental Report Wizard'

    from_date=fields.Date()
    to_date=fields.Date()

    vehicle_id=fields.Many2one('rental.vehicle',string='vehicle',required=True)

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
        data = {
            'vehicle_ids': self.vehicle_id.id,

            'from_date': self.from_date,
            'to_date': self.to_date,


        }

        return self.env.ref(
            'vehicle_rental.action_rental_request_report'
        ).report_action([], data=data)

    def action_generate_excel(self):

            output = io.BytesIO()

            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet('Rental Report')

            worksheet.write('A1', 'Rental Request Report')

            worksheet.write('A3', 'Rental ID')
            worksheet.write('B3', 'Customer')
            worksheet.write('C3', 'Request Date')
            worksheet.write('D3', 'Rent Date')
            worksheet.write('E3', 'Return Date')
            worksheet.write('F3', 'Period')
            worksheet.write('G3', 'Status')

            workbook.close()

            output.seek(0)


            print("Excel Button Clicked")
            print("Excel Headers Created")