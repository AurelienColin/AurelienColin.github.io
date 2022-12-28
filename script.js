

function init() {
    for (let i = 1; i <= 99; i++) {
        const button = document.querySelector(`#button-${i}`);
        const container = document.querySelector(`#container-${i}`);
        button.addEventListener('click', () => {
            // Toggle the button text
          container.classList.toggle('expanded');
        });
    };
}

function changeImage(image) {
    var img = document.getElementById("coverImage");
    img.src = image;
}

window.onload = init;