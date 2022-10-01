const toggler = document.querySelector('#header-toggle')
toggler.addEventListener('click', () => {
    const nav = document.querySelector('#nav-bar'),
    bodypd = document.querySelector('#body-pd'),
    headerpd = document.querySelector('#header')
    console.log(nav, bodypd, headerpd)

    if(nav && bodypd && headerpd) {
        nav.classList.toggle('show')
        toggler.classList.toggle('bx-x')
        bodypd.classList.toggle('body-pd')
        headerpd.classList.toggle('body-pd')
    }
})
