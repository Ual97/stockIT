window.addEventListener('load', function() {
  const elements = document.getElementsByClassName('updateButton');
  console.log(elements);
  for (let element of elements) {
    console.log(element);
    element.addEventListener('click', function () {   
      document.querySelector('.Invisible').classList.replace('Invisible', 'update');
      console.log(element.id)
      /**document.querySelector('.update').setAttribute('id', element.id)*/
    });
  };
});