// Função que adiciona preview aos inputs
function attachPreviewToInput(input) {
    input.addEventListener("change", function () {
        // Remove previews anteriores criados pelo JS
        const old = this.parentNode.querySelector(".js-preview-container");
        if (old) old.remove();

        const previewContainer = document.createElement("div");
        previewContainer.className = "js-preview-container";
        previewContainer.style.marginTop = "10px";

        [...this.files].forEach(file => {
            const reader = new FileReader();
            reader.onload = event => {
                const img = document.createElement("img");
                img.src = event.target.result;
                img.style.width = "120px";
                img.style.margin = "5px";
                img.style.borderRadius = "6px";
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(file);
        });

        this.parentNode.appendChild(previewContainer);
    });
}

// Aplica preview aos inputs existentes
function initPreview() {
    const fileInputs = document.querySelectorAll("input[type='file']");
    fileInputs.forEach(input => attachPreviewToInput(input));
}

// Detecta quando um inline é adicionado dinamicamente
document.addEventListener("DOMNodeInserted", event => {
    if (event.target && event.target.classList && event.target.classList.contains("dynamic-form")) {
        const newInputs = event.target.querySelectorAll("input[type='file']");
        newInputs.forEach(input => attachPreviewToInput(input));
    }
});

// Executa ao carregar a página
document.addEventListener("DOMContentLoaded", initPreview);