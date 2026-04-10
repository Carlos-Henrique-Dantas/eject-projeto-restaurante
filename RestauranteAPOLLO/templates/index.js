const listadebotoes = document.querySelectorAll("button");
const modal = document.querySelector("dialog");
const buttonClose = document.querySelector("dialog button")

listadebotoes.forEach(button => {
    button.onclick = function(){
    modal.showModal()
}
});


buttonClose.onclick = function(){
    modal.close()
}