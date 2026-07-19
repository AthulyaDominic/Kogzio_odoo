import {PosStore} from "@point_of_sale/app/store/pos_store";
import {patch} from "@web/core/utils/patch";

patch(PosStore.prototype, {
    getActiveRentals() {
        const rentals = this.models["rental.request"].filter(
            rental => rental.status !== "returned"
        );

        console.log("Active Rentals:", rentals);

        return rentals;
    },
    getCustomerRentals(partnerId) {
        return this.getActiveRentals().filter(
            rental => rental.customer_id?.id === partnerId
        );
    },
    getRentalById(rentalId) {
    return this.models["rental.request"].get(rentalId);
},
});