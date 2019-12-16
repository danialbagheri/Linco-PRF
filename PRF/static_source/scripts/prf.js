console.log("hello");
var mainForm = document.getElementById("mainForm");
var requestType = document.getElementById("requestType");
var typeInfo = document.getElementById("typeInfo");
mainForm.style = "display:none;";

function selectType(element, type) {
  setTimeout(function() {
    mainForm.style = "display:block;";
    requestType.style = "display:none;";
  }, 1000);
  element.classList.toggle("add-selected");
  typeInfo.innerHTML = `You have selected ${type}.`;
}
