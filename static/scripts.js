
function updateImage() {
    const img = document.getElementById('automata-image');
    fetch('/image')
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            img.src = url;
        })
        .catch(error => console.error('Error fetching image:', error));
}

setInterval(updateImage, 100); // Actualiza cada 100 ms