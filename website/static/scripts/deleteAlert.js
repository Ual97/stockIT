window.addEventListener('load', function() {
    const elements = document.getElementsByClassName('deleteButton');
    console.log(elements);
    for (let element of elements) {
      console.log(element);
      element.addEventListener('click', async function () { //asyc function which allows make await returns
        document.querySelector('.InvisibleDel').classList.replace('InvisibleDel', 'delete');
        const yesButton = document.querySelector('#yesDelete');
        tokens = element.id.split('.');
        yesButton.setAttribute('href', `/${tokens[1]}/delete/${tokens[0]}`);
        const noButton = document.querySelector('#noDelete');
        noButton.setAttribute('onclick', 'document.querySelector(".delete").classList.replace("delete", "InvisibleDel")');
      });
    };
  });