document.addEventListener("DOMContentLoaded", () => {

    // Campo de pesquisa
    const pesquisa =
    document.querySelector("#pesquisa");

    // Cards dos funcionários
    const funcionarios =
    document.querySelectorAll(".funcionario-card");

    // Verifica se existe
    if (pesquisa) {

        pesquisa.addEventListener("keyup", () => {

            // Texto digitado
            const texto =
            pesquisa.value.toLowerCase();

            // Percorre os cards
            funcionarios.forEach((card) => {

                // Conteúdo do card
                const conteudo =
                card.textContent.toLowerCase();

                // Verifica se encontrou
                if (conteudo.includes(texto)) {

                    card.style.display = "block";

                } else {

                    card.style.display = "none";

                }

            });

        });

    }

});