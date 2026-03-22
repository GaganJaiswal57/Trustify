document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("upload-form");
    const resultBox = document.getElementById("result-box");
    console.log(form); 
    

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        let fileInput = document.querySelector("input[type=file]");
        let file = fileInput.files[0];

        // ❌ No file
        if (!file) {
            resultBox.classList.add("show");
            resultBox.innerHTML = "<h3 style='color:orange;'>⚠ Please select a file</h3>";
            return;
        }

        // ⏳ Loading
        resultBox.classList.add("show");
        resultBox.innerHTML = "<h3 style='color:blue;'>⏳ Checking...</h3>";

        let formData = new FormData();
        formData.append("file", file);

        try {
            let response = await fetch("/check", {
                method: "POST",
                body: formData
            });

            let data = await response.json();
            console.log("Response:", data);

            // ❌ Check for error
            if (data.error) {
                resultBox.classList.add("show");
                resultBox.innerHTML = "<h3 style='color:red;'>❌ Error: " + data.error + "</h3>";
                return;
            }

            // ✅ Check for result
            if (data.result) {
                let color = data.result === "AI Generated Content" ? "red" : "green";
                resultBox.classList.add("show");
                resultBox.innerHTML = "<h2 style='color:" + color + ";'>📋 Result: " + data.result + "</h2>";
            } else {
                resultBox.classList.add("show");
                resultBox.innerHTML = "<h3 style='color:red;'>❌ No result received</h3>";
            }

        } catch (error) {
            resultBox.classList.add("show");
            resultBox.innerHTML = "<h3 style='color:red;'>❌ Server Error: " + error.message + "</h3>";
            console.error("Fetch error:", error);
        }

    });

});