console.log("hey sala")

function load(val){
    const newUrl = val.getAttribute("data-id");
    console.log(newUrl);
    document.getElementById("editHidden").innerHTML = `
        <div class="editnotes">
                    <form action="/edited/${newUrl}" method="post">
                            <input type="text" class="input" name="editedtitle" id="editeddesc" placeholder="Provide new Title....">
                            <textarea type="area" class="input" name="editeddesc" id="editeddesc" placeholder="Hard to code the editing part write Wisely...."></textarea>
                            <button type="submit">Edited..</button>
                        </div>
        `;
}