from . import messages
from . import mongotools

from telebot.types import Message

class BotAssistant:
    """
    FSM for bot
    """

    def __init__(self, state):
        """
        State:
            0 - waiting for /register
            1 - waiting for name
            2 - waiting for surname
            3 - registered
            4 - wanna delete
        """
        self.state = state
    
    def action(self, db, message: Message, _type='text'):
        """
        Type can be either text or command
        
        Returns message, that the bot have to send to the user
        """

        content = message.text
        if self.state == 0:
            if _type == 'command':
                if content == '/register':
                    self.state = 1
                    return messages.SEND_NAME
                elif content == '/help':
                    return messages.HELP_MESSAGE    


            return messages.SEE_HELP
            
        elif self.state == 1:
            if _type == 'text':
                mongotools.update_user(db, message.from_user.id, name=content)
                self.state = 2
                return messages.SEND_SURNAME
            return messages.SEND_NAME
                
        elif self.state == 2:
            if _type == 'text':
                mongotools.update_user(db, message.from_user.id, surname=content)
                self.state = 3
                return messages.REGISTER_FINISH
            return messages.SEND_SURNAME

        elif self.state == 3:
            if _type == 'command':
                if content == '/remove':
                    self.state = 4
                    return messages.ARE_YOU_SURE
                if content == '/help':
                    return messages.HELP_MESSAGE
                if content == '/register':
                    return messages.REGISTER_FINISH
            return messages.SEE_HELP

        elif self.state == 4:
            if _type == 'text':
                if content in ['Yes', 'yes']:
                    self.state = 0
                    return messages.START_BOT
                if content in ['No', 'no']:
                    self.state = 3
                    return messages.USER_CHANGED_HIS_MIND
            return messages.ARE_YOU_SURE


    def get_state(self):
        return self.state