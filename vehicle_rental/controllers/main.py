from odoo import http
from odoo.http import request
import io
import xlsxwriter
from datetime import datetime
import json

from odoo.http import content_disposition


class XLSXReportController(http.Controller):
    @http.route(
        '/rental/excel/report',
        type='http',
        auth='user',csrf=False, methods=['POST']

    )
    def download_excel(self,model,options,output_format,report_name,**kwargs):
        # Convert JSON string back to Python dictionary
        options = json.loads(options)
        print('options:',options)

        # Get the data sent from the wizard
        rows = options.get('result', [])
        print('rows:',rows)

        # Create HTTP response
        response = request.make_response(
            None,
            headers=[
                (
                    'Content-Type',
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                ),
                (
                    'Content-Disposition',
                    content_disposition(report_name + '.xlsx')
                ),
            ]
        )

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
              report_name,
            title_format
        )
        # Border
        header_format = workbook.add_format({
            'bold': True,
            'border': 1
        })

        data_format = workbook.add_format({
            'border': 1
        })

        # Headers
        worksheet.write('A3', 'Rental ID', header_format)
        worksheet.write('B3', 'Customer', header_format)
        worksheet.write('C3', 'Vehicle', header_format)
        worksheet.write('D3', 'Rent Date', header_format)
        worksheet.write('E3', 'Return Date', header_format)
        worksheet.write('F3', 'Period', header_format)
        worksheet.write('G3', 'Status', header_format)



        # Data starts after header row
        row = 3
        status_dict = dict(
            request.env[model]._fields['status'].selection
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
            worksheet.write(row, 0, rec['rental_id'], data_format)
            worksheet.write(row, 1, rec['customer_name'], data_format)
            worksheet.write(row, 2, str(rec['vehicle_name']), data_format)
            worksheet.write(row, 3, rent_date, data_format)
            worksheet.write(row, 4, return_date, data_format)
            worksheet.write(row, 5, rec['period'], data_format)
            worksheet.write(
                row,
                6,
                status_dict.get(rec['status']),
                data_format
            )

            row += 1


        # Close workbook
        workbook.close()

        # Move cursor to beginning
        output.seek(0)

        # Write Excel file into HTTP response
        response.stream.write(output.read())

        # Free memory
        output.close()

        return response


