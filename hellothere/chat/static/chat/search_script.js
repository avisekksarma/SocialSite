let searchBtn = document.getElementById('search-btn')
let domain_name='http://127.0.0.1:8000/'
searchBtn.addEventListener('click',e=>{
    e.preventDefault();
    let userSearch = {
        'search':document.getElementById('search-box').value
    }
    //TODO: I may need to change the mode to cors and also change other parts of fetch api to work on production mode.
    fetch(domain_name + 'chat/search/',{
        method:'POST',
        mode: 'same-origin',
        credentials: 'include',
        headers:{
            'Content-Type':'application/json',
            'Accept':'*/*'
        },
        body:JSON.stringify(userSearch)
    })
    .then(res=>res.json())
    .then(result=>{
        if (!result.no_users){
            showSearchedUsers(result.users)
        }else{
            // case when empty submitted by the user.
            showSearchedUsers([],result.no_users)
        }
        
    })
    .catch(e=>console.log(e))
})


function showSearchedUsers(usersArray,message){
    all_searched_users_div = document.getElementById('all_searched_users')
    all_searched_users_div.innerHTML = ''
    if (message){
        all_searched_users_div.innerHTML = message
        return
    }
    for (const user of usersArray){
        all_searched_users_div.innerHTML += `<p class="p-3 mb-2 bg-info text-white"><a class="searched-users" href="" data-user="${user}">${user}</a></p>`
    }
    if (usersArray.length === 0){
        all_searched_users_div.innerHTML = '<p class="p-3 mb-2 bg-danger">No user found matching your searched username.</p>'
    }

    createEventHandlersForLink()
}

function createEventHandlersForLink(){
    // returns the link of all the searched users.
    all_searched_users_link = document.querySelectorAll('a.searched-users')
    all_searched_users_link.forEach(link_element => {
        link_element.addEventListener('click',e=>{
            e.preventDefault();
            fetch('http://127.0.0.1:8000/chat/makeurlforprivatechat/',{
            method:'POST',
            mode: 'same-origin',
            credentials:'include',
            headers:{
                'Content-Type':'application/json',
                'Accept':'*/*'
            },
            body:JSON.stringify({
                'requested_user':link_element.dataset.user,
                'my_username':document.getElementById('userinfo').innerText
            })
            })
            .then(res=>res.json())
            .then(result=>{

                window.location.href = domain_name+'chat/privatechat/'+result.url+'/'
            })
            .catch(e=>console.log(e))
        })
    })

}

// it sends the username of the requested user that the current user wants to speak to if there is any getrequest 
// to that requested user and current user's combined url.
function sendCurrentOpenedPrivateChat(){
    fetch(domain_name+'chat/sendprivatechatuser/',{
        method:'POST',
        mode: 'same-origin',
        credentials: 'include',
        headers:{
            'Content-Type':'application/json',
            'Accept':'*/*'
        },
        body:JSON.stringify({})
    })
    .then(res=>res.json())
    .then(result=>{
        if (!result.no_users){
            showSearchedUsers(result.users)
        }else{
            // case when empty submitted by the user.
            showSearchedUsers([],result.no_users)
        }
        
    })
    .catch(e=>console.log(e))
}