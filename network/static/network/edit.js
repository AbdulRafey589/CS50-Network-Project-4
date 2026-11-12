const editButtons = document.querySelectorAll(".edit-button");
    editButtons.forEach(editButton =>{
       editButton.addEventListener('click', function(){
        const postContainer = this.closest(".post-container");
        const postContent = postContainer.querySelector(".post-content");
        const textarea = document.createElement("textarea");
        const originalText = postContent.textContent;
        textarea.value = postContent.textContent;
        postContent.replaceWith(textarea);


        const postId = this.dataset.postId;

        const save = document.createElement("button");
        save.textContent = "Save";
        save.type = "button";

        const cancel = document.createElement("button");
        cancel.textContent = "Cancel";
        cancel.type = "button";

        postContainer.append(save, cancel);
        textarea.after(save, cancel);
        save.className = "btn btn-outline-success";
        cancel.className = "btn btn-outline-danger";

        cancel.addEventListener('click', function(){
            postContent.textContent = originalText;
            textarea.replaceWith(postContent);
            save.remove();
            cancel.remove();
        });




        save.addEventListener('click', function(){
            const csrfToken = document.querySelector(
            '[name=csrfmiddlewaretoken]'
                ).value;
            fetch(`/edit/${postId}`,{
                method: "POST",
                headers: {
                "X-CSRFToken": csrfToken
                },
                body: new URLSearchParams({
                    post: textarea.value
                })
            })
            .then(response => {
                if (!response.ok) {
                throw new Error("Could not update post");
                }
                return response.json();
            })
            .then(data => {
                if (data.post) {
                    postContent.textContent = data.post;
                    textarea.replaceWith(postContent);
                    save.remove();
                    cancel.remove();
                }
                else {
                    alert("Post could not be updated.");
                    }
            })
            .catch(error => {
            console.error("Edit error:", error);
            alert("Something went wrong while saving.");
            });
        });
    });
});
