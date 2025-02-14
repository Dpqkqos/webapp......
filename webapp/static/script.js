document.getElementById('state-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const state = document.getElementById('state-input').value;
    fetch(`/client/${window.location.pathname.split('/')[2]}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `state=${state}`
    }).then(response => response.json())
      .then(data => location.reload());
});