document.addEventListener('DOMContentLoaded', () => {
    const downloadAsHTMLBtns = document.querySelectorAll('.download-map')
    const downloadAsImageBtns = document.querySelectorAll('.download-image')
    const deleteMapBtns = document.querySelectorAll('.delete-map')

    downloadAsHTMLBtns.forEach((btn) => {
        btn.addEventListener("click", (event) => {
            const mapID = event.target.id
            fetchHTMLMap(mapID)
        })
    })

    deleteMapBtns.forEach((btn) => {
        btn.addEventListener("click", (event) => {
            const mapID = event.target.id
            deleteMap(mapID)
        })
    })

    
    downloadAsImageBtns.forEach((btn) => {
        btn.addEventListener("click", (event) => {
            const mapID = event.target.id
            const iframe = document.querySelector(`#iframe-${mapID}`)
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
                link.click();
                document.body.removeChild(link);
              });
        })
    })

    function fetchHTMLMap(id) {
        const url = `/api/get_html_map/${id}/`
        fetch(url)
            .then(response => response.json())
            .then(data => downloadHTMLMap(data))
    }

    function downloadHTMLMap(data) {
        const parts = data.html.split('/')
        const name = parts[parts.length - 1]
        const link = document.createElement('a');
        link.href = data.html;
        link.download = `${name}.html`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    function deleteMap(id) {
        const url = `/api/delete_map/${id}/`
        fetch(url)
            .then(response => response.json())
            .then(data => {
                location.reload()
            })
}
  });