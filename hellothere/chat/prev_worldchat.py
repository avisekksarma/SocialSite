from chat.models import AllWorldChatMessages,AllPrivateChatMessages

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


def get_all_previous_private_msgs(room_name):
    all_msgs = []
    for msg in AllPrivateChatMessages.objects.filter(room_name=room_name):
        all_msgs.append(
        {
                'message':msg.message,
                'sent_by':msg.sent_by.username,
                'msg_sent_time': msg.serialize_datetime()
            })
    return all_msgs