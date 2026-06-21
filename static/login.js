document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    // Admin Login
    if (username === "admin" && password === "admin123") {
        window.location.href = "admin.html";
    }

    // Customer Login
    else if (username === "customer" && password === "customer123") {
        window.location.href = "products.html";
    }

    // Invalid Login
    else {
        alert("Invalid Username or Password!");
    }
});