document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript loaded successfully!");

  const container = document.getElementById('auth-container');
  const signUpButton = document.getElementById('signUp');
  const signInButton = document.getElementById('signIn');

  if (container && signUpButton && signInButton) {
    console.log("Elements found!");
    signUpButton.addEventListener('click', () => {
      container.classList.add("right-panel-active");
    });

    signInButton.addEventListener('click', () => {
      container.classList.remove("right-panel-active");
    });
  } else {
    console.warn("Auth container or buttons not found in DOM");
  }
});

