<script type="text/javascript">
//variables' declaration
var timer        = 0;
var item      = 0;

//function for opening of submenu elements
function openelement(num)
{    
        
        //checks whether there is an open submenu and makes it invisible
        if(item) item.style.visibility = 'hidden';

            //shows the chosen submenu element
                item = document.getElementById(num);
                    item.style.visibility = 'visible';
}

// function for closing of submenu elements
function closeelement()
{
    //closes the open submenu elements and loads the timer with 500ms
    timer = window.setTimeout('if(item) item.style.visibility = 'hidden';',500);
}

//function for keeping the submenu loaded after the end of the 500 ms timer
function keepsubmenu()
{
            window.clearTimeout(timer);
}
//hides the visualized menu after clicking outside of its area and expiring of the loaded timer
document.onclick = closeelement;

</script>
