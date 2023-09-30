import random
import logging
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from slack_sdk import WebClient
from django.template import loader

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from slack_sdk.errors import SlackApiError

from justsayhi.models import Team, AutoMessage
from justsayhi.tasks import post_message

logger = logging.getLogger()


@api_view(['POST'])
@permission_classes([AllowAny])
def slack_webhook(request):
    payload = request.data

    logger.debug(payload)
    type = payload['type']

    if type == 'url_verification':
        return Response({
            "challenge": payload['challenge']
        })
    elif type == 'event_callback':
        event_type = payload['event']['type']
        if event_type == 'team_join':
            user = payload['event']['user']
            team_id = user['team_id']
            user_id = user['id']
            real_name = user['real_name']
            logger.debug(f'User {real_name} just joined to team {team_id}')
            team = Team.objects.filter(team_id=team_id).first()
            if not team:
                logging.debug(f'Team {team_id} not found!')
                return Response()
            all_messages_list = team.auto_messages.filter(team__team_id=team_id).values_list('id', flat=True)
            logger.debug(f'Found {len(all_messages_list)} messages')
            if len(all_messages_list):
                random_id = random.choice(all_messages_list)
                message = team.auto_messages.filter(pk=random_id).select_related('team').first()
                message_text = message.text
            else:
                logger.debug(f'No message found, using default message')
                message_text = 'Hi @username, welcome to our Slack :wave:'

            post_message.apply_async([user_id, team.authed_user_access_token, message_text, real_name], countdown=15)

    return Response()


@api_view(['GET'])
@permission_classes([AllowAny])
def slack_oauth(request):
    payload = request.data

    logger.debug(payload)

    code_param = request.GET['code']

    # An empty string is a valid token for this request
    client = WebClient()

    # Request the auth tokens from Slack
    try:
        response = client.oauth_v2_access(
            client_id=settings.SLACK_CLIENT_ID,
            client_secret=settings.SLACK_CLIENT_SECRET,
            code=code_param
        )
    except SlackApiError as e:
        return redirect(reverse('error-view'))

    if response.status_code == 200:
        with transaction.atomic():
            team_data = response.data['team']
            logger.debug(f"Authorizing team: {team_data['name']} / {team_data['id']}")

            team, _ = Team.objects.get_or_create(team_id=team_data['id'])
            team.team_id = team_data['id']
            team.name = team_data['name']
            team.token = response.data['access_token']
            team.authed_user_id = response.data['authed_user']['id']
            team.authed_user_access_token = response.data['authed_user']['access_token']
            team.save()

            return redirect(reverse('success-view'))

    return redirect(reverse('error-view'))


@api_view(['POST'])
@permission_classes([AllowAny])
def slack_receive_slash_command(request):
    payload = request.data

    logger.debug(payload)
    team_id = payload['team_id']
    command = payload['command']
    text = payload['text']

    team = Team.objects.filter(team_id=team_id).first()
    if not team:
        return Response({'text': 'Invalid team!'})

    response_text = 'Invalid command'
    if command == '/add':
        AutoMessage.objects.create(team=team, text=text)
        response_text = 'New text added. Use /list to list all available messages.'
    elif command == '/list':
        all_messages = team.auto_messages.values_list('id', 'text')
        response_text = '\n'.join(map(lambda x: f'{x[0]}: {x[1]}', all_messages))
    elif command == '/del':
        deleted = team.auto_messages.filter(pk=int(text)).delete()
        response_text = 'Message deleted' if deleted else 'No such message exists'

    response = {
        'text': response_text
    }
    return Response(data=response)


def index_view(request):
    template = loader.get_template('justsayhi/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def error_view(request):
    template = loader.get_template('justsayhi/error.html')
    context = {}
    return HttpResponse(template.render(context, request))


def success_view(request):
    template = loader.get_template('justsayhi/success.html')
    context = {}
    return HttpResponse(template.render(context, request))