const likes = document.querySelectorAll(".like-button");
        likes.forEach( like => {
            like.addEventListener('click', function(){
                const icon = this.querySelector("i");
                const postId = this.dataset.postId;
                const csrfToken = document.querySelector(
                    '[name=csrfmiddlewaretoken]'
                ).value;
                fetch(`/likes/${postId}`, {
                    method : "POST",
                    headers: {
                            "X-CSRFToken": csrfToken
                                }
                })
                .then(response => response.json())
                .then(data => {

                if (data.liked) {
                    // Change heart to filled
                    icon.className ="bi bi-heart-fill";
                    like.classList.add("liked");
                }
                else {
                    // Change heart to outline
                    icon.className = "bi bi-heart";
                    like.classList.remove("liked")
                }

                // Update like count
                const count = document.querySelector(
                    `.like-count[data-post-id="${postId}"]`
                );

                count.textContent = data.count;

            });
        });
    });
