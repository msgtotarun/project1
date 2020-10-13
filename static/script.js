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
var lst = [];
var user;
var bookisbn;


function loadDoc() {
  let request = new XMLHttpRequest();
  var res = document.forms["res"]["find"].value;
  user = document.getElementById("username").innerHTML;
  console.log(res);

  //Setting the table display property to block.
  let myElement = document.querySelector(".hide-table");
  myElement.style.display = "block";

  request.open("POST", "/api/search/");
  request.setRequestHeader("Content-Type", "application/json");
  request.send(
    JSON.stringify({
      search: res,
    })
  );
  request.onload = () => {
    if (request.status === 200) {
      console.log("entered3");
      var data = JSON.parse(request.responseText);
      console.log(data);
      let str = "";
      lst = [];

      for (let i = 0; i < data["author"].length; i++) {
        var a = `<img src="http://covers.openlibrary.org/b/isbn/${data["isbn"][i]}-M.jpg" width = "100" height = "150" >`;
        console.log(a);
        str =
          str +
          "<tr>" +
          "<td>" +
          a +
          "</td>" +
          "<td>" +
          "<a href=javascript:bookPage(" +
          i +
          ")>" +
          data["isbn"][i] +
          "</a>" +
          "</td>" +
          "<td>" +
          data["title"][i] +
          "</td>" +
          "<td>" +
          data["author"][i] +
          "</td>" +
          "<td>" +
          data["year"][i] +
          "</td>" +
          "</tr>";
        lst.push(data["isbn"][i]);
        console.log(lst);
      }
      document.getElementById("tb").innerHTML = str;
    } else {
      console.log(`error ${request.status} ${request.statusText}`);
    }
  };
  event.preventDefault();
  return false;
}

function bookPage(isbn) {

  var isbn = lst[isbn];

  bookisbn = isbn;
  console.log(isbn);

  let request = new XMLHttpRequest();
  request.open("POST", "/api/book/");
  request.setRequestHeader("Content-Type", "application/json");
  request.send(JSON.stringify({
    isbn: isbn
  }));

  //Setting the table display property to None.
  let myElement = document.querySelector(".hide-table");
  myElement.style.display = "none";
  document.querySelector(".container").style.display = 'block'

  request.onload = () => {
    if (request.status === 200) {
      var data = JSON.parse(request.responseText);
      console.log(data);

      let str = "";

      str =
        str +
        `<img src="http://covers.openlibrary.org/b/isbn/${isbn}-L.jpg" width = "300" height = "400" class="img2" >` +
        `<table id="tab">
    <tr>
      <thead>
        <h1>${data["title"]}</h1>
      </thead>
    </tr>
    <tr>
      <td class="isbn"><b>ISBN:&nbsp&nbsp</b>${isbn}</td>
      <td><b>Author:&nbsp&nbsp</b>${data["author"]}</td>
    </tr>
    <tr>
      <td><b>Rating:&nbsp&nbsp</b>${data["average_rating"]}</td>
      <td><b>Year Published:&nbsp&nbsp</b>${data["year"]}</td>
    </tr>
    <tr>
      <td><b>Review Count:&nbsp&nbsp</b>${data["average_reviewcount"]}</td>
    </tr>
  </table> `;

      document.querySelector(".clearfix").innerHTML = str;
      var msg = "";
      var flag = false;

      //check if the user has already given review or not.
      for (let i = 0; i < data["username"].length; i++) {
        if (data["username"][i] === user) {
          msg = "You have already reviewed this book. ";
          let reviewSection = document.querySelector(".reviews");
          reviewSection.style.display = "none";
          flag = true;
          console.log(flag);
        }
      }

      //if review was not gives display review section.
      if (flag === false) {
        let reviewSection = document.querySelector(".reviews");
        reviewSection.style.display = "block";
      }

      let rev_str = "";
      //display all the reviews for that book.
      for (let i = 0; i < data["review"].length; i++) {
        rev_str =
          rev_str +
          `<div class="review-body"><p>
        <b>${data["username"][i]}</b> 
        ${data["time_stamp"][i]}<br>
        ${data["review"][i]}</p>
      </div>
      <hr>`;
      }

      let all_rev = "";
      all_rev =
        all_rev +
        `<p style="color:rgb(22, 233, 22);text-align:center;">${msg}</p> 
        <h2 id="heading">Reviews</h2>` +
        rev_str;
      document.querySelector(".reviews1").innerHTML = all_rev;
    }
  };
}

function submitReview(isbn) {
  rating = document.forms["userRating"]["rating"].value;
  rev = document.forms["userRating"]["review"].value;
  console.log(username);
  console.log(bookisbn);
  console.log(rating);
  console.log(rev);

  let request = new XMLHttpRequest();
  request.open("POST", "/api/submit_review/");
  request.setRequestHeader("Content-Type", "application/json");
  request.send(
    JSON.stringify({
      username: username,
      isbn: bookisbn,
      rating: rating,
      reviews: rev,
    })
  );
  request.onload = () => {
    if (request.status === 200) {
      var data = JSON.parse(request.responseText);
      console.log(data);
      setTimeout(function () {}, 2000);

      var msg = "";
      var flag = false;
      for (let i = 0; i < data["username"].length; i++) {
        if (data["username"][i] === usr) {
          msg = "You have already reviewed this book. ";
          let reviewSection = document.querySelector(".reviews");
          reviewSection.style.display = "none";
          flag = true;
          console.log(flag);
        }
      }

      if (flag === false) {
        let reviewSection = document.querySelector(".reviews");
        reviewSection.style.display = "block";
      }
      var usr = document.getElementById("username").innerHTML;
      let rev_str = "";

      for (let i = 0; i < data["review"].length; i++) {
        rev_str =
          rev_str +
          `<div class="review-body">
      <p>
        <b>${data["username"][i]}</b> 
           ${data["time_stamp"][i]}<br>
           ${data["review"][i]}
      </p>
    </div>
      <hr>`;
      }

      let all_rev = "";
      all_rev =
        all_rev +
        `<p style="color:rgb(22, 233, 22);text-align:center;">${msg}</p>
    <h2 id="heading">Reviews</h2>` +
        rev_str;

      document.querySelector(".reviews1").innerHTML = all_rev;
    }
  };
  event.preventDefault();
  return false;
}

window.onload = function () {
  //Setting the table display property to None.
  let myElement = document.querySelector(".hide-table");
  myElement.style.display = "none";
};