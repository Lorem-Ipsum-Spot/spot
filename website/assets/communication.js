
setInterval(sendAll, 1000);

async function sendAll(){
    sendMovementVector();
    sendFollowing();
}


async function sendMovementVector(){
    const url = "/cli/server.py";

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


async function sendFollowing(){
    const url = "/cli/voky.py";

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

