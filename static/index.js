const formControls = document.querySelectorAll('.form-control-2');
const forms = document.querySelectorAll('form');
const submitButtons = document.querySelectorAll('button[type="submit"]');
const result = document.querySelector('.result');
const overlay = document.querySelector('.result-overlay');
const closeBtn = document.querySelector('#close-btn');

formControls.forEach(control => {
    const checkbox = control.querySelector('.appliance');
    const amount = control.querySelector('.appliance-amount');
    const load = control.querySelector('.appliance-load');

    checkbox.onchange = () => {
        if (checkbox.checked) {
            amount.disabled = false;
            load.disabled = false;
        } else {
            amount.disabled = true;
            load.disabled = true;
        }
    }
});

forms.forEach(form => {
    form.onsubmit = (e) => {
        e.preventDefault();
        submitForm();
    }
});

submitButtons.forEach(button => {
    button.onclick = (e) => {
        e.preventDefault();
        submitForm();
    }
});

overlay.addEventListener('click', () => {
    result.classList.remove('active');
    overlay.classList.remove('active');
});

closeBtn.addEventListener('click', () => {
    result.classList.remove('active');
    overlay.classList.remove('active');
});

function submitForm() {
    if (window.innerWidth < 940) {
        result.classList.add('active');
        overlay.classList.add('active');
    }
}
