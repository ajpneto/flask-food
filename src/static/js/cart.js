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
