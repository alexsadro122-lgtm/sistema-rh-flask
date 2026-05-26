// Campo de pesquisa
const pesquisa = document.querySelector("#pesquisa");

// Verifica se o input existe
if (pesquisa) {

    pesquisa.addEventListener("keyup", () => {

        // Texto digitado
        const texto = pesquisa.value.toLowerCase();

        // Seleciona todos os cards
        const funcionarios = document.querySelectorAll(".funcionario-card");

        // Percorre todos os cards
        funcionarios.forEach((card) => {

            // Texto completo do card
            const nome = card.textContent.toLowerCase();

            // Verifica se encontrou o texto
            if (nome.includes(texto)) {

                card.style.display = "block";

            } else {

                card.style.display = "none";

            }

        });

    });

}


// Remove popup automaticamente
setTimeout(() => {

    const popup = document.querySelector(".popup");

    if (popup) {
        popup.style.display = "none";
    }

}, 3000);

function confirmarExclusao() {

    return confirm(
        "deseja realmente excluir este funcionário?"

    );

}