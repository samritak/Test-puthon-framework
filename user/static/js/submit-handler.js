function submitTest(postUrl) {
    document.getElementById("report-error").style.display = 'none';
    document.getElementById("report-error").innerHTML = "";
    var formData = new FormData();
    var fileInput = document.getElementById('fileInput');
    var urlInput = document.getElementById('url').value;

    if (fileInput.files[0] || urlInput != "") {
        formData.append("classified_id", 2);
        if(urlInput != "") {
            if(urlInput.startsWith("https://www.aarp.org/membership/") || urlInput.startsWith("https://www-pi.aarp.org/membership/") ){
                 formData.append("singleurl", urlInput);
                postUrl=postUrl+'-url'
            }
            else {
                //alert("Please enter valid url  "+urlInput)
                document.getElementById("report-error").innerHTML = "Please enter valid URL in textbox";
                document.getElementById("report-error").style.display = 'block';
                return false;
           }
         }
        else if(fileInput.files[0]) {
             formData.append("file", fileInput.files[0]);
             formData.append("singleurl", "");
                 postUrl=postUrl+'-file'
         }

        document.getElementById("submit-btn").style.display = 'none';
        document.getElementById("submit-loader").style.display = 'block';
        axios({
                method: 'post',
                url: '/user/' + postUrl,
                data: formData,
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'multipart/form-data'
                },
            })
            .then(response => {
                if(response.status == 200) {
                    document.getElementById("front-page").style.display = 'none';
                    document.getElementById("report-page").style.display = 'block';
                    document.getElementById("report-name").value = response.data.file_name;
                    document.getElementById("report-link").setAttribute("href", response.data.Report + '.pdf')
                } else {
                    document.getElementById("report-error").style.display = 'block';
                    document.getElementById("report-error").innerHTML = "There is some error in the report. Please try again";
                }
            })
            .catch(error => {
                document.getElementById("report-error").style.display = 'block';
                document.getElementById("report-error").innerHTML = error;
                document.getElementById("submit-btn").style.display = 'block';
                document.getElementById("submit-loader").style.display = 'none';
                return false;
            });
    } else {
        document.getElementById("report-error").innerHTML = "Please upload the file or enter URL in textbox";
        document.getElementById("report-error").style.display = 'block';
    }
}

function submitImageTest() {
document.getElementById("report-error2").style.display = 'none';
    document.getElementById("report-error2").innerHTML = "";
    var formData = new FormData();
    var fileInput = document.getElementById('ImageInput');
    var urlInput = document.getElementById('Imageurl').value;
//    selectElement = document.querySelector('#comparison_select');
//    var ComparisonInput = selectElement.options
//                [selectElement.selectedIndex].value;
    var ComparisonInput = document.getElementById('comparison_select').value;
//    alert(ComparisonInput)
    var postUrl='test-Image-compare'
    if (fileInput.files[0] || urlInput != "") {
        formData.append("classified_id", 2);
        if(urlInput != "") {
            if(urlInput.startsWith("https://www.aarp.org/membership/") || urlInput.startsWith("https://www-pi.aarp.org/membership/") ){
                formData.append("input_compare_type", ComparisonInput );
                formData.append("singleurl", urlInput);
                //postUrl=postUrl+'-url'
            }
            else {
                //alert("Please enter valid url  "+urlInput)
                document.getElementById("report-error2").innerHTML = "Please enter valid URL in textbox";
                document.getElementById("report-error2").style.display = 'block';
                return false;
           }
         }
         else
         {
            document.getElementById("report-error2").innerHTML = "Please enter URL in textbox";
            document.getElementById("report-error2").style.display = 'block';
            return false;
         }

        if(fileInput.files[0]) {
             formData.append("file", fileInput.files[0]);
         }
//        alert(formData[0])
//        alert(formData[1])
//        alert(formData[2])
        document.getElementById("submit-btn2").style.display = 'none';
        document.getElementById("submit-loader2").style.display = 'block';
        axios({
                method: 'post',
                url: '/user/' + postUrl,
                data: formData,
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'multipart/form-data'
                },
            })
            .then(response => {
            	console.log(response)
                if(response.status == 200) {
                    document.getElementById("image-page").style.display = 'none';
                    document.getElementById("img-report-page").style.display = 'block';
                    document.getElementById("img-report-name1").value = response.data.file_name1;
                    document.getElementById("img-report-link1").setAttribute("href", response.data.Report1)
                    document.getElementById("img-report-name2").value = response.data.file_name2;
                    document.getElementById("img-report-link2").setAttribute("href", response.data.Report2)
                    document.getElementById("img-report-name3").value = response.data.file_name3;
                    document.getElementById("img-report-link3").setAttribute("href", response.data.Report3)
                    document.getElementById("img-report-name4").value = response.data.file_name4;
                    document.getElementById("img-report-link4").setAttribute("href", response.data.Report4)
                } else {
                    document.getElementById("report-error2").style.display = 'block';
                    document.getElementById("report-error2").innerHTML = "There is some error in the report. Please try again";
                }
            })
            .catch(error => {
            	console.error(error)
                document.getElementById("report-error2").style.display = 'block';
                document.getElementById("report-error2").innerHTML = error;
                document.getElementById("submit-btn2").style.display = 'block';
                document.getElementById("submit-loader2").style.display = 'none';
                return false;
            });
    } else {
        document.getElementById("report-error2").innerHTML = "Please upload the file and enter URL in textbox";
        document.getElementById("report-error2").style.display = 'block';
    }
}
