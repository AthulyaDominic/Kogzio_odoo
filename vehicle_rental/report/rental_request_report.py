# report/rental_request_report.py

from odoo import models


class RentalRequestReport(models.AbstractModel):
    _name = 'report.vehicle_rental.report_rental_request_template'
    _description = 'Rental Request Report'

    def _get_report_values(self, docids, data=None):
        vehicle_id=data.get('vehicle_id')

        from_date=data.get('from_date')
        to_date=data.get('to_date')
        rows = self.env['rental.request'].get_report_data(
            vehicle_id,

            from_date,
            to_date
        )
        status_dict = dict(
            self.env['rental.request']._fields['status'].selection
        )

        return {
            'data': data,
            'rows': rows,
            'status_dict': status_dict,
        }