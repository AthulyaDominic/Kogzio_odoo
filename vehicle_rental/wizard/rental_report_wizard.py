from odoo import models,fields,api
from odoo.exceptions import ValidationError
import io
import base64
import xlsxwriter
from datetime import datetime




class RentalReportWizard(models.TransientModel):
    _name='rental.report.wizard'
    _description = 'Rental Report Wizard'

    from_date=fields.Date(string='From Date')
    to_date=fields.Date(string='To Date')

    vehicle_id=fields.Many2one('rental.vehicle',string='Vehicle',required=True)

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
        title_format = workbook.add_format({
            'bold': True,
            'align': 'center'
        })
        worksheet.merge_range(
            'A1:G1',
            'Rental Request Report',
            title_format
        )
        #Border
        header_format = workbook.add_format({
            'bold': True,
            'border': 1
        })

        data_format = workbook.add_format({
            'border': 1
        })

        # Headers
        worksheet.write('A3', 'Rental ID',header_format)
        worksheet.write('B3', 'Customer',header_format)
        worksheet.write('C3', 'Vehicle',header_format)
        worksheet.write('D3', 'Rent Date',header_format)
        worksheet.write('E3', 'Return Date',header_format)
        worksheet.write('F3', 'Period',header_format)
        worksheet.write('G3', 'Status',header_format)

        # Fetch records
        vehicle_id=self.vehicle_id.id

        from_date=self.from_date
        to_date=self.to_date

        rows=self.env['rental.request'].get_report_data(
            vehicle_id,

            from_date,
            to_date
        )
        # Data starts after header row
        row = 3
        status_dict = dict(
            self.env['rental.request']._fields['status'].selection
        )


        for rec in rows:
            rent_date = datetime.strptime(
                str(rec['rent_date']),
                '%Y-%m-%d'
            ).strftime('%d-%m-%Y')

            return_date = datetime.strptime(
                str(rec['return_date']),
                '%Y-%m-%d'
            ).strftime('%d-%m-%Y')
            worksheet.write(row, 0, rec['rental_id'],data_format)
            worksheet.write(row, 1, rec['customer_name'],data_format)
            worksheet.write(row, 2, str(rec['vehicle_name']),data_format)
            worksheet.write(row, 3, rent_date,data_format)
            worksheet.write(row, 4, return_date,data_format)
            worksheet.write(row, 5, rec['period'],data_format)
            worksheet.write(
                row,
                6,
                status_dict.get(rec['status']),
                data_format
            )

            row += 1

        # Close workbook LAST
        workbook.close()

        output.seek(0)

        print("Excel Button Clicked")
        print("Excel Headers Created")
        print("Excel Data Written")


        #read the file and convert it to encoded format


        # excel_data=output.read()
        # excel_file=base64.b64encode(excel_data)
        #
        # print(type(excel_file))
        # print(excel_file[:50])
        #
        # #create an attachment in odoo
        # attachment=self.env['ir.attachment'].create({
        #     'name':'Rental_Report.xlsx',
        #     'type':'binary',
        #     'datas':excel_file,
        #     'mimetype':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        # })

        #Excel directly send to browser

