
document.querySelector('#Generate').addEventListener("click", (e) => {
    e.preventDefault();

    console.log('inside submit');


    let endpoint = "/generate";
    console.log("endpoint: ", endpoint);
    const url = document.getElementById("url").value;
    const output = document.getElementById("output");
    console.log("url:", output);
    const overlay = document.getElementById("overlay");
    const loading = document.getElementById("loading");
    console.log('working')
    overlay.style.display = "flex";
    loading.style.display = "block";
    console.log('overlay done')
    console.log('fetching data')
    fetchData(url, endpoint)
        .then((data) => {
            loading.style.display = "none";
            overlay.style.display = "none";
            console.log('layout done')

            output.style.display = "block";
            console.log(data)
            output.innerHTML = data.content;
            console.log('output done')
        })
        .catch((error) => {
            console.log(error);
        });
    
});



async function fetchData(url, endpoint) {
    try {
        console.log('inside fetch')
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({url: url})
        });
        console.log(response.status);
        if (!response.ok) {
            throw Error(response.statusText);
        }

        console.log('fetch done')

        const data = await response.json();

        console.log(data);
        return data;
    } catch (error) {
        console.log(error);
        throw new Error(`Fetch error: ${error.message}`);
    }
}