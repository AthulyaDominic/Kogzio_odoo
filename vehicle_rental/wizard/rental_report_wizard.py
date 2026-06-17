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

        # Title
        worksheet.write('A1', 'Rental Request Report')

        # Headers
        worksheet.write('A3', 'Rental ID')
        worksheet.write('B3', 'Customer')
        worksheet.write('C3', 'Request Date')
        worksheet.write('D3', 'Rent Date')
        worksheet.write('E3', 'Return Date')
        worksheet.write('F3', 'Period')
        worksheet.write('G3', 'Status')

        # Fetch records
        vehicle_id=self.vehicle_id.id
        from_date=self.from_date
        to_date=self.to_date

        query="""SELECT *,
        (SELECT name FROM res_partner WHERE id=rental_request.customer_id)
        AS customer_name
        FROM rental_request WHERE 1=1 """

        if vehicle_id:
            query+= f" AND vehicle_id={vehicle_id}"
        if from_date:
            query+= f" AND request_date>='{from_date}'"
        if to_date:
            query+= f" AND request_date<='{to_date}'"

        self.env.cr.execute(query)
        rows=self.env.cr.dictfetchall()

        # Data starts after header row
        row = 3

        for rec in rows:
            worksheet.write(row, 0, rec['rental_id'])
            worksheet.write(row, 1, rec['customer_name'])
            worksheet.write(row, 2, str(rec['request_date']))
            worksheet.write(row, 3, str(rec['rent_date']))
            worksheet.write(row, 4, str(rec['return_date']))
            worksheet.write(row, 5, rec['period'])
            worksheet.write(row, 6, rec['status'])

            row += 1

        # Close workbook LAST
        workbook.close()

        output.seek(0)

        print("Excel Button Clicked")
        print("Excel Headers Created")
        print("Excel Data Written")


        #read the file and convert it to encoded format
        import base64

        excel_data=output.read()
        excel_file=base64.b64encode(excel_data)

        print(type(excel_file))
        print(excel_file[:50])

        #create an attachment in odoo
        attachment=self.env['ir.attachment'].create({
            'name':'Rental_Report.xlsx',
            'type':'binary',
            'datas':excel_file,
            'mimetype':'application/vnd.openxmlformat-officedocument.spreadsheetml.sheet'
        })

        #Return download action
        return{
            'type':'ir.actions.act_url',
            'url':f'/web/content/{attachment.id}?download=true',
            'target':'self'
        }