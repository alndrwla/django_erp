
$(function () {

  $('#frmPayCheck').on('submit', function (e) {
    e.preventDefault();

    var parameters = new FormData();
    parameters.append('action', $('input[name="action"]').val());
    parameters.append('numCheck', $('input[name="numCheck"]').val());
    parameters.append('name', $('input[name="name"]').val());
    parameters.append('valor', $('input[name="valor"]').val());
    parameters.append('plus', $('input[name="plus"]').val());
    parameters.append('place', $('input[name="place"]').val());
    parameters.append('date', $('input[name="date"]').val());
    parameters.append('payChoice', document.getElementById('id_payChoice').value);

    submit_with_ajax(window.location.pathname, 'Notificación',
      '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
        location.href = '/erp/paycheck/list/';
      });
  });

});

