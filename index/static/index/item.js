document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#delete_form_submit").addEventListener("click", () => {
        if(window.confirm("Are you sure?")){
            document.querySelector("#delete_form").submit()
        }
    })
})