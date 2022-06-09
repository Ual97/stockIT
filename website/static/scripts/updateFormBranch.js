window.addEventListener('load', function() {
    const elements = document.getElementsByClassName('updateButton');
    console.log(elements);
    for (let element of elements) {
      console.log(element);
      element.addEventListener('click', async function () { //asyc function which allows make await returns
        document.querySelector('.Invisible').classList.replace('Invisible', 'update');
        console.log(element.id)
        // await in fetch return which with wait to conclude the request to then return the json obj
        const data = await (await fetch(`/branch/${element.id}`)).json()
        // filling form with corresponding branch data:
        document.querySelector("#updateForm").setAttribute("action", `/branch/${element.id}`);
        const id = document.querySelector("#idUpdate");
        id.appendChild(document.createTextNode(data.id));
        document.querySelector("#nameUpdate").setAttribute("value", data.name);
        function cancel() {
          document.querySelector('.update').classList.replace('update', 'Invisible')
          id.innerHTML = "";
        }
        const cancelButton = document.querySelector("#cancelButtonUpdate")
        cancelButton.addEventListener("click", cancel);
     
      });
    };
  });