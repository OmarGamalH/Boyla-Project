// register page
let page = document.location.pathname

if (page == "/register"){
let register_form = document.querySelector("#register_form")
let register_pass = document.querySelector("#register_password")
register_pass.oninput = function(){
    let underpassword = document.querySelector("#register_under_password")
    if (Number(register_pass.value.length) <= 5){
        underpassword.style.display = "block"
        underpassword.innerHTML = `The length is: ${register_pass.value.length}/5`
    }else{
        underpassword.style.display = "none"
    }
}


register_form.addEventListener('submit' , function(event){
    let error = document.querySelector("#register_error")
    let first_name = document.querySelector("#register_first_name").value.trim()
    let second_name = document.querySelector("#register_second_name").value.trim()
    let email = document.querySelector("#register_email").value.trim()
    let password = document.querySelector("#register_password").value.trim()
    let gender = document.querySelector("#register_gender_select").value
    let phone = document.querySelector("#register_phone").value
    if (first_name == "" || second_name == "" || email == "" || password == "" || phone == "" || !(/[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+/i.test(email)) || gender == "not_selected" || !/\S+/g.test(first_name) || !/\S+/g.test(second_name)){
        event.preventDefault()
        error.innerHTML = "Please enter all info correctly"
        error.style.display = "block"
    }else if(password.length <= 4){
        event.preventDefault()
        error.innerHTML = "INVALID PASSWORD(Password must be higher than 4)"
        error.style.display = "block"
    }
    if (!/\+?\d+/i.test(phone)){
        event.preventDefault()
        error.innerHTML = "Invalid phone number"
        error.style.display = "block"
    }
})
}




//login page
if (page == "/login"){
let login_form = document.querySelector("#login_form")
login_form.addEventListener('submit' , function(event){
    let login_email = document.querySelector("#login_email").value.trim()
    let login_password = document.querySelector("#login_password").value.trim()
    let login_error = document.querySelector("#login_error")
    if (login_email == "" || login_password == ""){
        event.preventDefault()
        login_error.innerHTML = "You must enter all required info"
        login_error.style.display = "block"
    }
    if (!/[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+/i.test(login_email)){
        event.preventDefault()
        login_error.innerHTML = "Invalid email"
        login_error.style.display = "block"
    }
})

}
// add page
if (page == "/add"){
    let form = document.querySelector("#add_div form")
    form.addEventListener('submit' , function(event){
        let option = document.querySelector("#add_select").value
        let price = document.querySelector("#add_price").value.trim()
        let number = document.querySelector("#add_number").value.trim()
        let short = document.querySelector("#short_textarea").value.trim()
        let long = document.querySelector("#long_textarea").value.trim()
        let error = document.querySelector("#add_error")
        if (option == "not_selected" || price == "" || number == "" || short == "" || long == ""){
            error.innerHTML = "All info required"
            event.preventDefault()
            error.style.display = "block"
        }
        if (!Number.isInteger(Number(price)) && !(/\d+.\d+/i.test(price))){
            error.innerHTML = "Please: Enter actual number in price"
            event.preventDefault()
            error.style.display = "block"
        }
        if(!Number.isInteger(Number(number))){
            event.preventDefault()
            error.innerHTML = "Please: Enter actual number in Number"
            error.style.display = "block"
        }else if(Number(number) < 1){
            event.preventDefault()
            error.innerHTML = "Please: Enter actual number in Number"
            error.style.display = "block"
        }
        if(short.length > 40 || long.length > 500){
            event.preventDefault()
            error.innerHTML = "Please: Enter the correct description"
            error.style.display = "block"
        }




    })
}
// profile page
if (page == "/profile"){
    document.querySelector("#profile_addcash_div form").addEventListener('submit' , function(){
        let cash = document.querySelector("#user_cash").value
        let error = document.querySelector("#add_cash_error")
        if (!Number.isInteger(Number(cash)) && !(/\d+.\d+/.test(cash))){
            error.innerHTML = "Please: Enter actual number in price"
            event.preventDefault()
            error.style.display = "block"
        }
    })
}

//password page
if (page == "/password"){
    document.querySelector("#password_form").addEventListener('submit' , function(event){
        let old_password = document.querySelector("#old_password").value
        let new_password = document.querySelector("#new_password").value
        let email = document.querySelector("#password_email").value
        let error = document.querySelector("#password_error")
        if (old_password == "" || new_password == "" || email == ""){
            event.preventDefault()
            error.innerHTML = "All info required"
            error.style.display = "block"
        }
        if (!(/[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+/i.test(email))){
            event.preventDefault()
            error.innerHTML = "Invalid email"
            error.style.display = "block"
        }

    })



}
