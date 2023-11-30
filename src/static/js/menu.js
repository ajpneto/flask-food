//*****************Menu******************//

  var cart = JSON.parse(localStorage.getItem('cart')) || {};
  updatecart(cart);


  $('.divpr').on('click', 'button.cart', function() {
    var itemId = $(this).attr('id');

    if (cart[itemId]) {
      cart[itemId]++;
      qty = cart[itemId][0] + 1;
      cart[itemId][0] = cart[itemId][0] + 1;
    } else {
      qty = 1;
      name = document.getElementById('name'+itemId).innerHTML;
      price = document.getElementById('price'+itemId).innerHTML;
      cart[itemId] = [qty,name,parseInt(price)];
    }
    updatecart(cart);

    // localStorage.setItem('cart', JSON.stringify(cart));
    // console.log(cart);
  });

  updatecart(cart);

  function updatecart(cart) {
    var total = 0;
    for (var item in cart){
      total = total + cart[item][0]
      document.getElementById('div'+item).innerHTML = "<button id='minus"+item+ "'class=' btn btn-danger minus'>-</button> <span id='val"+item+"''>"+cart[item][0]+"</span> <button id='plus"+item+"'class='btn btn-danger plus' > + </button>";
    }
  localStorage.setItem('cart', JSON.stringify(cart));
//  document.getElementById('cart').innerHTML= total;
  }

  $('.divpr').on('click', 'button.minus', function(){
    a=this.id.slice(5,);
    cart[a][0]= cart[a][0] -1;
    cart[a][0] = Math.max(0,cart[a][0])
    document.getElementById('val'+a).InnerHTML= cart[a][0];
    updatecart(cart);
  } )

  $('.divpr').on('click', 'button.plus', function(){
    a=this.id.slice(4,);
    cart[a][0]= cart[a][0] +1;
    document.getElementById('val'+a).InnerHTML= cart[a][0];
    updatecart(cart);
  } )

  var url = window.location.href;
        var params = new URLSearchParams(new URL(url).search);
        var tableValue = params.get('table');
        localStorage.setItem('tableValue', tableValue);
