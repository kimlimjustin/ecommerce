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
            this.title = "Like";
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
            this.title = "Unlike";
        }
    })
    document.querySelector("#cart-icon").addEventListener("click", function(){
        const csrf = Cookies.get('csrftoken');
        const id = document.querySelector("#item-id").innerText;
        if(new URL(this.src).pathname === "/static/Icon/cart.jpg"){
            fetch('/cart/add', {
                method: "POST",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    id: id
                })
            })
            this.src = "/static/Icon/remove_cart.png";
            this.title = "Remove from cart";
        }else{
            this.src = "/static/Icon/cart.jpg";
            this.title = "Add to cart"
            fetch('/cart/remove', {
                method: "POST",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    id: id
                })
            })
        }
    })
})