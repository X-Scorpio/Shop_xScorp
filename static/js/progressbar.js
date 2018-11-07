let num = 0;
function load_bar(){
    window.setInterval(load, 50);
}
function load(){
    num += 10;
    let percent_loaded = num + "%";
    if(num === 100){
        clearInterval();
    }
    else{
        document.getElementById("progress").style.width = percent_loaded;
    }
}

load_bar()