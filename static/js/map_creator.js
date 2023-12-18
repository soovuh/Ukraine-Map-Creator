document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.querySelector('#xlsx_file');
  const columnsSelect = document.querySelector('#column_selectors');
  const iconSelect = document.querySelector('#icon_selectors');
  const uniqueLabelsInput = document.querySelector('#uniqueLabel')
  const uniqueLabelsContainer = document.querySelector('.form-check')
  const createMapBtn = document.querySelector('#create-map');
  const downloadAsHTMLButton = document.querySelector('#download-map')
  const downloadAsImageButton = document.querySelector('#download-image')
  const refreshButton = document.querySelector('#refresh')
  const errorsModal = document.querySelector('#errors')
  const saveToProfileBtn = document.querySelector("#save")


  fileInput.addEventListener('change', handleFileInputChange);

  createMapBtn.addEventListener('click', handleCreateMapClick);

  function handleFileInputChange(event) {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      fetchData(selectedFile);
    }
  }

function fetchData(selectedFile) {
  const formData = new FormData();
  formData.append('file', selectedFile);

  fetch('/api/get_headers/', {
    method: 'POST',
    body: formData
  })
    .then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw new Error('Network response was not ok.');
      }
    })
    .then(data => {
      cleanModalWindow()
      disableModalBtns()

      if (data.headers) {
        createSelectOptions(data.headers);
      } else {
        displayErrorModal(data.error)
      }
    })
    .catch(error => {
      console.error('Fetch error:', error);
      displayErrorModal('Error fetching data. Please try again later.');
    });
}


  function createSelectOptions(headers) {
    const headerLabelOptions = [];
    const headerLatOptions = [];
    const headerLonOptions = [];

    headers.forEach(header => {
      const createOption = text => {
        const option = document.createElement('option');
        option.value = text;
        option.textContent = text;
        return option;
      };

      const headerLabelOption = createOption(header);
      const headerLatOption = createOption(header);
      const headerLonOption = createOption(header);

      headerLabelOptions.push(headerLabelOption);
      headerLatOptions.push(headerLatOption);
      headerLonOptions.push(headerLonOption);
    });

    appendOptionsToSelect(columnsSelect, headerLabelOptions, 'label-select');
    appendOptionsToSelect(columnsSelect, headerLatOptions, 'lat-select');
    appendOptionsToSelect(columnsSelect, headerLonOptions, 'lon-select');

    createListeners(columnsSelect)

    iconSelect.style.display = 'block';
    createMapBtn.style.display = 'block';
    uniqueLabelsContainer.style.display = 'block';

  }

  function cleanModalWindow() {
    const selectors = document.querySelector('#column_selectors')
    const iconSelect = document.querySelector('#icon_selectors')
    const errors = document.querySelector('#errors')
    const uniqueLabelsContainer = document.querySelector('.form-check')
    errors.innerHTML = ''
    iconSelect.style.display = 'none'
    selectors.innerHTML = ''
    uniqueLabelsContainer.style.display = 'none';

  }

  function createListeners(columnSelect){
    columnSelect.querySelectorAll('select').forEach(select => {
        select.addEventListener('change', () => {
          const selects = columnSelect.querySelectorAll('select')
          const createMapBtn = document.querySelector('#create-map');

          const allSelected = Array.from(selects).every(select => select.value !== '');
            if (allSelected) {
              createMapBtn.removeAttribute('disabled');
            } else {
              disableModalBtns()
            }
        });
    })

  }


  function appendOptionsToSelect(selectElement, options, selectId) {
    const select = document.createElement('select');
    select.setAttribute('id', selectId);
    select.setAttribute('class', 'form-select mb-2');

    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = `Select a header for ${selectId === 'label-select' ? 'label' : selectId === 'lat-select' ? 'latitude' : 'longitude'}`;
    defaultOption.disabled = true;
    defaultOption.selected = true;

    select.appendChild(defaultOption);

    options.forEach(option => {
      select.appendChild(option);
    });

    selectElement.appendChild(select);
  }

  function handleCreateMapClick() {
    const label = getValue('#label-select');
    const lat = getValue('#lat-select');
    const lon = getValue('#lon-select');
    const icon = getValue('#icon-select');
    const color = getValue('#color-select');

    const uniqueLabels = uniqueLabelsInput.checked

    const selectedFile = fileInput.files[0];

    if (label && lat && lon && icon && color && selectedFile) {
      const formData = new FormData();
      formData.append('label', label);
      formData.append('lat', lat);
      formData.append('lon', lon);
      formData.append('icon', icon);
      formData.append('color', color);
      formData.append('file', selectedFile);
      formData.append('unique_labels', uniqueLabels)

      fetch('/api/get_map/', {
        method: 'POST',
        body: formData
      })
        .then(response => {
          if (response.ok) {
            return response.json()
          } else {
            throw new Error('Network response was not ok.');
          }
        })
        .then(data => {
          if(data.map_html) {
            const myModalEl = document.getElementById('downloadModal');
            const modal = bootstrap.Modal.getInstance(myModalEl)
            modal.hide()

            displayMap(data.map_html);
          } else {
            clearErrorModal()
            displayErrorModal(data.error)
          }
        })
        .catch(error => {
          console.error('Fetch error:', error);
        });
    }
  }

  function getValue(selector) {
    return document.querySelector(selector).value;
  }

  function displayMap(htmlContent) {
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const embeddedContent = URL.createObjectURL(blob);

    const iframe = document.createElement('iframe');
    iframe.src = embeddedContent;
    iframe.style.width = '100%';
    iframe.style.height = '100%';

    iframe.sandbox = 'allow-same-origin allow-scripts allow-popups allow-forms';

    const container = document.getElementById('map-container');
    container.appendChild(iframe);
    enableButtons()
    refreshButton.addEventListener('click', () => {
      location.reload();
    })
    downloadAsHTMLButton.addEventListener('click', () => {
      const downloadLink = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadLink;
      link.download = 'map.html';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    })
    downloadAsImageButton.addEventListener('click', () => {
      html2canvas(iframe.contentDocument.querySelector('.folium-map'), {
        useCORS: true,
        ignoreElements: (element) => {
          return element.classList.contains('leaflet-bar') || element.classList.contains('leaflet-control');
        },
      }).then(canvas => {
        const imageData = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.href = imageData;
        link.download = 'map-snapshot.png';
        document.body.appendChild(link);
        link.click(); // Simulate click to trigger download
        document.body.removeChild(link);
      });

    });
    console.log(saveToProfileBtn)
    if(saveToProfileBtn) {
      saveToProfileBtn.addEventListener('click', () => {
        fetch("/api/save/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({html_data: htmlContent})
        })
        .then(response => response.json())
        .then(data => {
          if(data.success)
          alert('Successfully saved map to profile!');
        })
        .catch((err) => alert("Oops! Something goes wrong!"))
      })
    }

  }
});

 function enableButtons() {
    const downloadAsHTMLButton = document.getElementById("download-map");
    const downloadAsImageButton = document.getElementById("download-image")
    const refreshButton = document.getElementById("refresh")
    const createMapButton = document.getElementById("create-map")
    const openModalButton = document.getElementById('generate')
    const saveToProfileBtn = document.getElementById('save')

    if (createMapButton)
        createMapButton.disabled = true;
        createMapButton.classList.remove("btn-primary");
        createMapButton.classList.add("btn-secondary");
    if (openModalButton)
        openModalButton.disabled = true;
        openModalButton.classList.remove("btn-primary");
        openModalButton.classList.add("btn-secondary");
    if (downloadAsHTMLButton) {
        downloadAsHTMLButton.disabled = false;

        downloadAsHTMLButton.classList.remove("btn-secondary");
        downloadAsHTMLButton.classList.add("btn-success");

    }
    if (downloadAsImageButton) {
        downloadAsImageButton.disabled = false;

        downloadAsImageButton.classList.remove("btn-secondary");
        downloadAsImageButton.classList.add("btn-danger");

    }
    if(saveToProfileBtn) {
      saveToProfileBtn.disabled = false

      saveToProfileBtn.classList.remove("btn-secondary");
      saveToProfileBtn.classList.add("btn-info");
      saveToProfileBtn.style.color = '#fff'
    }
    if (refreshButton) {
      refreshButton.disabled = false
      refreshButton.classList.remove("btn-secondary");
      refreshButton.classList.add("btn-primary");
    }
}


function displayErrorModal(errorMessage) {
   const error = document.createElement('div');
   const errorsModal = document.querySelector('#errors')

   error.innerHTML = errorMessage;
   error.style.color = 'red'
   error.style.fontSize = '0.7em'
   error.classList.add('mb-2')

   errorsModal.appendChild(error)
}

function clearErrorModal() {
   const errors = document.querySelector('#errors')
   errors.innerHTML = ''
}

function disableModalBtns() {
  const createMapBtn = document.querySelector('#create-map');
  createMapBtn.setAttribute('disabled', 'true');
}
