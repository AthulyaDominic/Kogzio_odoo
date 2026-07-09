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

    console.log("------------ START ------------");

    const container = this.el.querySelector(".dynamic_snippet_template");

    console.log(container);

    console.log("Has row class ?", container.classList.contains("row"));

    container.replaceChildren(this.renderedContent);


    console.log("Children inserted");

    container.style.display = "flex";
    container.style.flexWrap = "wrap";
    container.style.justifyContent = "space-between";

    container.querySelectorAll(".col-lg-4").forEach((card) => {
    card.style.flex = "0 0 32%";
    card.style.maxWidth = "32%";
});

}
}
/* ---------- Public Interaction ---------- */

registry.category("public.interactions").add(
'vehicle_rental.top_vehicle',TopVehicleSnippet
);

/* ---------- Edit Mixin ---------- */
const TopVehicleSnippetEdit = (I) =>
    class extends I {

        start() {
            super.start();
            console.log("Editor mode started");
        }

    };
/* ---------- Editor Interaction ---------- */
registry.category("public.interactions.edit").add(
    "vehicle_rental.top_vehicle",
    {
        Interaction: TopVehicleSnippet,
        mixin: TopVehicleSnippetEdit,
    }
);