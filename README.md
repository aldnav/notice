# notice
A simple Push Notification server made from Tornado.

##Proof of concept
###Registration
```txt
		----------------------------
		| Push Notification Server |
		----------------------------
			[2]	|		^	[1]
		Reg ID	|		|	Project ID
				|		|
				,		|
--------		----------
|Server|<-[3]---| Client |
--------		----------		
		Reg ID		
```
1. On load, send Project ID to Push Notification Server.
2. PN response with a Reg ID. This serves as address unique to each client (multiple browsers by a user).
3. Client sends Reg ID to the application server and keep this registration ID paired with the client.

###Message sending
```txt
	  Reg ID, Context
--------		  ----------------------------
|Server|---[1]--->| Push Notification Server |
--------		  ----------------------------
							  |
							 [2]	Context
							  |
							  ,
						  ----------
						  | Client |
						  ----------
```
1. Server sends Context with Reg ID to PNS.
2. Since PNS holds the web sockets, it sends the Context to the web sockets with the corresponding Reg ID.
Client recieves context. (Optional: Client can request to Server what the Context is and retrieves the message).

###Unregistration
On progress.