(function(){
    function getUsers(){
        return JSON.parse(localStorage.getItem('users') || '[]');
    }

    function saveUsers(users){
        localStorage.setItem('users', JSON.stringify(users));
    }

    function sha256Hex(message){
        const enc = new TextEncoder();
        const data = enc.encode(message);
        return crypto.subtle.digest('SHA-256', data).then(hashBuffer => {
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        });
    }

    const registerForm = document.getElementById('registerForm');
    if(registerForm){
        registerForm.addEventListener('submit', async function(e){
            e.preventDefault();
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim().toLowerCase();
            const password = document.getElementById('password').value;
            const confirm = document.getElementById('confirmPassword').value;
            if(password !== confirm){
                alert('Passwords do not match');
                return;
            }
            const users = getUsers();
            if(users.find(u => u.email === email)){
                alert('Email already registered');
                return;
            }
            const hashed = await sha256Hex(password);
            users.push({name, email, passwordHash: hashed});
            saveUsers(users);
            alert('Registration successful. You can now login.');
            window.location.href = 'index.html';
        });
    }

    const loginForm = document.getElementById('loginForm');
    if(loginForm){
        loginForm.addEventListener('submit', async function(e){
            e.preventDefault();
            const email = document.getElementById('email').value.trim().toLowerCase();
            const password = document.getElementById('password').value;
            const users = getUsers();
            const hashed = await sha256Hex(password);
            const user = users.find(u => u.email === email && u.passwordHash === hashed);
            if(user){
                if(document.getElementById('remember') && document.getElementById('remember').checked){
                    localStorage.setItem('session', JSON.stringify({role:'student', email:user.email, name:user.name}));
                } else {
                    sessionStorage.setItem('session', JSON.stringify({role:'student', email:user.email, name:user.name}));
                }
                window.location.href = 'student-dashboard.html';
            } else {
                alert('Invalid email or password');
            }
        });
    }

    const adminForm = document.getElementById('adminLoginForm');
    if(adminForm){
        adminForm.addEventListener('submit', async function(e){
            e.preventDefault();
            const email = document.getElementById('adminEmail').value.trim().toLowerCase();
            const password = document.getElementById('adminPassword').value;
            const ADMIN_EMAIL = 'admin@university.edu';
            const ADMIN_PLAIN = 'admin123';
            const ADMIN_HASH = await sha256Hex(ADMIN_PLAIN);
            const enteredHash = await sha256Hex(password);
            if(email === ADMIN_EMAIL && enteredHash === ADMIN_HASH){
                if(document.getElementById('rememberAdmin') && document.getElementById('rememberAdmin').checked){
                    localStorage.setItem('session', JSON.stringify({role:'admin', email, name:'Administrator'}));
                } else {
                    sessionStorage.setItem('session', JSON.stringify({role:'admin', email, name:'Administrator'}));
                }
                window.location.href = 'admin-dashboard.html';
            } else {
                alert('Invalid admin credentials');
            }
        });
    }

    function protectPage(role, redirectTo){
        try{
            const session = JSON.parse(localStorage.getItem('session') || sessionStorage.getItem('session') || 'null');
            if(!session || session.role !== role){
                window.location.href = redirectTo;
            } else {
                const welcome = document.querySelector('.navbar .text-muted');
                if(welcome && session.name) welcome.textContent = 'Welcome, ' + session.name;
            }
        } catch(e){}
    }

    // robust page detection (works when opened via file://)
    const currentPage = window.location.pathname.split('/').pop();
    if(currentPage === 'student-dashboard.html') protectPage('student','index.html');
    if(currentPage === 'admin-dashboard.html') protectPage('admin','admin-login.html');

    // Attach logout handlers to any element with .logout-link
    document.querySelectorAll('.logout-link').forEach(function(el){
        el.addEventListener('click', function(e){
            e.preventDefault();
            localStorage.removeItem('session');
            sessionStorage.removeItem('session');
            const href = el.getAttribute('href') || 'index.html';
            window.location.href = href;
        });
    });

})();
