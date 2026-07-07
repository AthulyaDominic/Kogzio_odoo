import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { renderToFragment } from "@web/core/utils/render";

export class TopVehicleSnippet extends Interaction {

    static selector = ".s_top_rental_vehicle";

    setup(){
    this.vehicles=[];
    console.log("Top vehicle snippet started");
    }

    async willStart() {

    await this.fetchVehicles();
    this.prepareContent();

}
 async fetchVehicles() {

        this.vehicles = await rpc("/top/vehicle");

        console.log(this.vehicles);

 }
prepareContent() {

    this.renderedContent = renderToFragment(
        "vehicle_rental.top_vehicle_cards",
        {
            vehicles: this.vehicles,
        }
    );
    console.log("Rendered Fragment:", this.renderedContent);

}
start() {

        console.log("start() executed");

        const container = this.el.querySelector(".dynamic_snippet_template");

        console.log("Container:", container);

        container.replaceChildren(this.renderedContent);
    }


}
registry.category("public.interactions").add(
'vehicle_rental.top_vehicle',TopVehicleSnippet
);