
setInterval(sendAll, 1000);

// every time period send info about buttons push-status in the moment
async function sendAll(){
    sendMovementVector();
    sendFollowingStatus();
    sendListeningStatus();
}

// send vector [x,y,z] to server - called periodically.
async function sendMovementVector(){
    const url = "/api/movement";

    const data = {
        dir : directions,
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

// send bool following to server - called periodically.
async function sendFollowingStatus(){
    const url = "/api/followingStatus";

    const data = {
        follow : following,
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

// send bool listening to server - called periodically.
async function sendListeningStatus(){
    const url = "/api/listeningStatus";

    const data = {
        listen : listening,
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

// send bool stop to server - only called when stop clicked.
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

