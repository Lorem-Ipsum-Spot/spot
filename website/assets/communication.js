
// get vector [x,y]
async function sendMovementVector(dirs){
    const url = "/api/movement";

    const data = {
        dir : dirs,
    }

    const response = await fetch(url,{
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data),
    })

    .then(response => response.json())
    
    .then(data => {
        console.log('Response from server:', data);
    })
    
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

// get +-1 for rotate to left/right
async function sendRotation(direction){
    const url = "/api/rotation";

    const data = {
        direction : direction,
    }

    const response = await fetch(url,{
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data),
    })

    .then(response => response.json())
    
    .then(data => {
        console.log('Response from server:', data);
    })
    
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

// get true/false for stand/lay down
async function sendUpDown(shouldStand){
    const url = "/api/updown";

    const data = {
        stand : shouldStand,
    }

    const response = await fetch(url,{
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data),
    })

    .then(response => response.json())
    
    .then(data => {
        console.log('Response from server:', data);
    })
    
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

// get bool
async function sendFollowingStatus(flwStatus){
    const url = "/api/followingStatus";

    const data = {
        follow : flwStatus,
    }

    const response = await fetch(url,{
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data),
    })

    .then(response => response.json())
    
    .then(data => {
        console.log('Response from server:', data);
    })
    
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

// get bool
async function sendListeningStatus(lstStatus){
    const url = "/api/listeningStatus";

    const data = {
        listen : lstStatus,
    }

    const response = await fetch(url,{
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data),
    })

    .then(response => response.json())
    
    .then(data => {
        console.log('Response from server:', data);
    })
    
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

// just send
async function stopSpot(){
    const url = "/api/stop";

    const data = {
        stop : true,
    }

    const response = await fetch(url,{
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data),
    })

    .then(response => response.json())
    
    .then(data => {
        console.log('Response from server:', data);
    })
    
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}