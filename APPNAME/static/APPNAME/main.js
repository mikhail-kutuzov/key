//display  modal on click
 
const modalWrapper = document.querySelector(".modals-wrapper");
const cnt = document.querySelector(".container");
const mnc = document.querySelector(".mini_container");
if (modalWrapper){
    function displayModal(id){
        const modal = document.getElementById(id);
        modalWrapper.style.display = "flex";
        modal.style.display = "flex";
        cnt.style.display="none";
        mnc.style.display="none";
        //close modal
        const close = document.getElementById("close-modal");
        close.addEventListener("click", () =>{
            modalWrapper.style.display = "none";
            modal.style.display = "none";
        document.querySelector("header").style.display = "unset";
        cnt.style.display="grid";
        mnc.style.display="block";
        })
        
        document.querySelector("header").style.display = "none";
    }
}

//copy to clipboard
const copies = document.querySelectorAll(".desi");
copies.forEach(copy =>{
    copy.onclick = () =>{
        let elemntToCopy = copy.previousElementSibling;
        elemntToCopy.select();
        document.execCommand("copy");
    }
})

/*Display the actions of the password card for mobile devices*/
const actions = document.querySelectorAll(".actions");
if (actions){
    actions.forEach(action =>{
        action.onclick = () =>{
            const links = action.querySelectorAll("a");
            links.forEach(link =>{
                link.style.display = "flex";
            })
            setTimeout(function(){
                links.forEach(link =>{
                    link.style.display = "none";
                })}
            , 1500)
        }
    })
  }

function toggleFunction() {
    var x = document.getElementsByClassName("myinput");
    for(var i=0;i<x.length;i++){
    if (x[i].type === "password") {
      x[i].type = "text";
    } else {
      x[i].type = "password";
    }
  }

  var y =document.getElementById("dup");
  if(y.style.display=="block")
  y.style.display="none";

  else
  y.style.display="block";
}
