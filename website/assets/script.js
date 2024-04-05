let listening = false;
let following = false;

function ListeningSwitch(element)
{
    if (listening == false)
    {
        listening = true;
        element.classList.remove("switchButton")
        element.classList.add("switchButtonActive");
        element.innerHTML="Listening here";
    }
    else
    {
        listening = false;
        element.classList.remove("switchButtonActive")
        element.classList.add("switchButton");
        element.innerHTML = "Listening there";
    }
}

function FollowingSwitch(element)
{
    if (following == false)
    {
        following = true;
        element.classList.remove("switchButton")
        element.classList.add("switchButtonActive")
        element.innerHTML = "Following";
    }
    else
    {
        following = false;
        element.classList.remove("switchButtonActive")
        element.classList.add("switchButton")
        element.innerHTML = "Not following";
    }
}