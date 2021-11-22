const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const alertBox = document.getElementById('alert-box')
Dropzone.autoDiscover = false

const thisDropzone = new Dropzone(
    '#file-dropzone', 
    {
        url: '/reports/upload/',
        init: function() {
            this.on('sending', (file, xhr, formData) => {
                formData.append('csrfmiddlewaretoken', csrf)
            })
            this.on('success', (file, response) => {
                console.log(response)
                alertBox.innerHTML = `<div class="alert alert-${response.type} alert-dismissible" role="alert">` 
                + response.msg 
                + `<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>`
                + `</div>`
            })
        },
        maxFiles: 3,
        maxFileSize: 3, //in MB
        acceptedFiles: '.csv', 
    }
)
