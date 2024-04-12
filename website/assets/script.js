let listening = false;
let following = false;
let directions = [0,0,0]

function ListeningSwitch(element)
{
    if (listening == false)
    {
        listening = true;
        element.classList.remove("switchButtonUnactive")
        element.classList.add("switchButtonActive");
        element.innerHTML="Listening here";
    }
    else
    {
        listening = false;
        element.classList.remove("switchButtonActive")
        element.classList.add("switchButtonUnactive");
        element.innerHTML = "Listening there";
    }
}

function FollowingSwitch(element)
{
    if (following == false)
    {
        following = true;
        element.classList.remove("switchButtonUnactive")
        element.classList.add("switchButtonActive")
        element.innerHTML = "Following";
    }
    else
    {
        following = false;
        element.classList.remove("switchButtonActive")
        element.classList.add("switchButtonUnactive")
        element.innerHTML = "Not following";
    }
}

function MovementButtonDown(element,direction)
{
    /*
    direction guide:
    1 = x, 2 = y, 3 = z
    minus direction meaning: 1 forward / -1 backward
    */

    directions[Math.abs(direction)-1]=(Math.sign(direction))
}

function MovementButtonUp(element,direction)
{
    direction[Math.abs(direction)-1]=0
}

document.getElementById("buttonForward").addEventListener('click', () =>{
    data = {
        x: "-1",
    }
    url = "/cli/server.py";
    postData(url,data);
    });