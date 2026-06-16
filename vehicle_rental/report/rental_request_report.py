# report/rental_request_report.py

from odoo import models


class RentalRequestReport(models.AbstractModel):
    _name = 'report.vehicle_rental.report_rental_request_template'
    _description = 'Rental Request Report'

    def _get_report_values(self, docids, data=None):

        vehicle_id=data.get('vehicle_ids')
        from_date=data.get('from_date')
        to_date=data.get('to_date')



        #fetch using sql query

        if not from_date and not to_date:
            self.env.cr.execute("""
                SELECT *,(SELECT name FROM res_partner WHERE id=rental_request.customer_id) 
                AS customer_name
                FROM rental_request
                WHERE vehicle_id = %s
            """, [vehicle_id])
        else:
            self.env.cr.execute("""
            SELECT * ,(SELECT name FROM res_partner WHERE id=rental_request.customer_id) 
            AS customer_name
            FROM rental_request 
            WHERE vehicle_id=%s 
            AND request_date>=%s 
            AND request_date<=%s""",[vehicle_id,from_date,to_date])

        rows=self.env.cr.dictfetchall()

        print("Rows",rows)
        return {

            'data': data,
            'rows':rows
        }