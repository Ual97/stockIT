window.addEventListener('load', function() {
  const elements = document.getElementsByClassName('updateButton');
  console.log(elements);
  for (let element of elements) {
    console.log(element);
    element.addEventListener('click', async function () { //asyc function which allows make await returns
      document.querySelector('.Invisible').classList.replace('Invisible', 'update');
      console.log(element.id)
      // await in fetch return which with wait to conclude the request to then return the json obj
      const data = await (await fetch(`/inventario/update/${element.id}`)).json()
      // creating form to append in popup div:                
      console.log(data);
      const form = document.createElement("form");
      form.setAttribute("id", "form");
      form.setAttribute("action", `/inventario/update/${element.id}`);
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
      const colSubsidiary = document.createElement("th")
      const textSubsidiary = document.createTextNode("Subsidiary");
      colSubsidiary.appendChild(textSubsidiary);
      rowNames.appendChild(colSubsidiary);
      const colQuantity = document.createElement("th");
      const textQuantity = document.createTextNode("Quantity");
      colQuantity.appendChild(textQuantity);
      rowNames.appendChild(colQuantity);
      const colCost = document.createElement("th");
      const textCost = document.createTextNode("Cost");
      colCost.appendChild(textCost);
      rowNames.appendChild(colCost);
      const colPrice = document.createElement("th");
      const textPrice = document.createTextNode("Price");
      colPrice.appendChild(textPrice);
      rowNames.appendChild(colPrice);
      const colExpiry = document.createElement("th")
      const textExpiry = document.createTextNode("Expiry");
      colExpiry.appendChild(textExpiry);
      rowNames.appendChild(colExpiry);
      const colReserved = document.createElement("th")
      const textReserved = document.createTextNode("Reserved");
      colReserved.appendChild(textReserved);
      rowNames.appendChild(colReserved);
      const colqr_barCode = document.createElement("th")
      const textColQr_barCode = document.createTextNode("QR/barCode");
      colqr_barCode.appendChild(textColQr_barCode);
      rowNames.appendChild(colqr_barCode);
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
      const colSubsidiaryCol = document.createElement("td");
      const colSubsidiaryValue = document.createElement("label");
      colSubsidiaryValue.setAttribute("for", "sucursal");
      const textSubsidiaryValue = document.createTextNode("Select S");
      colSubsidiaryValue.appendChild(textSubsidiaryValue);
      const colSubsidiaryInput = document.createElement("select");
      colSubsidiaryInput.setAttribute("name", "sucursal");
      colSubsidiaryInput.setAttribute("id", "sucursal");
      for (let i = 0; data.ownerBranches[i]; i++) {
        const option = document.createElement("option");
        option.setAttribute("value", data.ownerBranches[i]);
        const textOption = document.createTextNode(data.ownerBranches[i]);
        option.appendChild(textOption);
        colSubsidiaryInput.appendChild(option);
      }
      colSubsidiaryValue.appendChild(colSubsidiaryInput);
      colSubsidiaryCol.appendChild(colSubsidiaryValue);
      rowInputs.appendChild(colSubsidiaryCol);
      //colSubsidiaryInput.setAttribute("type", "text");
      //colSubsidiaryInput.setAttribute("placeholder", "");
      //colSubsidiaryInput.setAttribute("name", "sucursal");
      //colSubsidiaryInput.setAttribute("id", "sucursal");
      //colSubsidiaryInput.setAttribute("value", data.sucursal);
      //colSubsidiaryValue.appendChild(colSubsidiaryInput);
      //rowInputs.appendChild(colSubsidiaryValue);
      const colQuantityValue = document.createElement("td");
      const colQuantityInput = document.createElement("input");
      colQuantityInput.setAttribute("type", "number");
      colQuantityInput.setAttribute("placeholder", "")
      colQuantityInput.setAttribute("name", "quantity");
      colQuantityInput.setAttribute("id", "quantity");
      colQuantityInput.setAttribute("value", data.quantity);
      colQuantityValue.appendChild(colQuantityInput);
      rowInputs.appendChild(colQuantityValue);
      const colCostValue = document.createElement("td");
      const colCostInput = document.createElement("input");
      colCostInput.setAttribute("type", "number");
      colCostInput.setAttribute("placeholder", "")
      colCostInput.setAttribute("name", "cost");
      colCostInput.setAttribute("id", "cost");
      colCostInput.setAttribute("value", data.cost);
      colCostValue.appendChild(colCostInput);
      rowInputs.appendChild(colCostValue);
      const colPriceValue = document.createElement("td");
      const colPriceInput = document.createElement("input");
      colPriceInput.setAttribute("type", "number");
      colPriceInput.setAttribute("placeholder", "");
      colPriceInput.setAttribute("name", "price");
      colPriceInput.setAttribute("id", "price");
      colPriceInput.setAttribute("value", data.price);
      colPriceValue.appendChild(colPriceInput);
      rowInputs.appendChild(colPriceValue);
      const colExpiryValue = document.createElement("td");
      const colExpiryInput = document.createElement("input");
      colExpiryInput.setAttribute("type", "date");
      colExpiryInput.setAttribute("placeholder", "");
      colExpiryInput.setAttribute("name", "expiry");
      colExpiryInput.setAttribute("id", "expiry");
      colExpiryInput.setAttribute("value", data.expiry);
      colExpiryValue.appendChild(colExpiryInput);
      rowInputs.appendChild(colExpiryValue);
      const colReservedValue = document.createElement("td");
      const colReserverInput = document.createElement("input");
      colReserverInput.setAttribute("type", "number");
      colReserverInput.setAttribute("placeholder", "");
      colReserverInput.setAttribute("name", "qty_reserved");
      colReserverInput.setAttribute("id", "qty_reserved");
      colReserverInput.setAttribute("value", data.qty_reserved);
      colReservedValue.appendChild(colReserverInput);
      rowInputs.appendChild(colReservedValue);
      const colqr_barCodeValue = document.createElement("td");
      const colqr_barCodeInput = document.createElement("input");
      colqr_barCodeInput.setAttribute("type", "text");
      colqr_barCodeInput.setAttribute("placeholder", "");
      colqr_barCodeInput.setAttribute("name", "qr_barcode");
      colqr_barCodeInput.setAttribute("id", "qr_barcode");
      colqr_barCodeInput.setAttribute("value", data.qr_barCode);
      colqr_barCodeValue.appendChild(colqr_barCodeInput);
      rowInputs.appendChild(colqr_barCodeValue);
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