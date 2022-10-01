let id;
var modal_rem = document.querySelector('.modal-remove')
var btn_delete = document.querySelectorAll('.gallery-text-delete')
btn_delete.forEach((item, index) => {
    item.addEventListener('click', (e) => {
        modal_rem.style.display = 'block'
        id = e.currentTarget.dataset.id
    })
})

const close_btn = document.querySelectorAll('.modal-remove-buttons-cancel')
close_btn.forEach((item, key) => {
    item.addEventListener('click', () => {
        modal_rem.style.display = 'none'
        id = null;
    })
    
})
window.onclick = function(event) {
    if(event.target == modal_rem){
        modal_rem.style.display = 'none'
        id = null;
    }
}

const confirm_btn = document.querySelectorAll('.modal-remove-buttons-confirm')
confirm_btn.forEach((item, key) => {
    item.addEventListener('click', () => {
        if (id) {
            console.log(id)
            fetch("/delete_img/"+id, {method: 'POST'})
            .then((_res) => {
                console.log(_res)
                window.location.reload()
            })
        }
    })
})

const actualBtn = document.querySelector('#actual-btn');

const fileChosen = document.querySelector('#file-chosen');

actualBtn.addEventListener('change', function(){
  fileChosen.textContent = this.files[0].name
})
