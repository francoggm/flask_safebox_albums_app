var send_obj = {id:0, pin:0}
var modal = document.querySelector('.modal-container')
const cards = document.querySelectorAll('div.card')
cards.forEach(function(item, id) {
    item.addEventListener('click', (e) => {
        modal.style.display = 'block'
        fetch("/get_pin", {
            method: 'POST',
            body: JSON.stringify({id: e.currentTarget.dataset.id})
        }).then((_res) => {
            return _res.json()
        }).then((res) => {
            send_obj['pin'] = res;
        })
        send_obj['id'] = item.dataset.id
    })
})
const cards_without_pin = document.querySelectorAll('.card-without-pin')
cards_without_pin.forEach(function(item, id) {
    item.addEventListener('click', (e) => {
        id = e.currentTarget.dataset.id
        window.location.replace("/images/"+ id)
    })
})

//Modal logic
const inputs = document.querySelectorAll('.modal-input')
inputs.forEach((input, key) => {
    input.addEventListener('keyup', function() {
        if (input.value){
            if(key === 3){
                const user_pin = [...inputs].map((input) => input.value).join('')
                if (user_pin == send_obj['pin']){
                    window.location.replace("/images/"+ send_obj['id'])
                } else {
                    inputs[0].focus()
                    modalText(true)
                    cleanInputs()
                }
            } else {
                inputs[key + 1].focus();
            }
        }
    })
})
const close = document.querySelectorAll('.close')
close.forEach((item, key) => {
    item.addEventListener('click', () => {
        modal.style.display = 'none'
        modal_remove.style.display = 'none'
        cleanModal()
    })
    
})
window.onclick = function(event) {
    if(event.target == modal || event.target == modal_remove){
        modal.style.display = 'none';
        modal_remove.style.display = 'none'
        cleanModal()
    }
}

function cleanInputs(){
    inputs.forEach((input, key) => {
        input.value = ''
    })
}

function cleanModal() {
    modalText(false)
    cleanInputs()
}

function modalText(error=false){
    const no_text = document.querySelector('.modal-text')
    if(!error){
        no_text.innerHTML = ''
    } else {
        no_text.innerHTML = 'Wrong pin, try again!'
    }
}


//Delete album modal logic
const cards_remove = document.querySelectorAll('p.card-remove')
const modal_remove = document.querySelector('div.modal-remove')
const modal_remove_text = document.querySelector('p.modal-remove-text')
const modal_remove_btn_confirm = document.querySelectorAll('button.modal-remove-buttons-confirm')
const modal_remove_btn_cancel = document.querySelectorAll('button.modal-remove-buttons-cancel')
var remove_id;
cards_remove.forEach((item, id) => {
    item.addEventListener('click', (e) => {
        remove_id = e.currentTarget.dataset.id
        modal_remove.style.display = 'block'
        modal_remove_text.innerHTML = `Are you sure you want to delete <strong>${e.currentTarget.dataset.name}</strong> ?`
    })
})
modal_remove_btn_confirm.forEach((item, id) => {
    item.addEventListener('click', () => {
        fetch("/delete_album", {
            method: 'POST',
            body: JSON.stringify({id: remove_id})
        }).then((_res) => {
            window.location.href = '/albums';
        })
        
    })
})
modal_remove_btn_cancel.forEach((item, id) => {
    item.addEventListener('click', ()=> {
        modal_remove.style.display = 'none'
    })
})

const inputs_pin = document.querySelectorAll('.album-create-pin-n')
const input_btn = document.querySelector('#album-create-btn')
const input_btn_label = document.querySelector('.album-create-button')
inputs_pin.forEach((input, key) => {
    input.addEventListener('keyup', function() {
        if (input.value){
            let user_pin = [...inputs_pin].map((input) => input.value).join('')
            if (user_pin.length === 0 || user_pin.length === 4){
                input_btn.disabled = false;
                input_btn_label.classList.remove('album-create-button-disabled')
            } else {
                input_btn.disabled = true;
                input_btn_label.classList.add('album-create-button-disabled')
            }
            if(key !== 3){
                inputs_pin[key + 1].focus();  
            } 
        }
    })
    input.addEventListener('keydown', function() {
        if (input.value){
            let user_pin = [...inputs_pin].map((input) => input.value).join('')
            console.log(user_pin)
            if (user_pin.length === 1){
                input_btn.disabled = false;
                input_btn_label.classList.remove('album-create-button-disabled')
            } else {
                input_btn.disabled = true;
                input_btn_label.classList.add('album-create-button-disabled')
            }
        }
    })
})