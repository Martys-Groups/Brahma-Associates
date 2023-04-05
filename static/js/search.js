const searchit = () => {
    let filter = document.getElementById('search-box').value.toUpperCase();
        console.log(filter)
    let card = document.getElementsByClassName('c-card');



    for (var i = 0; i < card.length; i++) {
        let h2 = card[i].getElementsByTagName('h3')[0];
        console.log(h2)
        let textValue = h2.innerText;


        if (textValue.toUpperCase().indexOf(filter) > -1) {
            card[i].style.display = '';

        } else {
            card[i].style.display = 'none';


        }
    }

}