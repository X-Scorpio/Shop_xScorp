function sayHello() {
    var name = prompt("What's your name?", "Donald John Trump")
    if (name !== null) {
        alert('Hello, ' + name);
    } else {
        alert("YOU ARE TRUMP!!!!");
    }
}
  
var count = 0;
function printRandom() {
    count++;
    console.log('Random: ', count, Math.random());
}