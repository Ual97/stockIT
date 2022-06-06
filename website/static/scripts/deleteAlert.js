window.addEventListener('load', function() {
    const elements = document.getElementsByClassName('deleteButton');
    console.log(elements);
    for (let element of elements) {
      console.log(element);
      element.addEventListener('click', async function () { //asyc function which allows make await returns
        document.querySelector('.InvisibleDel').classList.replace('InvisibleDel', 'delete');
        console.log(element.id);
        document.querySelector('.delete').innerHTML = `<h1>Are you sure you want to delete this item?</h1>`;
        const yesButton = document.createElement('a');  //creating yes button
        const yes = document.createTextNode('Yes');
        yesButton.appendChild(yes);
        yesButton.setAttribute('class', 'deleteButton');
        tokens = element.id.split('.');
        yesButton.setAttribute('href', `/${tokens[1]}/delete/${tokens[0]}`);
        console.log(element.value);
        const noButton = document.createElement('a');   //creating no button
        const no = document.createTextNode('No');
        noButton.appendChild(no);
        noButton.setAttribute('class', 'cancelButton');
        noButton.setAttribute('onclick', 'document.querySelector(".delete").classList.replace("delete", "InvisibleDel")');
        document.querySelector('.delete').appendChild(yesButton);
        document.querySelector('.delete').appendChild(noButton);
        // creating form to append in popup div:                
        //const form = document.createElement("form");
        //form.setAttribute("id", "form");
        //form.setAttribute("action", `/inventario/update/${element.id}`);
        //form.setAttribute("method", "DELETE");
        //form.appendChild(table);
        //// apending form to popup div
        //document.querySelector('.update').appendChild(form);
  
        // we need to do the same but only with this
        //querySelector('#updateForm').action = `/inventario/update/${element.id}`
        //querySelector('#pId').value = product.id
        //querySelector('#pName').value = product.name
        //querySelector('#pSubsidiary').value = product.subsidiary
        //querySelector('#pQuan').value = product.quantity
        //querySelector('#pCost').value = product.cost
        //querySelector('#pPrice').value = product.price
        //querySelector('#pExpiry').value = product.expiry
        //querySelector('#pReserved').value = product.reserved
        //querySelector('#Cbar').value = product.cbar
     
      });
    };
  });