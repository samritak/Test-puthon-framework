function submitTest(postUrl) {
  document.getElementById("report-error").style.display = "none";
  document.getElementById("report-error").innerHTML = "";
  var formData = new FormData();
  var fileInput = document.getElementById("fileInput");
  var urlInput = document.getElementById("url").value;

  if (fileInput.files[0] || urlInput != "") {
    var testTicketInput = document.getElementById("test_ticket").value;
    var testDescriptionInput =
      document.getElementById("test_description").value;
    var testNamesInput = document.getElementById("test_names").value;

    if (!testTicketInput || testTicketInput == "") {
      document.getElementById("report-error").innerHTML =
        "Please enter the test ticket number";
      document.getElementById("report-error").style.display = "block";
      return false;
    } else {
      formData.append("test_ticket", testTicketInput);
    }
    if (!testDescriptionInput || testDescriptionInput == "") {
      document.getElementById("report-error").innerHTML =
        "Please enter the test ticket description";
      document.getElementById("report-error").style.display = "block";
      return false;
    } else {
      formData.append("test_description", testDescriptionInput);
    }

    if (testNamesInput && testNamesInput != "") {
      formData.append("test_names", testNamesInput);
    }

    formData.append("classified_id", 2);
    if (urlInput != "") {
      if (
        urlInput.startsWith("https://www.aarp.org/membership/") ||
        urlInput.startsWith("https://www-pi.aarp.org/membership/") ||
        urlInput.startsWith("https://www.aarp.org/lp/") ||
        urlInput.startsWith("https://www-pi.aarp.org/lp/")
      ) {
        formData.append("singleurl", urlInput);
        postUrl = postUrl + "-url";
      } else {
        document.getElementById("report-error").innerHTML =
          "Please enter valid URL in textbox";
        document.getElementById("report-error").style.display = "block";
        return false;
      }
    } else if (fileInput.files[0]) {
      formData.append("file", fileInput.files[0]);
      formData.append("singleurl", "");
      postUrl = postUrl + "-file";
    }

    document.getElementById("submit-btn").style.display = "none";
    document.getElementById("submit-loader").style.display = "block";
    axios({
      method: "post",
      url: "/user/" + postUrl,
      data: formData,
      headers: {
        Accept: "application/json",
        "Content-Type": "multipart/form-data",
      },
      timeout: 0,
    })
      .then((response) => {
        if (response.status == 200) {
          document.getElementById("front-page").style.display = "none";
          document.getElementById("report-page").style.display = "block";
          document.getElementById("report-name").value =
            response.data.file_name;
          document
            .getElementById("report-link")
            .setAttribute("href", response.data.Report + ".pdf");
        } else {
          document.getElementById("report-error").style.display = "block";
          document.getElementById("report-error").innerHTML =
            "There is some error in the report. Please try again";
        }
      })
      .catch((error) => {
        document.getElementById("report-error").style.display = "block";
        document.getElementById("report-error").innerHTML = error;
        document.getElementById("submit-btn").style.display = "block";
        document.getElementById("submit-loader").style.display = "none";
        return false;
      });
  } else {
    document.getElementById("report-error").innerHTML =
      "Please upload the file or enter URL in textbox";
    document.getElementById("report-error").style.display = "block";
  }
}

function submitImageTest() {
  document.getElementById("report-error2").style.display = "none";
  document.getElementById("report-error2").innerHTML = "";
  var formData = new FormData();
  var fileInput = document.getElementById("ImageInput");
  var urlInput = document.getElementById("Imageurl").value;
  var widthInput = document.getElementById('Imagewidth').value;
  var comparisonInput = document.getElementById("comparison_select").value;
  var screenshotInput = "Local Browser";
  var testTicketInput = document.getElementById("test_ticket_img").value;
  var testDescriptionInput = document.getElementById("test_description_img").value;

  var postUrl = "/test-image-compare";
  if (fileInput.files[0] || urlInput != "") {
    formData.append("classified_id", 2);
    if (urlInput != "") {
      if (
        urlInput.startsWith("https://www.aarp.org/membership/") ||
        urlInput.startsWith("https://www-pi.aarp.org/membership/") ||
        urlInput.startsWith("https://www.aarp.org/lp/") ||
        urlInput.startsWith("https://www-pi.aarp.org/lp/")
      ) {
        formData.append("singleurl", urlInput);
        formData.append("input_compare_type", comparisonInput);
        formData.append("ScreenshotInput", screenshotInput);
      } else {
        document.getElementById("report-error2").innerHTML =
          "Please enter valid URL in textbox";
        document.getElementById("report-error2").style.display = "block";
        return false;
      }
    } else {
      document.getElementById("report-error2").innerHTML =
        "Please enter URL in textbox";
      document.getElementById("report-error2").style.display = "block";
      return false;
    }

    if (!testTicketInput || testTicketInput == "") {
      document.getElementById("report-error2").innerHTML =
        "Please enter the test ticket number";
      document.getElementById("report-error2").style.display = "block";
      return false;
    } else {
      formData.append("test_ticket", testTicketInput);
    }
    if (!testDescriptionInput || testDescriptionInput == "") {
      document.getElementById("report-error2").innerHTML =
        "Please enter the test ticket description";
      document.getElementById("report-error2").style.display = "block";
      return false;
    } else {
      formData.append("test_description", testDescriptionInput);
    }

    if (fileInput.files[0]) {
      var reader = new FileReader();
      reader.readAsDataURL(fileInput.files[0]);
      reader.onload = function (e) {
        var image = new Image();
        image.src = e.target.result;
        image.onload = function () {
          var width = this.width;
          if (width != widthInput) {
            document.getElementById("report-error2").innerHTML = "Please enter the correct width of the image.";
            document.getElementById("report-error2").style.display = 'block';
            document.getElementById("submit-btn2").style.display = 'block';
            document.getElementById("submit-loader2").style.display = 'none';
            return false;
          }

          document.getElementById("submit-btn2").style.display = 'none';
          document.getElementById("submit-loader2").style.display = 'block';

          formData.append("file", fileInput.files[0]);

          axios({
            method: "post",
            url: "/user/" + postUrl,
            data: formData,
            headers: {
              Accept: "application/json",
              "Content-Type": "multipart/form-data",
            },
          }).then((response) => {
            if (response.status == 200) {
              document.getElementById("image-page").style.display = "none";
              document.getElementById("img-report-page").style.display = "block";
              document.getElementById("img-report-name1").value =
                response.data.file_name1;
              document
                .getElementById("img-report-link1")
                .setAttribute("href", response.data.Report1);
              document.getElementById("img-report-name2").value =
                response.data.file_name2;
              document
                .getElementById("img-report-link2")
                .setAttribute("href", response.data.Report2);
              document.getElementById("img-report-name3").value =
                response.data.file_name3;
            } else {
              document.getElementById("report-error2").style.display = "block";
              document.getElementById("report-error2").innerHTML =
                "There is some error in the report. Please try again";
            }
          }).catch((error) => {
            console.error(error);
            document.getElementById("report-error2").style.display = "block";
            document.getElementById("report-error2").innerHTML = error;
            document.getElementById("submit-btn2").style.display = "block";
            document.getElementById("submit-loader2").style.display = "none";
            return false;
          });
        };
      }
    } else {
      document.getElementById("report-error2").innerHTML = "Please select figma screenshot";
      document.getElementById("report-error2").style.display = 'block';
      return false;
    }
  } else {
    document.getElementById("report-error2").innerHTML =
      "Please upload the file and enter URL in textbox";
    document.getElementById("report-error2").style.display = "block";
  }
}

// function for showing the uploaded file.
function showUploadFileName(inputid, outputid) {
  document.getElementById(inputid).addEventListener("change", function (e) {
    if (e.target.files[0]) {
      document.getElementById(outputid).innerHTML = e.target.files[0].name;
    }
  });
}
//for showing the uploaded csv file.
if (document.getElementById("fileInput")) {
  showUploadFileName("fileInput", "file-status");
}
//for showing the uploaded figma file.
if (document.getElementById("ImageInput")) {
  showUploadFileName("ImageInput", "file-status2");
}

// Function to update the URL status
function updateUrlStatus() {
  const urlInput = document.getElementById("url");
  const urlStatus = document.querySelector("#url-status");
  urlStatus.textContent = urlInput.value; // Update the status text
}

// Event listener for keyup event
if (document.getElementById("url")) {
  document.getElementById("url").addEventListener("keyup", updateUrlStatus);
}

// Run the function on page load
document.addEventListener("DOMContentLoaded", function () {
  if (document.getElementById("url") && document.getElementById("url-status")) {
    updateUrlStatus(); // Update URL status on initial load
  }
});

// function for highlighting the nav bar with Active page
let pathname = window.location.pathname;
pathname = pathname.split("user/")[1].toLowerCase();

function handleClient(client) {
  document.querySelector("." + client + "-icon").style.display = "block";
  document.querySelector(".sidebar-nav-itm-" + client).classList.add("active");
}

if (pathname.includes("dashboard")) {
  document.querySelector(".sidebar-nav-itm-dashboard").classList.add("active");
} else {
  document.querySelector(".heading").style.display = "none";
}

if (pathname.includes("login")) {
  document.querySelector(".heading").innerHTML = "Login";
  document.querySelector(".heading").style.display = "block";
}

if (pathname.includes("aarp")) {
  handleClient("aarp");
  if (pathname.includes("aarp-image-comparison")) {
    document.querySelector("#front-page").style.display = "none";
    document.querySelector("#image-page").style.display = "block";
  }
}
if (pathname.includes("inogen")) {
  handleClient("inogen");
}
if (pathname.includes("rif")) {
  handleClient("rif");
}
if (pathname.includes("jaya")) {
  handleClient("jaya");
}
if (pathname.includes("greeting")) {
  handleClient("gg");
}

// function for handling selected test checkbox options

function replaceTrailingComma(input) {
  return input.replace(/,$/, ""); // Replace trailing comma with an empty string
}

function handleSelectedTestcases() {
  let count = 0;
  let selectedTests = "";
  document.querySelectorAll(".test-case-link").forEach(function (e) {
    if (e.checked) {
      count = count + 1;
      selectedTests += e.value + ",";
    }
  });
  if (count > 0 && selectedTests !== "") {
    selectedTests = replaceTrailingComma(selectedTests);
    document.querySelector("#test_names").value = selectedTests;
    document.querySelector("#submit-selected-tests").click();
  } else {
    document.querySelector("#test_names_empty_error").innerHTML =
      "Please select the required tests from the above list and continue.";
  }
}

// for opening a new tab after submiting the selected tests
if (document.getElementById("test-selection-Form")) {
  document
    .getElementById("test-selection-Form")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the default form submission

      const testNames = document.getElementById("test_names").value; // Get the value of test_names
      const actionUrl = this.action; // Get the form action URL

      // Construct the URL with query parameters
      const url = new URL(actionUrl, window.location.origin);
      if (testNames) {
        url.searchParams.append("test_names", testNames);
      }

      // Open the URL in a new tab
      window.open(url, "_blank");
    });
}
