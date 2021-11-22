const reportBtn = document.getElementById('report-btn')
const img = document.getElementById('img')
const reportForm = document.getElementById('report-form')
const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value // We have two csrf tokens in the page and they are identical.
const modalBody = document.getElementsByClassName('modal-body')[0]


// window.onload = ()=>{
//     dateFields = document.querySelectorAll('input[type=date]')
//     dateFields.forEach((df)=> {
//         df.value = ''
//     })
// }

if (img) {
    reportBtn.classList.remove('not-visible')
}

function removeOldAlerts() {
    const alerts = modalBody.querySelectorAll('.alert')
    console.log('There are ' + alerts.length + ' alerts.')
    alerts.forEach( (alert) => {
        alert.remove()
    })
}

reportBtn.addEventListener('click', () => {
    // The two lines below are to ensure there won't be stuck images if the modal was dismissed without saving previously.
    oldImg = document.getElementById('report-img')
    if (oldImg) oldImg.remove()
    // The bit below is to ensure the image on search page will not disappear when the modal pops up.
    newImg = document.createElement('img')
    imgAttrNames = img.getAttributeNames()
    imgAttrNames.forEach((n) => {
        // console.log(n)
        newImg.setAttribute(n, img.getAttribute(n))
    })
    newImg.setAttribute('id', 'report-img')
    newImg.setAttribute('class', 'w-100') //w-100 scales the img to 100% width of its parent element.
    modalBody.prepend(newImg)

    reportForm.addEventListener('submit', (e) => {
                e.preventDefault()
                const formData = new FormData()
                formData.append('csrfmiddlewaretoken', csrfToken)
                formData.append('name', reportName.value)
                formData.append('remarks', reportRemarks.value)
                formData.append('image', newImg.src)

                $.ajax(
                    {
                        type: 'POST',
                        url: '/reports/save/',
                        data: formData,
                        success: (response) => {
                            // removeOldAlerts()
                            var wrapper = document.createElement('div')
                            wrapper.innerHTML = `
                                <div class="alert alert-success alert-dismissible" role="alert">
                                    Report has been saved successfully.
                                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                </div>`
                            modalBody.prepend(wrapper)
                            reportForm.reset()
                        },
                        error: (error) => {
                            // removeOldAlerts()
                            var wrapper = document.createElement('div')
                            wrapper.innerHTML = `
                                <div class="alert alert-danger alert-dismissible" role="alert">
                                    Failed to create report!
                                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                </div>`
                            modalBody.prepend(wrapper)
                        },
                        processData: false,
                        contentType: false,
                    }
                )
            }
        )
    }
)

