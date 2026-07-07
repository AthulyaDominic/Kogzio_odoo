from odoo import http, fields
from odoo.http import request


# class for website
class VehicleRentalWebsite(http.Controller):
    @http.route('/vehicle/rental', auth='public', website=True)
    def vehicle_rental_form(self):
        vehicles = request.env['rental.vehicle'].sudo().search([('status', '=', 'available')])
        return request.render(
            'vehicle_rental.vehicle_rental_form_template', {
                'vehicles': vehicles,
                'today': fields.Date.today(),

            }
        )

    @http.route('/vehicle/rental/submit', type='http', auth='public', website=True, methods=['POST'])
    def submit_rental_request(self, **post):
        customer = request.env['res.partner'].sudo().search([('email', '=', post.get('customer_email'))], limit=1)
        if not customer:
            customer = request.env['res.partner'].sudo().create({
                'name': post.get('customer_name'),
                'email': post.get('customer_email'),
                'phone': post.get('customer_phone')
            })
        rental_request = request.env['rental.request'].sudo().create({
            'customer_id': customer.id,
            'vehicle_id': int(post.get('vehicle_id')),
            'rent_date': post.get('rent_date'),
            'return_date': post.get('return_date')
        })
        return request.render(
            'vehicle_rental.vehicle_rental_success_template',
            {
                'rental_id': rental_request.rental_id,
                'customer': rental_request.customer_id.name,
            }
        )

    # website snippet
    @http.route('/top/vehicle',type="json", auth='public', website=True)
    def top_vehicles(self):
        vehicles = request.env['rental.vehicle'].sudo().search([],order="rental_count desc", limit=3)
        data=[]
        for vehicle in vehicles:
            data.append({
                "id":vehicle.id,
                "name":vehicle.name,
                "price":vehicle.price,
                "status":vehicle.status,
                "rental_count":vehicle.rental_count,
                "image":f"/web/image/rental.vehicle/{vehicle.id}/image_1920"
            })
        return data
