/** @odoo-module **/

import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";

export class RentalPeriod extends Interaction {

    static selector = "#vehicle_rental_form";

    dynamicContent = {
        "#rent_date": {
            "t-on-change": this.calculatePeriod,
        },
        "#return_date": {
            "t-on-change": this.calculatePeriod,
        },
    };

    setup() {
        this.requestDate = this.el.querySelector("#request_date");
        this.rentDate = this.el.querySelector("#rent_date");
        this.returnDate = this.el.querySelector("#return_date");
        this.period = this.el.querySelector("#period");
        this.alertDiv = this.el.querySelector("#date_validation_alert");
    }

    calculatePeriod() {

        // Clear previous alert
        this.alertDiv.innerHTML = "";

        const request = this.requestDate.value;
        const rent = this.rentDate.value;
        const ret = this.returnDate.value;

        // Wait until both dates are entered
        if (!rent || !ret) {
            this.period.value = "";
            return;
        }

        const requestDay = new Date(request);
        const rentDay = new Date(rent);
        const returnDay = new Date(ret);

        // Validation 1
        if (rentDay < requestDay) {

            this.period.value = "";

            this.alertDiv.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Rent Date must be greater than or equal to Request Date.
                </div>
            `;

            return;
        }

        // Validation 2
        if (returnDay <= rentDay) {

            this.period.value = "";

            this.alertDiv.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Return Date must be after Rent Date.
                </div>
            `;

            return;
        }

        // Calculate rental period
        const difference = returnDay - rentDay;
        const days = difference / (1000 * 60 * 60 * 24);

        this.period.value = days;
    }
}

registry.category("public.interactions").add(
    "vehicle_rental.rental_period",
    RentalPeriod
);