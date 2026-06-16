# report/rental_request_report.py

from odoo import models


class RentalRequestReport(models.AbstractModel):
    _name = 'report.vehicle_rental.report_rental_request_template'
    _description = 'Rental Request Report'

    def _get_report_values(self, docids, data=None):

        vehicle_id = data.get('vehicle_ids')
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        query = """
            SELECT *,
                   (SELECT name
                    FROM res_partner
                    WHERE id = rental_request.customer_id)
                   AS customer_name
            FROM rental_request
            WHERE 1=1
        """

        if vehicle_id:
            query += f" AND vehicle_id = {vehicle_id}"

        if from_date:
            query += f" AND request_date >= '{from_date}'"

        if to_date:
            query += f" AND request_date <= '{to_date}'"

        print(query)

        self.env.cr.execute(query)
        rows = self.env.cr.dictfetchall()

        return {
            'data': data,
            'rows': rows,
        }