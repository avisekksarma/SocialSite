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