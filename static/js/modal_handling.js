$('#editCampaign').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var name = button.data('name');
    var description = button.data('description');
    var identifier = button.data('identifier')
    var modal = $(this);
    modal.find('.modal-title').text("Kampagne bearbeiten: " + name);
    modal.find('.modal-body input').val(name);
    modal.find('textarea').val(description);
    modal.find('#identifier').val(identifier)
});

$('#pinInfluencer').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var identifier = button.data('identifier');
    var modal = $(this);
    modal.find('.modal-title').text("Influencer hinzufügen: " + identifier);
    currentIdentifier = identifier;
});