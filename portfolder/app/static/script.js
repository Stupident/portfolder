(function(){
    var clack = function(e){
        
        // IE is whack, apparently
        var e = e || window.event;
        if( e.srcElement ) {
            e.target = e.srcElement;
        };
        
        var divs = document.getElementById("awesome-container").childNodes;
        for (var i = 0; i < divs.length; i++){
            if (divs[i].firstChild !== null) {
                divs[i].style.display = "none";
            }
        }
        document.getElementById(e.target.getAttribute("data-container")).style.display = "block";
        var links = document.getElementById("asset-category").childNodes;
        console.log(links)
        for (var j = 0; j < links.length; j++) {
            if (links[j].firstChild !== null) {
                links[j].className = "";
            }
        }
        e.target.className = "selected";
    };

    var links = document.getElementById("asset-category").childNodes;
    for (var i = 0; i < links.length; i++) {
        if (links[i].firstChild !== null) {
            links[i].onclick = clack;
        }
    }
})();

function auto_height(elem) {  /* javascript */
    elem.style.height = "1px";
    elem.style.height = (elem.scrollHeight)+"px";
}

