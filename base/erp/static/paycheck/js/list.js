$(function () {
  $('#data').DataTable({
    responsive: true,
    autoWidth: false,
    destroy: true,
    deferRender: true,
    order: [0, 'desc'],
    ajax: {
      url: window.location.pathname,
      type: 'POST',
      data: {
        'action': 'searchdata'
      },
      dataSrc: "",
      headers: {
                    'X-CSRFToken': csrftoken
                }
    },
    columns: [
      {"data": "id"},
      {"data": "numCheck"},
      {"data": "name"},
      {"data": "valor"},
      {"data": "date"},
      {"data": "payChoice"},
      {"data": "id"},
    ],
    columnDefs: [{
      targets: [-3],
      class: 'text-center',
      orderable: false,
      render: function (data, type, row) {
        var d = new Date();
        var aFecha1 = d.getUTCDate() + "-" + d.getMonth() + "-" + d.getFullYear();

        var aFecha1 = aFecha1.split('-');
        var aFecha2 = row.date.split('-');

        var fFecha1 = Date.UTC(aFecha1[2], aFecha1[1], aFecha1[0]);
        var fFecha2 = Date.UTC(aFecha2[0], aFecha2[1] - 1, aFecha2[2]);

        var dif = fFecha2 - fFecha1;
        var dias = Math.floor(dif / (1000 * 60 * 60 * 24));

        if (parseInt(dias) >= 30) {
          return '<button class="btn btn-sm btn-success">' + row.date + '</button> ';
        } else if (parseInt(dias) >= 10) {
          return '<button class="btn btn-sm btn-warning">' + row.date + '</button> ';
        } else {
          return '<button class="btn btn-sm btn-danger">' + row.date + '</button> ';
        }
      }
    },
      {
        targets: [-2],
        class: 'text-center',
        orderable: false,
        render: function (data, type, row) {
          if (row.payChoice === 'C') {
            return '<button class="btn btn-sm btn-warning">PENDIENTE</button> ';
          } else {
            return '<button class="btn btn-sm btn-success">PAGADO</button> ';
          }
        }
      },
      {
        targets: [-1],
        class: 'text-center',
        orderable: false,
        render: function (data, type, row) {
          var buttons = '<a href="/erp/paycheck/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
          buttons += '<a href="/erp/paycheck/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
          return buttons;
        }
      },
    ],
    rowCallback: function (row, data, index) {
      $('td:eq(0)', row).html(index + 1);
    },
    initComplete: function (settings, json) {

    }
  });
});
