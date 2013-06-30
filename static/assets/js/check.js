console.log("hi");

//make this prettier, oh goodness
function noPackages(){
    $(".page-header")[0].innerHTML="Sadly, you have no packages. Maybe wait and try again later?";
    window.setTimeout(function(){
        $(".page-header")[0].innerHTML="";
    },5000);
}


$(document).ready(function(){
        $("input").keypress(function(e){
            console.log("here");
            if(e.which==13 && $("input")[0].validity.valid){
                var uni = $("input").val();
                console.log(uni);
                var response = $.ajax({
                    type:"GET",
                    url:"/",
                    data:("uni="+uni)
                    }).done(function(data){
                        console.log("data");
                        if(data=="T"){
                            window.location.href="/choose.html";
                        }

                        else{
                            noPackages();
                        }
                    });

            }
        });
});


