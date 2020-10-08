const form = document.getElementById("Rverify");
const Lform = document.getElementById("Lverify");
const name = document.getElementById("Name");
const username = document.getElementById("Username");
const email = document.getElementById("Email");
const password = document.getElementById("Password");
const password2 = document.getElementById("RPassword");
const check = document.getElementById("exampleCheck1");
form.addEventListener("submit", (e) => {
  if (checkInputs()) e.preventDefault();
});

Lform.addEventListener("submit", (e) => {
  if (checkLogin()) e.preventDefault();
});

function checkLogin() {
  const usernameValue = username.value.trim();
  const passwordValue = password.value.trim();
  var f = 1;
  if (usernameValue === "") {
    setErrorFor(username, "Username cannot be blank");
    f = 0;
  } else {
    setSuccessFor(Username);
  }
  if (passwordValue === "") {
    setErrorFor(Password, "Password cannot be blank");
    f = 0;
  } else {
    setSuccessFor(Password);
  }
  if ((f = 0)) return false;
  else return true;
}

function checkInputs() {
  // trim to remove the whitespaces
  const usernameValue = username.value.trim();
  const emailValue = email.value.trim();
  const passwordValue = password.value.trim();
  const password2Value = password2.value.trim();
  var f = 1;

  if (name.value === "") {
    setErrorFor(name, "name cannot be blank");
    f = 0;
  } else {
    setSuccessFor(name);
  }

  if (usernameValue === "") {
    setErrorFor(username, "Username cannot be blank");
    f = 0;
  } else if (isEmail(usernameValue)) {
    setErrorFor(username, "Username cannot be an Email");
    f = 0;
  } else {
    setSuccessFor(Username);
  }

  if (emailValue === "") {
    setErrorFor(Email, "Email cannot be blank");
    f = 0;
  } else if (!isEmail(emailValue)) {
    setErrorFor(Email, "Not a valid email");
    f = 0;
  } else {
    setSuccessFor(Email);
  }
  console.log(checkPass(passwordValue));
  if (!checkPass(passwordValue)) {
    setErrorFor(
      password,
      "password has to be at least 6 characters, with at least one uppercase letter, one lowercase letter, one number and a symbol"
    );
  } else setSuccessFor(password);

  if (password2Value === "") {
    setErrorFor(RPassword, "Retype Password cannot be blank");
    f = 0;
  } else if (passwordValue !== password2Value) {
    setErrorFor(Rpassword, "Passwords does not match");
    f = 0;
  } else {
    setSuccessFor(Rpassword);
  }

  if (!check.checked) {
    setErrorFor(check, "agree terms and conditions");
    f = 0;
  } else setSuccessFor(check);
  if ((f = 0)) return false;
  else return true;
}

function setErrorFor(input, message) {
  const formControl = input.parentElement;
  const small = formControl.querySelector("small");
  small.innerText = message;
  small.style.color = "red";
}

function setSuccessFor(input) {
  const formControl = input.parentElement;
  const small = formControl.querySelector("small");
  small.innerText = "";
}
function checkPass(pass) {
  return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&.])[A-Za-z\d$@$!%*?&.]{6,20}/.test(
    pass
  );
}
function isEmail(email) {
  return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
    email
  );
}
