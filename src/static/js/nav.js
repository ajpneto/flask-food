      if (localStorage.getItem('cart')==null){
    var cart={};
  }
  else{
    cart = JSON.parse(localStorage.getItem('cart'));
  }
  // console.log(cart);
  var total = 0;
    for (var item in cart){
      total = total + cart[item][0]
      document.getElementById('cart').innerHTML= total;
    }
