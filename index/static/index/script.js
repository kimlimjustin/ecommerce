document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#nav-ham").addEventListener('click', function(){
        let element = document.getElementById(this.dataset.target);
        if(element.style.display === "block") element.style.display = "none";
        else element.style.display = "block";
    })
})