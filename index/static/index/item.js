document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#delete_form_submit").addEventListener("click", () => {
        if(window.confirm("Are you sure?")){
            document.querySelector("#delete_form").submit()
        }
    })
    document.querySelector("#love-icon").addEventListener("click", function(){
        const csrf = Cookies.get('csrftoken');
        const id = document.querySelector("#item-id").innerText;
        const totalLikeElement = document.querySelector("#total_like");
        if(new URL(this.src).pathname === "/static/Icon/loved.png"){
            this.src = "/static/Icon/love.png";
            fetch('/unlike', {
                method: "POST",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    id: id
                })
            })
            totalLikeElement.innerText = parseInt(totalLikeElement.innerText) - 1;
        }else {
            fetch('/like', {
                method: "POST",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    id: id
                })
            })
            totalLikeElement.innerText = parseInt(totalLikeElement.innerText) + 1;
            this.src = "/static/Icon/loved.png";
        }
    })
})