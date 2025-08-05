 // active taps
 document.addEventListener('DOMContentLoaded', function() {
    const currentUrl = window.location.pathname;
    const navLinks = document.querySelectorAll('#nav-tabs a');

    navLinks.forEach(link => {
      if (link.getAttribute('href') === currentUrl) {
        link.classList.add('active-tab');  
      }
    });
  });
   const profile = document.getElementById("profileMenu");
    const dropdown = document.getElementById("dropdownMenu");

    // Toggle dropdown on profile click
    profile.addEventListener("click", function(event) {
      event.stopPropagation(); // Prevent closing immediately
      dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
    });

    // Close dropdown if clicked outside
    window.addEventListener("click", function() {
      dropdown.style.display = "none";
    });

    // Optional: Prevent dropdown closing when clicking inside it
    dropdown.addEventListener("click", function(event) {
      event.stopPropagation();
    });
 

    
  const toggleBtn = document.getElementById('modeToggle');
  const body = document.body;

  // Load saved mode from localStorage
  if (localStorage.getItem("theme") === "dark") {
    body.classList.add("dark-mode");
    toggleBtn.textContent = "☀️ Light Mode";
  }

  toggleBtn.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
    const isDark = body.classList.contains("dark-mode");
    toggleBtn.textContent = isDark ? "☀️ Light Mode" : "🌙 Dark Mode";
    localStorage.setItem("theme", isDark ? "dark" : "light");
  });
