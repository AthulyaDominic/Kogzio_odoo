/** @odoo-module **/

import { registry } from "@web/core/registry";
import { download } from "@web/core/network/download";

registry.category("ir.actions.report handlers").add("xlsx", async (action) => {
    if (action.report_type !== "xlsx") {
        return;
    }

    await download({
        url: "/rental/excel/report",
        data: action.data,
    });
});