$('#add_property').on('click', function() {
    var nb_form_groups = $('#add_object').find('.form-group').length - 1;
    $(this).before(
        '<br><div class="form-group"><input name="property' + nb_form_groups/2 +
        '" type="text" class="form-control" placeholder="Property name"></div>' +
        '<div class="form-group"><input name="value' + nb_form_groups/2 +
        '" type="text" class="form-control" placeholder="Value"></div>'
    );
});