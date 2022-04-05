var students;

document.addEventListener("DOMContentLoaded", function() {
    let input = document.querySelector("#search"); 
    let total = document.querySelector("#total")
    input.addEventListener('keyup', async function() {
        if (document.title.toLowerCase().includes("student"))
        {
            total.innerText = 0;
            let In = input.value.toLowerCase();
            let table = document.getElementById("tstudent");
            let tr = table.getElementsByTagName("tr");
            for (let i = 1; i < tr.length; i++)
            {
                let get = tr[i].getElementsByTagName("td")
                let name = get[0].innerText.toLowerCase()
                let gender = get[1].innerText.toLowerCase()
                let guardian = get[3].innerText.toLowerCase()
                let country = get[4].innerText.toLowerCase()
                let course = get[6].innerText.toLowerCase()
                let teacher = get[8].innerText.toLowerCase()
                if (name.includes(In) || gender.includes(In) || guardian.includes(In) || country.includes(In) || course.includes(In) || teacher.includes(In))
                {
                    tr[i].style.display = "";
                }
                else {
                    tr[i].style.display = "none";
                }
                var rowCount = $('#tstudent >tbody >tr:visible').length; // using jquery
                total.innerText = 'search results: ' + rowCount
            }
        }
        else if (document.title.toLowerCase().includes("teacher"))
        {
            total.innerText = 0;
            let In = input.value.toLowerCase();
            let table = document.getElementById("tteacher");
            let tr = table.getElementsByTagName("tr");
            for (let i = 1; i < tr.length; i++)
            {
                let get = tr[i].getElementsByTagName("td")
                let name = get[0].innerText.toLowerCase()
                let gender = get[1].innerText.toLowerCase()
                let salary = get[5].innerText.toLowerCase()
                if (name.includes(In) || gender.includes(In) || salary.includes(In))
                {
                    tr[i].style.display = "";
                }
                else {
                    tr[i].style.display = "none";
                }
                var rowCount = $('#tteacher >tbody >tr:visible').length; // using jquery
                total.innerText = 'search results: ' + rowCount
            }
        }   
    })
})

