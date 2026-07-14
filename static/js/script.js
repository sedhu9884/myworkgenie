document.addEventListener("DOMContentLoaded", () => {

    const tool = document.getElementById("tool");
    const hiddenTool = document.getElementById("selectedTool");

    const form = document.getElementById("uploadForm");

    const browseBtn = document.getElementById("browseBtn");
    const fileInput = document.getElementById("fileInput");

    const dropArea = document.getElementById("dropArea");

    const selectedFile = document.getElementById("selectedFile");

    const loading = document.getElementById("loadingSection");
    const success = document.getElementById("successSection");
    const error = document.getElementById("errorSection");

    const convertBtn = document.getElementById("convertBtn");


    //-----------------------------------
    // Tool Changed
    //-----------------------------------

    function updateTool(){

        hiddenTool.value = tool.value;

        selectedFile.innerHTML = "";

        fileInput.value = "";

        success.style.display = "none";
        error.style.display = "none";

        if(tool.value==="pdf_to_word"){

            fileInput.accept=".pdf";

        }

        else{

            fileInput.accept=".doc,.docx";

        }

    }

    updateTool();

    tool.addEventListener("change",updateTool);


    //-----------------------------------
    // Browse Button
    //-----------------------------------

    browseBtn.addEventListener("click",()=>{

        fileInput.click();

    });


    //-----------------------------------
    // Selected File
    //-----------------------------------

    fileInput.addEventListener("change",()=>{

        if(fileInput.files.length===0){

            selectedFile.innerHTML="";

            return;

        }

        const file=fileInput.files[0];

        if(file.size>100*1024*1024){

            alert("Maximum file size is 100 MB.");

            fileInput.value="";

            return;

        }

        selectedFile.innerHTML=

        "<strong>Selected:</strong><br>"+

        file.name+

        "<br><small>"+

        (file.size/1024/1024).toFixed(2)+

        " MB</small>";

    });


    //-----------------------------------
    // Drag & Drop
    //-----------------------------------

    dropArea.addEventListener("dragover",(e)=>{

        e.preventDefault();

        dropArea.classList.add("drag");

    });

    dropArea.addEventListener("dragleave",()=>{

        dropArea.classList.remove("drag");

    });

    dropArea.addEventListener("drop",(e)=>{

        e.preventDefault();

        dropArea.classList.remove("drag");

        fileInput.files=e.dataTransfer.files;

        fileInput.dispatchEvent(

            new Event("change")

        );

    });

    //-----------------------------------
    // Convert
    //-----------------------------------

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        success.style.display = "none";
        error.style.display = "none";

        if (fileInput.files.length === 0) {

            alert("Please select a file.");

            return;

        }

        convertBtn.disabled = true;

        convertBtn.innerHTML = "Converting...";

        loading.style.display = "block";

        const data = new FormData();

        data.append("tool", hiddenTool.value);

        data.append("file", fileInput.files[0]);

        try {

            const response = await fetch("/convert", {

                method: "POST",

                body: data

            });

            if (!response.ok) {

                let message = "Conversion failed.";

                try {

                    const json = await response.json();

                    message = json.detail;

                }

                catch (e) {

                }

                throw new Error(message);

            }

            const blob = await response.blob();

            const original = fileInput.files[0].name;

            const baseName = original.substring(
                0,
                original.lastIndexOf(".")
            );

            let extension = ".pdf";

            if (hiddenTool.value === "pdf_to_word") {

                extension = ".docx";

            }

            const url = window.URL.createObjectURL(blob);

            const a = document.createElement("a");

            a.href = url;

            a.download = baseName + extension;

            document.body.appendChild(a);

            a.click();

            a.remove();

            window.URL.revokeObjectURL(url);

            loading.style.display = "none";

            success.style.display = "block";

            form.reset();

            selectedFile.innerHTML = "";

            updateTool();

        }

        catch (err) {

            loading.style.display = "none";

            error.style.display = "block";

            error.innerHTML =
                "<strong>Conversion Failed</strong><br><br>" +
                err.message;

        }

        finally {

            convertBtn.disabled = false;

            convertBtn.innerHTML = "Convert";

        }

    });

});    