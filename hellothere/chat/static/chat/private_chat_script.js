const host = '127.0.0.1:8000' // this should be the actual host address with port number too..


let smallId = document.getElementById('small-id').innerHTML
let bigId = document.getElementById('big-id').innerHTML
// created a websocket connection which will  handsake with the server if server responds with the self.accept()
const socket = new WebSocket(`ws://${window.location.host}/ws/chat/privatechat/${smallId}/${bigId}/`)

socket.addEventListener('open', function (e) {
  document.getElementsByClassName('flash-msg')[0].innerHTML =
    'You are successfully connected to the server'
})

socket.addEventListener('message',function(e){
    let data = JSON.parse(e.data)
    if (data.message) {
        let p = ''
        if (data.sent_by === document.getElementById('username').innerText) {
          p = `<p class="msgs"><strong>You:</strong><span>${data.message}</span>(${data.msg_sent_time.date} ,  ${data.msg_sent_time.time})</p>`
        } else {
          p = `<p class="msgs"><strong>${data.sent_by}:</strong><span>${data.message}</span>(${data.msg_sent_time.date} ,  ${data.msg_sent_time.time})</p>`
        }
    
        document.getElementById('message-list').innerHTML += p
      }else if (data.online_users) {
        console.log(data.online_users)
        delete_user_who_is_not_online_anymore(data.online_users)
        for (const online_user of data.online_users) {
          console.log(online_user.username)
          let written_online_array = get_all_written_online_friends()
          if (!written_online_array.includes(online_user.username)) {
            let p = `<p id="${online_user.username}">${online_user.username}</p>`
            document.getElementById('online-list').innerHTML += p
          }
        }
      }
})

document.getElementById('submit').onclick = function (event) {
    let message_box = document.getElementById('input-message-box')
    let sent_by = document.getElementById('username').innerText
    socket.send(
      JSON.stringify({
        message: message_box.value,
        sent_by: sent_by
      })
    )
    message_box.value = ''
  }

  function get_all_written_online_friends () {
    let written_online_node = document.querySelectorAll('#online-list p')
  
    let written_online_array = []
    for (const a_user of written_online_node) {
      written_online_array.push(a_user.innerText)
    }
    console.log(written_online_array)
    return written_online_array
  }
  
  function delete_user_who_is_not_online_anymore (online_user_list) {
    written_online_array = get_all_written_online_friends()
  
    for (written_online_user of written_online_array) {
      if (!online_user_list.includes(written_online_user)) {
        let element = document.getElementById(written_online_user)
        element.parentNode.removeChild(element)
      }
    }
  }
  