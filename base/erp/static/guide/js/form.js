var tblProducts;
var tblSearchProducts;
var vents = {
    items: {
        sale_location_id: '',
        date_joined: '',
        products: []
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.products, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        $.each(this.items.products, function (pos, dict) {
            dict.pos = pos;

            dict.subtotal = dict.cant * parseFloat(dict.sale_price);
            subtotal += dict.subtotal;
        });

        this.items.subtotal = subtotal;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "full_name"},
                {"data": "stock"},
                {"data": "sale_price"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: data.stock,
                    step: 1
                });

            },
            initComplete: function (settings, json) {

            }
        });
    },
};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    if (!Number.isInteger(repo.id)) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-12 text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.full_name + '<br>' +
        '<b>Stock:</b> ' + repo.stock + '<br>' +
        '<b>PVP:</b> <span class="badge badge-warning">$' + repo.sale_price + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

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

    $('.btnRemoveAll').on('click', function () {
        if (vents.items.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            vents.items.products = [];
            vents.list();
        }, function () {

        });
    });

    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    vents.items.products.splice(tr.row, 1);
                    vents.list();
                }, function () {

                });
        })
        .on('change', 'input[name="cant"]', function () {
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products[tr.row].cant = cant;
            vents.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
        });

    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'ids': JSON.stringify(vents.get_ids()),
                    'term': $('select[name="search"]').val()
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                }
            },
            columns: [
                {"data": "full_name"},
                {"data": "stock"},
                {"data": "sale_price"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a rel="add" class="btn btn-success btn-xs btn-flat"><i class="fas fa-plus"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody')
        .on('click', 'a[rel="add"]', function () {
            var tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            var product = tblSearchProducts.row(tr.row).data();
            product.cant = 1;
            product.subtotal = 0.00;
            vents.add(product);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });

    $('#frmGuide').on('submit', function (e) {
        e.preventDefault();

        if (vents.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de guía');
            return false;
        }

        vents.items.date_joined = $('input[name="date_joined"]').val();
        vents.items.sale_location_id = document.getElementById('sale_location_id').value;

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                window.open('/erp/guide/invoice/pdf/' + response.id + '/', '_blank');
                location.href = '/erp/guide/index/';
            });
    });

    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            headers: {
                    'X-CSRFToken': csrftoken
                },
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_autocomplete',
                    ids: JSON.stringify(vents.get_ids())
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        if (!Number.isInteger(data.id)) {
            return false;
        }
        data.cant = 1;
        data.subtotal = 0.00;
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });

    vents.list();
});

