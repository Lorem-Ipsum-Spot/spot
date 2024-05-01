let listening = false;
let following = false;
let directions = [0,0];

function MovementButtonDown(element,direction)
{
    /*
    direction guide:
    1 = x, 2 = y
    minus direction meaning: 1 forward / -1 backward
    */
    directions[Math.abs(direction)-1]=(Math.sign(direction));
    sendMovementVector(directions);
    
    element.classList.remove("movementButtonUnactive");
    element.classList.add("movementButtonActive");
    
}

function MovementButtonUp(element,direction)
{   
    if (directions[Math.abs(direction)-1]==0)
    {
        return;
    }
    directions[Math.abs(direction)-1]=0;
    sendMovementVector(directions);
    element.classList.remove("movementButtonActive");
    element.classList.add("movementButtonUnactive");
}

function RotationButtonDown(element,rotation)
{    
    sendRotation(rotation);   
    element.classList.remove("movementButtonUnactive");
    element.classList.add("movementButtonActive");
}

function RotationButtonUp(element,rotation)
{
    sendRotation(0);
    element.classList.remove("movementButtonActive");
    element.classList.add("movementButtonUnactive");
}

function UpDownButton(element,stand)
{
    sendUpDown(stand);
}

function ListeningSwitch(element)
{
    if (listening == false)
    {
        listening = true;
        element.classList.remove("switchButtonUnactive");
        element.classList.add("switchButtonActive");
        element.innerHTML="Listening here";
    }
    else
    {
        listening = false;
        element.classList.remove("switchButtonActive");
        element.classList.add("switchButtonUnactive");
        element.innerHTML = "Listening there";
    }
    sendListeningStatus(listening);
}

function FollowingSwitch(element)
{
    if (following == false)
    {
        following = true;
        element.classList.remove("switchButtonUnactive");
        element.classList.add("switchButtonActive");
        element.innerHTML = "Following";
    }
    else
    {
        following = false;
        element.classList.remove("switchButtonActive");
        element.classList.add("switchButtonUnactive");
        element.innerHTML = "Not following";
    }
    sendFollowingStatus(following);
}
