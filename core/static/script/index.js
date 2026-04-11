const botoesAbrir = document.querySelectorAll(".abrir-modal");
const modal = document.querySelector("dialog");
const btnFechar = document.getElementById(".fechar-modal");

botoesAbrir.forEach(botao => {
    botao.addEventListener("click", () => {
        modal.showModal();
    });
});



const botaoFechar = document.querySelector(".fechar-modal");

botaoFechar.addEventListener("click", () => {
    modal.close();
});