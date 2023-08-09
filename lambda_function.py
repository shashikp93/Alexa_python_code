# -*- coding: utf-8 -*-

from __future__ import print_function



# This function used to give responses by alexa like "skill title","skill content", "skill session" etc.
def build_speechlet_response(title, output, reprompt_text, should_end_session, cardContent):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': '<speak>' + output + '</speak>'
        },
        'card': {
            'type': 'Standard',
            'title':  title,
            'text':  cardContent
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': '<speak>' + reprompt_text + '</speak>'
            }
        },
        'shouldEndSession': should_end_session
    }


# We can pass here the session details and the skill speech responses.
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------




##--This is the help section of this skill. when we want to know something about this skill or if we need any help related to this skill,
## we can call help intent.
def help_response(intent,session):
    speech_output = "This is the rules. I will help you later."
    card_title = "Help"
    reprompt_text = "what would you like to know?"
    session_attributes = {}
    card_title = "Help"
    should_end_session = False
    cardContent = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session, cardContent))


# This function can call when we want to cancel or stop the skill.   
def cancel_response(intent,session):
    speech_output = "Thank you for using this skill. Have a nice day."
    session_attributes = {}
    card_title = "Thank you for playing"
    reprompt_text = speech_output
    should_end_session = True
    cardContent = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session, cardContent))


# This is the Builtin home intent. we call this intent when we want to restart the skill.  
def navigateHome():
    speech_output = ""
    session_attributes = {}
    card_title = "Home"
    reprompt_text = ""
    should_end_session = False
    cardContent = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session, cardContent))


# This is the Welcome intent. Skill always starts from this intent whenever user will invoke the skill name.
def get_welcome_response(session):
    speech_output = "this is welcome"
    session_attributes = {}
    card_title = "welcome"
    reprompt_text = "what would you like to know?"
    should_end_session = False
    cardContent = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session, cardContent))


# This is the fallback intent
def fallback(intent,session):
    speech_output = "something went wrong"
    reprompt_text = "what would you like to know?"
    session_attributes = {}
    card_title = "fallback"
    should_end_session = False
    cardContent = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session, cardContent))




""" This is the repeat intent. whatever we wants alexa to repeat the context.
we will use this builtin intent to repeat the any context
"""
def repeatIntent(intent,session):
    speech_output = ""
    reprompt_text = ""
    session_attributes = {}
    card_title = ""
    should_end_session = False
    cardContent = ""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session, cardContent))

# This is the builtin intent. Setting this to true ends the session and exits the skill.
def handle_session_end_request():
    card_title = "Thank you for playing"
    speech_output = "Thank you for using this skill." 
    should_end_session = True
    cardContent = ""
    return build_response({}, build_speechlet_response(
        card_title, speech_output, "", should_end_session, cardContent ))



#== Called when the session starts
def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])




"""
Called when the user launches the skill without specifying what they want,
when request type is LaunchRequest, then this function will called in lambda handler function.
"""
def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response(session)




#== Called when the user specifies an intent or function for this skill.
def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.HelpIntent":
        return help_response(intent,session)
    elif intent_name == "AMAZON.CancelIntent":
        return cancel_response(intent,session)
    elif intent_name == "AMAZON.StopIntent":
        return cancel_response(intent,session)
    elif intent_name == "" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback(intent,session)
    elif intent_name == "AMAZON.RepeatIntent":
        return repeatIntent(intent,session)
    else:
        raise ValueError("Invalid intent")



""" 
Called when the user ends the session.
Is not called when the skill returns should_end_session=true
"""
def on_session_ended(session_ended_request, session):

    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------
"""
This is the main handler in lambda function. whenever skill starts this function will call. It will check the request type and launch the skill
"""
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")


    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
