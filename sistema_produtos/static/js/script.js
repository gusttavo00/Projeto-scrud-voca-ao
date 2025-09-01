 function toggleSenha() {
      var senhaInput = document.getElementById("senha");
      if (senhaInput.type === "password") {
        senhaInput.type = "text";
      } else {
        senhaInput.type = "password";
      }
    }

// tempo do pop-up
setTimeout(() => {
  document.querySelectorAll("ul.flash-messages li").forEach(msg => {
    msg.style.opacity = "0";
    setTimeout(() => msg.remove(), 1000);
  });
}, 3000); // tempo igual ao da animação