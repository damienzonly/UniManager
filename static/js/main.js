$(function () {
    $('#datetimepicker1').datetimepicker({
        format: 'YYYY-MM-DD'
    });

    var elem = document.querySelector('.js-switch');
    var init = new Switchery(elem, {
        color: '#28a745',
        secondaryColor: '#dc3545'
    });

    init.enable()
});