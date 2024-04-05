let listening = false;

function ListeningSwitch(element)
{
    if (listening == false)
    {
        listening = true;
        element.style.backgroundColor="green";
        element.innerHTML="Listening here";
    }
    else
    {
        listening = false;
        element.style = null;
        element.innerHTML = "Listening there";
    }
}