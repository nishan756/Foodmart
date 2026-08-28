function performAutoSearch(){
    const searchForm = document.getElementById("searchForm");
    const searchInput = document.getElementById("searchInput");

    let timer;
    const delay = 1000;

    if (searchForm && searchInput){
        searchInput.addEventListener("input" , function(){
            clearTimeout(timer);

            timer = setTimeout(function(){
                if(searchInput.value.trim().length > 0){
                    searchForm.submit();
                }
            } , delay)
        })
    }
}

function clearSearchInput(){
    const clearBtn = document.getElementById("clearBtn");
    const searchInput = document.getElementById("searchInput");

    if (clearBtn && searchInput.value.trim().length > 0){
        searchInput.value = "";
    }
}
