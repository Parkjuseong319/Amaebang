function getProperties() {
  $.ajax({
    url: '/api/properties',
    type: 'GET',
    dataType: 'json',
    beforeSend: function (xhr) {
      xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val());
    },
    success: function (data) {
      updatePropertyList(data['results']);
    },
    error: function (error) {
      console.log('Error:', error);
    },
  });
}
