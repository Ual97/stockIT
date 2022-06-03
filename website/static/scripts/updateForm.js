

function httpGet(theUrl) {
  let xmlHttpReq = new XMLHttpRequest();
  xmlHttpReq.open("GET", theUrl, false); 
  xmlHttpReq.send(null);
  const Dict = JSON.parse(xmlHttpReq.responseText);
  let List = []
  const results = Dict['results']
  for (let i = 0; results[i]; i++) {
    List.push(results[i]['title'])
  }
  return List
}

window.addEventListener('load', function() {
  const elements = document.getElementsByClassName('updateButton');
  console.log(elements);
  for (let element of elements) {
    console.log(element);
    element.addEventListener('click', function () {   
      document.querySelector('.Invisible').classList.replace('Invisible', 'update');
      console.log(element.id)
      
      const response = httpGet(`/inventory/update/${element.id}`)
      for (var i = 0; response[i]; i++) {
        document.querySelector('.update').append("<li>" + response[i]);
}

    });
  };
});