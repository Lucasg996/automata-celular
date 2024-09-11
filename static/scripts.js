let isMuted = false;
let volume = 1.0;
const muteButton = document.getElementById('mute-button');
const volumeSlider = document.getElementById('volume-slider');

muteButton.addEventListener('click', () => {
    isMuted = !isMuted;
    muteButton.textContent = isMuted ? 'Unmute' : 'Mute';
    volumeSlider.value = isMuted ? 0 : volume;
    fetch(`/mute`);
});

volumeSlider.addEventListener('input', (event) => {
    volume = event.target.value;
    if (!isMuted) {
        fetch(`/set_volume/${volume}`);
    }
});

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

setInterval(updateImage, 100); // Actualiza la imagen cada 100 ms
