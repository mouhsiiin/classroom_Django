from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import conversation, message
from django.shortcuts import redirect
from main.models import User
from django.http import JsonResponse
import json

@login_required
def chat(request):
    conversations = conversation.objects.filter(user1=request.user) | conversation.objects.filter(user2=request.user)

    
    context = {
        'conversations': conversations
    }
    return render(request, 'socialmedia/chat.html', context)


@login_required
def create_conversation(request):
    if request.method == 'POST':
        print(request.body)
        #extracting the recipient username from the ajax body
        user2 = json.loads(request.body).get('recipient')
        if user2:
            try:
                user2 = User.objects.get(username=user2)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
                
            new_conversation = conversation(user1=request.user, user2=user2)
            new_conversation.save()
            return JsonResponse({'success': 'Conversation created successfully'})
        else:
            return JsonResponse({'error': 'Recipient not provided'}, status=400)
    else:
        return redirect('socialmedia:chat')
    

@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        conversation_id = data.get('conversation_id')
        text = data.get('message')
        if conversation_id and text:
            try:
                conversation_obj = conversation.objects.get(id=conversation_id)
            except conversation.DoesNotExist:
                return JsonResponse({'error': 'Conversation not found'}, status=404)
            
            new_message = message(conversation=conversation_obj, sender=request.user, text=text)
            new_message.save()
            return JsonResponse({'success': 'Message sent successfully'})
        else:
            return JsonResponse({'error': 'Conversation ID or text not provided'}, status=400)
    else:
        return redirect('socialmedia:chat')
    

@login_required
def get_messages(request):
    if request.method == 'GET':

        conversation_id = request.headers.get('conversation_id')
        print(request.headers)
        print(conversation_id)
        if conversation_id:
            try:
                conversation_obj = conversation.objects.get(id=conversation_id)
            except conversation.DoesNotExist:
                return JsonResponse({'error': 'Conversation not found'}, status=404)
            
            messages = conversation_obj.messages
            messages_data = []
            for message in messages:
                messages_data.append({
                    'id': message.id,
                    'text': message.text,
                    'sender': message.sender.username,
                    'created_on': message.created_on
                })
            return JsonResponse({'messages': messages_data}, status=200)
        else:
            return JsonResponse({'error': 'Conversation ID not provided'}, status=400)
    else:
        return redirect('socialmedia:chat')