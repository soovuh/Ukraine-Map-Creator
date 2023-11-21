const fileInput = document.querySelector('#xlsx_file');
const columnsSelect = document.querySelector('#column_selectors')
const iconSelect = document.querySelector('#icon_selectors')
const createMapBtn = document.querySelector('#create-map')

fileInput.addEventListener('change', function(event) {
  const selectedFile = event.target.files[0];
  if (selectedFile) {
    const formData = new FormData();
    formData.append('file', selectedFile); // Append the file to the FormData object

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
      const headers = data.headers
      const headerLabelOptions = []
      const headerLatOptions = []
      const headerLonOptions = []
      headers.forEach(header => {
        // Create separate option elements for each select
        const headerLabelOption = document.createElement('option');
        headerLabelOption.value = header;
        headerLabelOption.textContent = header;
        headerLabelOptions.push(headerLabelOption);

        const headerLatOption = document.createElement('option');
        headerLatOption.value = header;
        headerLatOption.textContent = header;
        headerLatOptions.push(headerLatOption);

        const headerLonOption = document.createElement('option');
        headerLonOption.value = header;
        headerLonOption.textContent = header;
        headerLonOptions.push(headerLonOption);
      });

      const selectLabelElement = document.createElement('select');
      selectLabelElement.setAttribute('id', 'label-select');
      const defaultLabelOption = document.createElement('option');
      defaultLabelOption.value = '';
      defaultLabelOption.textContent = 'Select a header for label';
      defaultLabelOption.disabled = true;
      defaultLabelOption.selected = true;
      selectLabelElement.appendChild(defaultLabelOption);

      const selectLatElement = document.createElement('select');
      selectLatElement.setAttribute('id', 'lat-select');
      const defaultLatOption = document.createElement('option');
      defaultLatOption.value = ''; // Set an empty value or any appropriate default value
      defaultLatOption.textContent = 'Select a header for latitude'; // Placeholder text
      defaultLatOption.disabled = true; // Optionally, disable this option
      defaultLatOption.selected = true; // Optionally, set this as the default selected option
      selectLatElement.appendChild(defaultLatOption);

      const selectLonElement = document.createElement('select');
      selectLonElement.setAttribute('id', 'lon-select');
      const defaultLonOption = document.createElement('option');
      defaultLonOption.value = ''; // Set an empty value or any appropriate default value
      defaultLonOption.textContent = 'Select a header for longitude'; // Placeholder text
      defaultLonOption.disabled = true; // Optionally, disable this option
      defaultLonOption.selected = true;
      selectLonElement.appendChild(defaultLonOption);

      headerLabelOptions.forEach(option => {
        selectLabelElement.appendChild(option);
      });
      headerLatOptions.forEach(option => {
        selectLatElement.appendChild(option);
      })
      headerLonOptions.forEach(option => {
        selectLonElement.appendChild(option);
      })
      columnsSelect.appendChild(selectLabelElement)
      columnsSelect.appendChild(selectLatElement)
      columnsSelect.appendChild(selectLonElement)
      iconSelect.style.display = 'block'
    })
    .catch(error => {
      console.error('Fetch error:', error);
    });
  }
});

createMapBtn.addEventListener('click', () => {
    const label = document.querySelector('#label-select').value
    const lat = document.querySelector('#lat-select').value
    const lon = document.querySelector('#lon-select').value
    const icon = document.querySelector('#icon-select').value
    const color = document.querySelector('#color-select').value

    const fileInput = document.querySelector('#xlsx_file');
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
      }).then(response => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Network response was not ok.');
        })
          .then(data => {
            const htmlContent = data.map_html
            const blob = new Blob([htmlContent], { type: 'text/html' });
            const downloadLink = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadLink;
            link.download = 'map.html'; // Specify the filename here
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          })
    }

})


