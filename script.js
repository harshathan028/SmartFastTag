let balance = 250;
let autoPayEnabled = true;

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Login successful') {
            alert('Login successful!');
            document.querySelector('.login-form').style.display = 'none';
            document.querySelector('.dashboard').style.display = 'block';
            updateBalance();
        } else {
            alert('Invalid username or password');
        }
    });
}

function updateBalance() {
    fetch('/balance')
        .then(response => response.json())
        .then(data => {
            balance = data.balance;
            autoPayEnabled = data.auto_pay_enabled;
            document.getElementById('balance').innerText = balance;
            document.getElementById('auto-pay-status').innerText = autoPayEnabled ? 'Enabled' : 'Disabled';
        });
}

function recharge() {
    const amount = parseInt(document.getElementById('recharge').value);
    if (amount > 0) {
        fetch('/recharge', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ amount })
        })
        .then(response => response.json())
        .then(data => {
            alert(`Recharged ₹${amount}. New balance: ₹${data.new_balance}`);
            updateBalance();
        });
    } else {
        alert('Please enter a valid amount');
    }
}

function deduct() {
    const amount = parseInt(document.getElementById('deduct').value);
    if (amount > 0 && balance >= amount) {
        fetch('/deduct', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ amount })
        })
        .then(response => response.json())
        .then(data => {
            alert(`₹${amount} deducted. Remaining balance: ₹${data.new_balance}`);
            updateBalance();
        });
    } else {
        alert('Insufficient balance or invalid amount');
    }
}

function toggleAutoPay() {
    autoPayEnabled = !autoPayEnabled;
    fetch('/toggle-autopay', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ enabled: autoPayEnabled })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('auto-pay-status').innerText = autoPayEnabled ? 'Enabled' : 'Disabled';
        alert(`Auto-pay is now ${autoPayEnabled ? 'Enabled' : 'Disabled'}`);
    });
}

function logout() {
    document.querySelector('.login-form').style.display = 'block';
    document.querySelector('.dashboard').style.display = 'none';
    alert('Logged out successfully');
}