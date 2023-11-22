document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.querySelector('#xlsx_file');
  const columnsSelect = document.querySelector('#column_selectors');
  const iconSelect = document.querySelector('#icon_selectors');
  const createMapBtn = document.querySelector('#create-map');
  const downloadAsHTMLButton = document.querySelector('#download-map')
  const downloadAsImageButton = document.querySelector('#download-image')

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
          return response.json();
        }
        throw new Error('Network response was not ok.');
      })
      .then(data => {
        createSelectOptions(data.headers);
      })
      .catch(error => {
        console.error('Fetch error:', error);
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

    iconSelect.style.display = 'block';
    createMapBtn.style.display = 'block';
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
    const selectedFile = fileInput.files[0];

    if (label && lat && lon && icon && color && selectedFile) {
      const formData = new FormData();
      formData.append('label', label);
      formData.append('lat', lat);
      formData.append('lon', lon);
      formData.append('icon', icon);
      formData.append('color', color);
      formData.append('file', selectedFile);

      fetch('/api/get_map/', {
        method: 'POST',
        body: formData
      })
        .then(response => {
          if (response.ok) {
            return response.json();
          }
          throw new Error('Network response was not ok.');
        })
        .then(data => {
          displayMap(data.map_html);
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

    const container = document.getElementById('map-container');
    container.appendChild(iframe);
    enableDownloadButtons()
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
      const mapElement = iframe.contentDocument.querySelector('.folium-map');

      // Wait for iframe content to fully load
      html2canvas(mapElement, {
          useCORS: true,
          ignoreElements: (element) => {
            return element.classList.contains('leaflet-bar') || element.classList.contains('leaflet-control');
          },
        }).then(canvas => {
          const imageData = canvas.toDataURL('image/png');
          const link = document.createElement('a');
          link.href = imageData;
          link.download = 'map.png';
          document.body.appendChild(link);
          document.body.removeChild(link);
        });
        html2canvas(mapElement, {
          useCORS: true,
          ignoreElements: (element) => {
            return element.classList.contains('leaflet-bar') || element.classList.contains('leaflet-control');
          },
        }).then(canvas => {
          const imageData = canvas.toDataURL('image/png');

          const link = document.createElement('a');
          link.href = imageData;
          link.download = 'map.png';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        });
    });

  }
});

 function enableDownloadButtons() {
    const downloadAsHTMLButton = document.getElementById("download-map");
    const downloadAsImageButton = document.getElementById("download-image")
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
}


