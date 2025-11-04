// Get DOM elements
const registerPanel = document.getElementById('registerPanel');
const loginPanel = document.getElementById('loginPanel');
const switchToLogin = document.getElementById('switchToLogin');
const switchToRegister = document.getElementById('switchToRegister');
const userForm = document.getElementById('userForm');
const loginForm = document.getElementById('loginForm');

// Switch to login panel
switchToLogin.addEventListener('click', (e) => {
  e.preventDefault();
  registerPanel.classList.remove('active');
  loginPanel.classList.add('active');
});

// Switch to register panel
switchToRegister.addEventListener('click', (e) => {
  e.preventDefault();
  loginPanel.classList.remove('active');
  registerPanel.classList.add('active');
});

// Register form submission
userForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  e.stopImmediatePropagation();
  
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('pswrd').value;
  
  const submitBtn = userForm.querySelector('button[type="submit"]');
  submitBtn.textContent = 'Registering...';
  submitBtn.disabled = true;
  
  console.log('Sending data:', { name, email, password });
  
  try {
    const response = await axios.post('http://localhost:8000/send', 
      { name, email, password },
      { headers: { 'Content-Type': 'application/json' } }
    );
    
    console.log('Success:', response.data);
    
    document.getElementById('name').classList.add('success');
    document.getElementById('email').classList.add('success');
    document.getElementById('pswrd').classList.add('success');
    
    alert(response.data.message || 'Registration successful!');
    
    userForm.reset();
    
    setTimeout(() => {
      document.querySelectorAll('input').forEach(input => {
        input.classList.remove('success');
      });
    }, 2000);
    
    setTimeout(() => {
      registerPanel.classList.remove('active');
      loginPanel.classList.add('active');
    }, 1500);
    
  } catch (error) {
    console.error('Full error:', error);
    
    document.getElementById('name').classList.add('error');
    document.getElementById('email').classList.add('error');
    document.getElementById('pswrd').classList.add('error');
    
    if (error.response) {
      console.error('Error response:', error.response.data);
      alert(`Error: ${error.response.data.detail || error.response.data.message || 'Unknown error'}`);
    } else if (error.request) {
      alert('Network error - is the backend running on http://localhost:8000?');
    } else {
      alert(`Error: ${error.message}`);
    }
    
    setTimeout(() => {
      document.querySelectorAll('input').forEach(input => {
        input.classList.remove('error');
      });
    }, 3000);
    
  } finally {
    submitBtn.textContent = 'Register';
    submitBtn.disabled = false;
  }
});

// Login form event handler 

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const email = document.getElementById('loginEmail').value; // Adjust ID
  const password = document.getElementById('loginPassword').value; // Adjust ID 
  const submitBtn = loginForm.querySelector('button[type="submit"]');
  submitBtn.textContent = 'Logging in...';
  submitBtn.disabled = true;
  
  console.log('Logging in:', { email });
  
  try {
    const response = await axios.post('http://localhost:8000/login', 
      { email, password },
      { headers: { 'Content-Type': 'application/json' } }
    );
    
    console.log('Login Success:', response.data);
    
    if (response.data.success) {

      // Store user data
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      // Show success message
      
      // redirects to home page 
      window.location.href = '/dashboard.html'; // Change to your actual page
      // OR if you have a dashboard route: window.location.href = '/dashboard';
    }
    
  } catch (error) {
    console.error('Login error:', error);
    
    if (error.response) {
      alert(`Login failed: ${error.response.data.detail || 'Invalid credentials'}`);
    } else if (error.request) {
      alert('Network error - is the backend running?');
    } else {
      alert(`Error: ${error.message}`);
    }
    
  } finally {
    submitBtn.textContent = 'Login';
    submitBtn.disabled = false;
  }
});