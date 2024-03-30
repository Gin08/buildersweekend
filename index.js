var input_bar = document.getElementById("input")
// console.log(input_bar)
input_bar.focus()

function appendImage(url) {
    var imageContainer = document.getElementById('imageContainer');
    var lastRow = imageContainer.lastElementChild;

    if (!lastRow || lastRow.childElementCount >= 3) {
        lastRow = document.createElement('div');
        lastRow.className = 'row p-2';
        imageContainer.appendChild(lastRow);
    }

    var col = document.createElement('div');
    col.className = 'col-md-4';

    var img = document.createElement('img');
    img.className = 'img-fluid rounded';
    img.src = url;

    col.appendChild(img);
    lastRow.appendChild(col);
}

input_bar.addEventListener("keypress", async function (event) {
    if (event.key === "Enter") {
        input_text = input_bar.value
        console.log(input_text)
        input_bar.value = ""

        // var prompt = "What kind of pose can we take with " + input_text;
        var prompt = input_text;
        var outputFormat = "webp"
        
        for (let i = 0; i < 3; i++) {
            fetch('http://127.0.0.1:5000/generate-image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prompt: prompt,
                    output_format: outputFormat
                })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.blob();
                })
                .then(blob => {
                    var url = URL.createObjectURL(blob);
                    // var img = document.createElement('img');
                    // img.src = url;
                    // // class="img-fluid rounded"
                    // img.className = "img-fluid rounded m-3"
                    // document.getElementById('imageContainer').appendChild(img);
                    appendImage(url);
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        }
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        });
    }
})


window.addEventListener('scroll', function () {
    var bottomBar = document.getElementById('bottomBar');
    if (window.scrollY > 0) {
        bottomBar.classList.remove('sticky-bottom');
    } else {
        bottomBar.classList.add('sticky-bottom');
    }
});