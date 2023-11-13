const modal_wrapper = document.querySelector('.modals-wrapper');

function display_modal(modal_id) {
    const modal = document.getElementById(modal_id);
    modal.style.display = "flex";
    modal_wrapper.style.display = "flex";

    // query all the modals
    const modals = document.querySelectorAll('.modal');
    // for each modal in modals array
    modals.forEach(modal => {
        // if the modal_id is not the current modal_id
        // close it
        if (modal.id !== modal_id) {
            modal.style.display = "none";
        }
    });

    const close_button = document.getElementById("close-modal");
    close_button.addEventListener('click', () => {
        modal.style.display = "none";
        modal_wrapper.style.display = "none";
    document.querySelector("header").style.display = "unset";
    });
    document.querySelector('header').style.display = "none";
}

const copies = document.querySelectorAll(".copy");
copies.forEach(copy => {
    copy.onclick = () => {
        let element_to_copy = copy.previousElementSibling;
        element_to_copy.select();
        document.execCommand("copy");
    }
})

const actions = document.querySelectorAll(".actions");
if(actions){
    actions.forEach(action => {
        action.onclick = () => {
            const links = actions.querySelectorAll("a");
            links.forEach(link => {
                link.style.display = "flex";
            })
            setTimeout(function(){
                links.forEach(link => {
                    link.style.display = "none";
                })}, 3000);
        }
    })
}