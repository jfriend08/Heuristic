# No-Tipping-Game
## As a player in the game
- You will have to download the framework for your player here.

- It contains a file NoTippingPlayer.java which you must extend. A sample Contestant.java file is provided which allows you to play by command line instruction is provided.

- To run the player, run it on the machine to which the application run by the architect will connect.

- Something like "java Contestant 8080" would run your program on port 8080.

- If the application (client) disconnects the connection to your player (server), the application exits.

## To run the code locally
- It contains a file PlayerInfo.txt which you must modify to use the ports of your players.

- Now each player should be having an assigned port, so that when you select the player, the game tries to connect to him or her.

- ReMake the jar file by "jar cvfm notippingapp.jar manifest.txt *.class *.java PlayerInfo.txt".

- When running the program, specify hostname=localhost to connect to the ports on your local machine. This is useful for testing. specify any other hostname to connect to machines on which the competition is being held.

- So, to run the application, something like "java -jar notippingapp.jar hostname=localhost" should be enough.

- First select the second player, then the first player and then click on Connect. Red always goes first, so select the blue player first.

## Help
AIContestant will be a good place to look at. For calculating the torque, take a look at the ```verifyGameNotOver``` in 
AIContestant.java

Please compile your code with ```NoTippingPlayer.java``` and put it in your team folder in **/tmp/noTippingGame**


