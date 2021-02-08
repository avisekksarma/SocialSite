from chat.models import AllWorldChatMessages

def get_all_previous_worldchat_msgs():
    all_msgs = []
    for msg in AllWorldChatMessages.objects.all():
        all_msgs.append(
        {
                'message':msg.message,
                'sent_by':msg.sent_by.username,
                'msg_sent_time': msg.serialize_datetime()
            })
    return all_msgs