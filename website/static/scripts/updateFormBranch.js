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
        // creating form to append in popup div:                
        console.log(data);
        const form = document.createElement("form");
        form.setAttribute("id", "form");
        form.setAttribute("action", `/branch/${element.id}`);
        form.setAttribute("method", "POST");
        const table = document.createElement("table");
        
        // creating table header with col names:
        const rowNames = document.createElement("tr");
        const colId = document.createElement("th");
        const textId = document.createTextNode("ID");
        colId.appendChild(textId);
        rowNames.appendChild(colId);
        const colName = document.createElement("th")
        const textName = document.createTextNode("Name");
        colName.appendChild(textName);
        rowNames.appendChild(colName);
        const exitButton = document.createElement("th");
        const exit = document.createElement("a");
        
        // appending header to table:
        table.appendChild(rowNames);
        // creating table body with col values:
        const rowValues = document.createElement("tr");
        const rowInputs = document.createElement("tr");
        const colIdValue = document.createElement("td");
        const valueId = document.createTextNode(data.id);
        colIdValue.appendChild(valueId);
        rowInputs.appendChild(colIdValue);
        const colNameValue = document.createElement("td");
        const colNameInput = document.createElement("input");
        colNameInput.setAttribute("type", "text");
        colNameInput.setAttribute("placeholder", "");
        colNameInput.setAttribute("value", data.name);
        colNameInput.setAttribute("name", "name");
        colNameInput.setAttribute("id", "name");
        colNameValue.appendChild(colNameInput);
        rowInputs.appendChild(colNameValue);
        const colSubmit = document.createElement("td");
        const colSumbitInput = document.createElement("input");
        colSumbitInput.setAttribute("type", "submit");
        colSumbitInput.setAttribute("value", "Submit");
        colSubmit.appendChild(colSumbitInput);
        rowInputs.appendChild(colSubmit);
        // appending body to table
        table.appendChild(rowInputs);
        // appending table to form
        form.appendChild(table);
  
        // apending cancel button
        const cancelButton = document.createElement("a");
        const cancelText = document.createTextNode("Cancel");
        cancelButton.appendChild(cancelText);
        cancelButton.setAttribute("class", "cancelButton")
        function cancel() {
          form.removeChild(table);
          form.removeChild(cancelButton);
          document.querySelector('.update').classList.replace('update', 'Invisible')
        }
        cancelButton.addEventListener("click", cancel);
        form.appendChild(cancelButton);
  
        // appending form to popup div
        document.querySelector('.update').appendChild(form);
  
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