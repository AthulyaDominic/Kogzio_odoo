# report/rental_request_report.py

from odoo import models
from datetime import datetime



class RentalRequestReport(models.AbstractModel):
    _name = 'report.vehicle_rental.report_rental_request_template'
    _description = 'Rental Request Report'

    def _get_report_values(self, docids, data=None):


        rows = data.get(
            'result'
        )




        status_dict = dict(
            self.env['rental.request']._fields['status'].selection
        )

        return {
            'data':data,
            'rows': rows,
            'status_dict': status_dict,
        }