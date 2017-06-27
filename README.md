to invoke the program, execute Client.sh with optional argument client_id:
./Client.sh client_id
not that all commas in client_id will be removed because we assume client_id cannot contain commas

The program implements a P2P messaging network
#### The specification of the network defines that:
    * a client can receive messages regarding setting up a connection
        - (SYN, client_id) meaning a client named client_id wants to establish a connection
        - (ACK, client_id) meaning a client named client_id agrees to establish a connection with you
        - (CON, client_id) meaning a client named client_id confirms a connection has been established with you
        - (TRD, client_id) meaning a client named client_id wants to teardown its connection with you
    * a client can also receive plain messages
        - (MSG, client_id, plain_message) meaning a client named client_id send you a message plain_message

#### client also supports following control messages:
    * a client can be shutdown, if it is running
        - (DWN) meaning the client will stop working, and all connections are to be teared down with appropriate messages
    * a client can be started, if it is shutdown
        - (SRT) meaning the client will start working in a fresh state

#### Client behaviors:
    * client is reactive
        - upon SYN, return ACK with its own client_id if there is no connection in place
        - upon ACK, always return CON with its own client_id and confirms connection
        - upon CON, confirm connection if we have received SYN and sent out ACK
        - upon MSG, echo back with its own client_id if connection is in place
    * client discard all messages not actionable
        - just send (DSC)
    * client remains listening for messages all the time, even when it is shutdown

#### Format and Test cases
    * the client waits for message from standard input
    * the client prints to standard output for any message it sends out




Assumptions:
A lot of assumptions have been made, some of them being:
1, When Client receives ACK, we assume a SYN has been sent. So Client sends CON and confirms connection
2, When Client receives ACK while expecting CON, Client will ignore previous session, and confirm connection upon receiving ACK
3, We assume Client id cannot contain commas, plain messages can contain commas
4, We assume we can discard empty plain messages
5, We assume we want to strictly follow TCP 3-way handshake procedure, unexpected connection packets will be discarded.
