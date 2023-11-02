const dpath = 'data.json'

async function fetchData(url) {
    try {
        const response = await fetch(url);
        if(!response.ok) {
            throw new Error('Error Status: ${reponse.status}');
        }
        return await response.json()
    } catch(error) {
        console.error("Could not fetch data: ", error);
    }
}


fetchData(dpath).then(data => {
    if (data) {
        console.log("yes it works!")
        console.log(data)
        console.log(data.stats.active_ds)
    }
});
