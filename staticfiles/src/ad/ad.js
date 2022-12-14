const carModelsPath = '/vehicle/api';
const host = 'http://127.0.0.1:8000';
const options = [];

async function setModel() {
    unsetModels();
    const carField = document.querySelector('.car');
    const modelField = document.querySelector('.model');
    const car = carField[carField.value].innerText;
    let carModels = await getCarModels(car);
    carModels = carModels.map(el => el.model);

    for (let o of options) {
        if (carModels.includes(o.innerText) || o.innerText === '---------')
            modelField.appendChild(o);
    }
}


function unsetModels() {
    const modelField = document.querySelector('.model');
    const opt = Array.from(modelField.getElementsByTagName('option'));

    for (let o of opt) {
        if (!(options.includes(o))) {
            options.push(o);
        }
        modelField.removeChild(o);
    }

    return options;
}


async function getCarModels(car) {
    return await get(`${carModelsPath}/?car=${car}`);
}


function getInit(method, data) {
    const init = {
        'method': method,
        'headers': {}
    }

    if (data) {
        init.headers['Content-Type'] = 'application/json';
        init.body = JSON.stringify(data)
    }

    return init;
}


async function request(path, init) {
    const url = `${host}${path}`;

    try {
        const response = await fetch(url, init);

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message);
        }

        if (response.status === 204) {
            return response
        } else {
            return response.json();
        }

    } catch (error) {
        alert(error.message);
        console.log(error.message);
        throw error;
    }
}


async function get(path) {
    return await request(path, getInit('GET'));
}

function setRequired() {
    const fields = document.querySelectorAll('.ad-form-field');
    Array.from(fields).forEach(el => el.required = false);
}

function imageHasChanged(event) {
    let selectedFile = event.target.files[0];
    let img = document.getElementById(event.target.id.slice(5))
    let reader = new FileReader();
    reader.onload = function () {
        img.src = this.result
    }
    reader.readAsDataURL(selectedFile);
}

function imageOnClick(event) {
    const inputField = document.getElementById('image' + event.target.id);
    inputField.click();
}

function profileImageHasChanged(event) {
    let selectedFile = event.target.files[0];
    let img = document.getElementById('profile-image')
    let reader = new FileReader();
    reader.onload = function () {
        img.src = this.result
    }
    reader.readAsDataURL(selectedFile);
}

function imageOnClickProfile(event) {
    const inputField = document.getElementById('image');
    inputField.click();
}

