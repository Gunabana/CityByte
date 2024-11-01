function sanitizeAddress(address) {
  return address.replace(/[^a-zA-Z0-9 ]/g, " "); 
}
function setLoc(address){
  setMap(address);
  var target = document.getElementById("map");
  window.scrollTo({ top: target.offsetTop, behavior: 'smooth'})
}

function setMap(address) {
 address = sanitizeAddress(address);
 document.getElementById("address").innerHTML = address;
document.getElementById("map").src ="a"+address;
}