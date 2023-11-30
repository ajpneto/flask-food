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

//*********************Cart******************//

  if (localStorage.getItem('cart')==null){
    var cart={};
  }
  else{
    cart = JSON.parse(localStorage.getItem('cart'));
  }
  // console.log(cart);

  if ($.isEmptyObject(cart)){
    mystr = `<li class="list-group-item d-flex justify-content-between align-items-center">
    Your Cart is empty Please add some items!!
    <span class="badge bg-primary rounded-pill"></span>
  </li>`
    $('#items').append(mystr);
  }
  else{
  let total_price = 0;
  for (item in cart){
    let name = cart[item][1];
    let qty = cart[item][0];
    let item_price = cart[item][2];
    let subtotal = qty*item_price
    total_price = total_price + qty*item_price;
    mystr = `<li class="list-group-item d-flex justify-content-between align-items-center">
    ${qty} ${name}
    <span class="badge bg-primary rounded-pill">R$ ${subtotal},00</span>
  </li>`
    $('#items').append(mystr);

  }
    var total = "R$ " + total_price.toFixed(2);
    total = total.replace(".",",");
    document.getElementById('total').innerHTML = `<br><li class="list-group-item d-flex justify-content-between align-items-center">
    <strong>Total</strong>
    <span class="badge bg-primary rounded-pill" style="padding:10px">${total}</span>
  </li>`
    $('#price_input').val(JSON.stringify(total_price));
  }

$('#itemsjson').val(JSON.stringify(cart));


  $('.clear_cart').click(function (event) {
    event.preventDefault();
    localStorage.removeItem('cart');
    $('#items').empty();
    mystr = `<li class="list-group-item d-flex justify-content-between align-items-center">
    Your Cart is empty. Please add some items!!
    <span class="badge bg-primary rounded-pill"></span>
  </li>`;
    $('#items').append(mystr);
  });

function clearLocalStorage() {
    localStorage.removeItem('cart');
  }

  $('form').submit(function () {
    clearLocalStorage();

  });

  var tableValue = localStorage.getItem('tableValue');
  document.getElementById('tableValueInput').value = tableValue;

  $('form').submit(function () {
  document.location= '/';
  });

//******************All Orders*********************//

  function generateBill(table) {
    window.location.href = '/generate_bill?table=' + table;
  }


//******************Generate Bills****************//

    function printBill() {
        window.print();
    }


