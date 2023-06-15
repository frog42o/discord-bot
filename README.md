#PREREQS:
-Must have Python installed and running on device to run.
-Includes libraries discord.py, openai, pickle, and os (may have to pip install openai)
-Discord Bot must have Administration access and intents. 

#USAGE
-Replace the OpenAI API Key token and Discord Bot Token respectively.
-Replace the "CHANNEL ID" to your own channel's id where you want to host the OpenAI
----------------------------------------------------------------------------------
After running the bot/program for the first time and populating it with inital data, expect:
-A category called #chats to appear if you had not created one yourself. This can be changed by modifying the function 'createUserEnv' and modifying the category names. this category is served as a space to host the OpenAI's logs with each individual users, and only the owner of the server, the bot, and the user who asked the question may see their own respective logs. 
  - EX.) owner: joe, bot: open-ai bot, petitioner: sally. If sally asks a question, only sally, joe, and open-ai-bot will see the log created for sally.
-A file called 'bot_data.pkl' will serve as your database to store user information. This information is stored in the same file locations as the rest of the files; **data is stored as a list of dictionaries**. 
  - You may opt to change the storing method to something more secure or comforatable to use, however this does require modifciation of the source code. 


Contact me 'frog42o' on Discord if you have any questions and enjoy <3 !


