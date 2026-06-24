from odoo import http
from odoo.http import request
import io
import xlsxwriter
from datetime import datetime

from xlwt.ExcelFormulaParser import TRUE_CONST


class XLSXReportController(http.Controller):
    @http.route(
        '/rental/excel/report',
        type='http',
        auth='user'
    )
    def download_excel(self,**kwargs):
        # Fetch records
        vehicle_id=kwargs.get('vehicle_id')
        from_date=kwargs.get('from_date')
        to_date=kwargs.get('to_date')


        rows= request.env['rental.report.wizard'].get_report_data(
            vehicle_id,
            from_date,
            to_date,

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
            'Rental Request Report',
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
            request.env['rental.request']._fields['status'].selection
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

        # Close workbook LAST
        workbook.close()

        output.seek(0)
        response=request.make_response(None,headers=[(
            'Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ),(
            'Content-Disposition','attachment;filename=Rental_Report.xlsx'
        )])
        response.stream.write(output.read())
        return response


