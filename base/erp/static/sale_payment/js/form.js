var vents_payment = {
    items: {
        user: 0,
        sale: 0,
        payment: 0,
        detail: 0,
        subtotal: 0,
    },
};


$(function () {

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
    });

    $('#frmSalePayment').on('submit', function (e) {
        e.preventDefault();

        vents_payment.items.user = document.getElementById('id_user').value;
        vents_payment.items.sale = document.getElementById('id_sale').value;
        vents_payment.items.payment = document.getElementById('id_payment').value;
        vents_payment.items.detail = document.getElementById('id_detail').value;
        vents_payment.items.subtotal = document.getElementById('id_subtotal').value;

        console.log(vents_payment.items.payment)
        if (vents_payment.items.payment == 0.0 || vents_payment.items.payment == 0,0 || vents_payment.items.payment == 0) {
            message_error('Debe al menos tener 0.01 centavos de pago');
            return false;
        }

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents_payment', JSON.stringify(vents_payment.items));

        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                alert_action('Notificación', '¿Desea imprimir la boleta de venta?', function () {
                    window.open('/erp/sale_payment/invoice/pdf/' + response.id + '/', '_blank');
                    location.href = '/erp/sale_payment/index/';
                }, function () {
                    location.href = '/erp/sale_payment/index/';
                });
            });
    });

});

