/*
* Verifies card number and displays error messages to the user if information
* entered into the field is incorrect
*/
function cardNum(){
    let inputBox = document.getElementById('cardN').value;
    const el = document.getElementById("cardNspan")
    let changeButton = document.getElementById('butChanger')

    if (!(/^(\d{4}[ -]?){3}\d{4}$/).test(inputBox)){
        el.innerHTML = "Enter your card number in the form of:<br><li>1234123412341234</li> <li>1234-1234-1234-1234</li> <li>1234 1234 1234 1234</li></ul>";
    }else{
        el.innerHTML= ""
        changeButton.innerHTML = '<button class="ButFormatGrey" type="submit" style="margin-top: 0.5rem;" href="{{url_for(orderComp.html)}}">Order Now</button>'
    }
}


/*
* Verifies card cvv code and displays error messages to the user if information
* entered into the field is incorrect
*/
function cardcvv(){
    const el = document.getElementById("cardCvvspan")
    let inputbox = document.getElementById("cvv").value;
    let changeButton = document.getElementById('butChanger')

    if ((inputbox.length < 3) || !(/^\d+$/).test(inputbox)){
        el.innerHTML="Enter your CVV code. This can typically be found on the rear of the card and will appear as a 3 digit code"
        changeButton.innerHTML = '<button class="ButFormatGrey" type="button" style="margin-top: 0.5rem;">Order Now</button>'
    }else{
        el.innerHTML = ""
        changeButton.innerHTML = '<button class="ButFormatGrey" type="submit" style="margin-top: 0.5rem;" href="{{url_for(orderComp.html)}}">Order Now</button>'
    }
    
}

/*
* Verifies card exp date and displays error messages to the user if information
* entered into the field is incorrect
*/
function cardexp(){
    const el = document.getElementById("expspan")
    let inputBox = document.getElementById('expDate').value;
    let changeButton = document.getElementById('butChanger')
    let month = inputBox.slice(0,2)
    month = Number(month)

    if (!(/^(0[1-9]|1[0-2])\/\d{2}$/).test(inputBox)){
        el.innerHTML = "Enter your card expiry date in the form MM/YY";
        changeButton.innerHTML = '<button class="ButFormatGrey" type="button" style="margin-top: 0.5rem;">Order Now</button>'
    } else if ((month > 0 && month < 13)){
        el.innerHTML = ""
        changeButton.innerHTML = '<button class="ButFormatGrey" type="submit" style="margin-top: 0.5rem;" href="{{url_for(orderComp.html)}}">Order Now</button>'
    } else{
        el.innerHTML = "Entered Month is not valid"
        changeButton.innerHTML = '<button class="ButFormatGrey" type="button" style="margin-top: 0.5rem;">Order Now</button>'
    }
}

/*
* Verifies card name and displays error messages to the user if information
* entered into the field is incorrect
*/
function cardH(){
    const el = document.getElementById("cardHspan")
    const inputbox = document.getElementById("cardhName").value

    if ((String(inputbox).length < 2)){
        el.textContent="Enter your cardholder name exactly as it appears on your card";
    }else{
        el.textContent=""
    }
}

/*
* Verifies first line of address and displays error messages to the user if information
* entered into the field is incorrect
*/
function street(){
    const el = document.getElementById("addFspan")
    const inputbox = document.getElementById("addFirst").value

    if (String(inputbox).length < 2){
        el.textContent="Enter the first line of your address";
    }else{
        el.textContent=""
    }

}


/*
* Verifies address town and displays error messages to the user if information
* entered into the field is incorrect
*/
function town(){
    const el = document.getElementById("townspan")
    const inputbox = document.getElementById("addTown").value

    if (String(inputbox).length < 2){
        el.textContent="Enter the town of your address";
    }else{
        el.textContent=""
    }

}

/*
* Verifies address postcode and displays error messages to the user if information
* entered into the field is incorrect
*/
function postcode(){
    const el = document.getElementById("postspan")
    const inputbox = document.getElementById("addPost").value

    if (String(inputbox).length < 2){
        el.textContent="Enter your postcode";
    }else{
        console.log("test2")
        el.textContent=""
    }

}


