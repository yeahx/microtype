$(document).ready(function(){
    url = window.location.href.split('/')[3];
    if(url == "index" or == ""){
        $("#index").attr("class","am-active");
    }
    else if(url == "links"){
        $("#links").attr("class","am-active");
    }
});