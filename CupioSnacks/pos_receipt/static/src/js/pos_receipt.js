odoo.define('pos_receipt.custom', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
//    models.load_fields('pos.order', ['sale_person_id']);
    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function () {
            var result = _super_order.export_for_printing.apply(this, arguments);
//            const order = this.pos.get_order();
            var total_sale_qty = this.get_total_sale_qty()
            var total_return_qty = this.get_total_return_qty()
            var shop = this.pos.config.name
            var barcode = this.barcode
//            var sale_person = this.sale_person_name
//            var mo_date   = new Date();
            var mo_date   = new Date(this.validation_date);
            var month = mo_date.getMonth() + 1
            var times = mo_date.toLocaleTimeString()
            result.total_sale_qty = total_sale_qty
            result.total_return_qty = total_return_qty
            result.shop = shop
            result.barcode = barcode
            result.month = month
            result.times = times
//            result.sale_person = sale_person
            return result;
        },
    });

});