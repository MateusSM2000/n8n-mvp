document.addEventListener('DOMContentLoaded', function() {

    // Função principal que gera o preview
    function createPreview(input) {
        // 1. Acha o container pai (a célula da tabela ou a div do campo)
        const parent = input.parentNode;

        // 2. Remove preview antigo se existir
        const old = parent.querySelector(".js-preview-container");
        if (old) old.remove();

        // 3. Se não tiver arquivo selecionado, para por aqui
        if (!input.files || !input.files[0]) return;

        // 4. Cria o container novo
        const previewContainer = document.createElement("div");
        previewContainer.className = "js-preview-container";
        previewContainer.style.marginTop = "10px";

        // 5. Gera as imagens
        Array.from(input.files).forEach(file => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement("img");
                img.src = e.target.result;
                img.style.width = "100px"; // Tamanho um pouco menor para Tabular
                img.style.height = "auto";
                img.style.margin = "5px";
                img.style.borderRadius = "4px";
                img.style.border = "1px solid #ccc";
                img.style.objectFit = "cover";
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(file);
        });

        // 6. Adiciona o container logo após o input
        parent.appendChild(previewContainer);
    }

    // --- O SEGREDO (Event Delegation) ---
    // Em vez de adicionar listener em cada input, adicionamos um no corpo da página.
    // Qualquer mudança em qualquer lugar sobe até aqui ("bubbling").
    document.body.addEventListener('change', function(event) {
        // Verificamos se quem disparou o evento foi um input do tipo file
        if (event.target && event.target.type === 'file') {
            createPreview(event.target);
        }
    });
});