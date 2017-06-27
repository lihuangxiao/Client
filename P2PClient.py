import sys

##
# Implements the Client Class
# Client has three fields.
# running: status of Client
# id: Client's id
# others: connection cache, a dict (id, status) storing all other Clients connecting with self
##
class Client:

    CONTROL_ACTIONS = ['SRT', 'DWN']
    CONNECT_ACTIONS = ['SYN', 'ACK', 'CON', 'TRD']
    MESSAGE_ACTIONS = ['MSG']

    ##
    # Constructor
    ##
    def __init__(self, client_id):
        self.running = True
        self.client_id = client_id
        self.others = dict()

    ##
    # Method used to process the raw message from any other p2p clients.
    # The processing mainly does two things:
    # 1. Split the raw messages into a list by commas, up to three elements.
    # 2. Strip each element's leading or trailing white spaces
    ##
    def processInput(self, message):
        if message.startswith('(') and message.endswith(')'):
            message = message[1:-1]
            arr_message = message.split(',', 2)
            for i in range(0, len(arr_message)):
                arr_message[i] = arr_message[i].strip()
            return arr_message
        return []

    ##
    # Method used to process message that are possibly related to control actions.
    ##
    def processControl(self, message):
        if len(message) != 1:
            print('(DSC)')
        else:
            if message[0] == 'SRT' and self.running == False:
                self.running = True
            elif message[0] == 'DWN' and self.running == True:
                for connction in self.others:
                    print ('(TRD, {})'.format(self.client_id))
                self.others = {}
                self.running = False
            else:
                print('(DSC)')

    ##
    # Method used to process message that are possibly related to connect actions.
    # only gets invoked when running
    ##
    def processConnect(self, message):
        if len(message) != 2:
            print('(DSC)')
        else:
            action = message[0]
            other_id = message[1]
            if action == 'SYN' and other_id not in self.others:
                print('(ACK, {})'.format(self.client_id))
                self.others[other_id] = 'ACK_sent'
            elif action == 'ACK' and (other_id not in self.others or self.others[other_id] != 'connected'):
                print('(CON, {})'.format(self.client_id))
                self.others[other_id] = 'connected'
            elif action == 'CON' and other_id in self.others and self.others[other_id] == 'ACK_sent':
                self.others[other_id] = 'connected'
            elif action == 'TRD' and other_id in self.others and self.others[other_id] == 'connected':
                del self.others[other_id]
            else:
                print('(DSC)')

    ##
    # Method used to process message that are possibly related to message actions.
    # only gets invoked when running
    ##
    def processMessage(self, message):
        if len(message) != 3:
            print('(DSC)')
        else:
            action = message[0]
            other_id = message[1]
            str_message = message[2]
            if action == 'MSG' and other_id in self.others and self.others[other_id] == 'connected':
                print('(MSG, {}, {})'.format(self.client_id, str_message))
            else:
                print('(DSC)')


    ##
    # Method waits for raw message from standard input,
    # it also prints to standard output for any message it sends out
    ##
    def listen(self):
        while True:
            message = input('waiting for incoming message...\n')
            processed_message = self.processInput(message)
            if len(processed_message) == 0:
                print('(DSC)')
                continue
            action = processed_message[0]
            if action in self.CONTROL_ACTIONS:
                self.processControl(processed_message)
            elif action in self.CONNECT_ACTIONS and self.running:
                self.processConnect(processed_message)
            elif action in self.MESSAGE_ACTIONS and self.running:
                self.processMessage(processed_message)
            else:
                print('(DSC)')
           


##
# Main function
# Main reads the first command line argument and set it as client_id,
# otherwise uses Tony as our client_id 
##
if __name__ == '__main__':
    client_id = 'Tony'
    if len(sys.argv) > 1:
        client_id = sys.argv[1]
        client_id = client_id.replace(',', '')
    myClient = Client(client_id)
    myClient.listen()





