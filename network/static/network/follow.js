const followers = document.querySelector("#follow");
    followers.addEventListener('click', function(){
        const pageId = this.dataset.userId;
        const csrfToken = document.querySelector(
                '[name=csrfmiddlewaretoken]'
                ).value;
        fetch(`/follow/${pageId}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken
                    }
        })
        .then(response => response.json())
        .then(data =>{
            if(data.followed){
                followers.innerHTML = 'Unfollow'
                followers.classList.add("following");
            }
            else{
                followers.innerHTML = 'Follow'
                followers.classList.remove("following");

            }
            document.querySelector("#followers-count").textContent = data.followers_count;
        });
    });
