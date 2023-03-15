var updateBtns = document.getElementsByClassName('update-cart')

for(var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log(productId, action)

        if (user == 'AnonymousUser'){
            console.log('User is not authenticated')
         
        }
        else {
            updateCartOrder(productId, action)
        }
    })
}


function updateCartOrder(productId, action){
    console.log('User authenticated')

    var url = '/update_item/'

    fetch(url, {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body : JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data', data)
        location.reload()
    })
<<<<<<< HEAD
}
=======
}



>>>>>>> cd7a5ddff68ff288e2cc7fa1f700f5a33b895e1a
