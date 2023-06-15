import discord
from discord.ext import commands
import openai
import pickle
import os

def run_discord_bot():
    openai.api_key = "OPEN AI API KEY HERE"
    TOKEN = 'DISCORD BOT TOKEN HERE'
    intents = discord.Intents.default()
    intents.messages = True
    bot = discord.Client(intents = intents)
    
    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        for guild in bot.guilds:
            print(f"guild name: {guild}, id: {guild.id}")
 
    @bot.event
    async def on_message(message):
        username = message.author
        #channel = message.channel
        channel_id = bot.get_channel("CHANNEL TO HOST THE QUESTION'S ID HERE")
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == bot.user:
            return
        if message.channel.id == channel_id.id and message.content.startswith('!'):
            data = message.content[1:]
            await process_message(channel_id, username, data, message.id)
        else:
            await message.delete()
    async def process_message(channel, user, message, msgid):
        user_exist = userInDatabase(user)
        if user_exist: #now we check for a channel
            uInfo = getUserInfo(user)
            uNew = uInfo['new']
            if uNew ==0:
                await createUserEnv(user,channel)
                uInfoUpdated = getUserInfo(user)
                await sendResponse(channel, uInfoUpdated, message, msgid) 
            else:
                await sendResponse(channel, uInfo, message, msgid) #send both the question and response in each respective log, and delete the message
   
    #DATABASE HELPER FUNCTIONS
    def userInDatabase(user):
        if os.path.exists('bot_data.pkl'):
            with open('bot_data.pkl', 'rb') as fp:
                userData = pickle.load(fp)
            if not userData: #if file exists but is empty
                return createDatabase(user)
            else:#find specific user
                for x in userData:
                    if x['name'] == user.name:
                        return True
                    else:
                        return updateDatabase(user)
        else: #file does not exist, create it
            return createDatabase(user)
    def updateDatabase(user):
        currentUserData = {'name': user.name, 'assigned_channel_id': 0, 'new': 0}
        if not os.path.exists('bot_data.pkl'):
            createDatabase(user)
        else:
            with open('bot_data.pkl', 'rb') as file:
                userData = pickle.load(file)
            userData.append(currentUserData) 
            with open('bot_data.pkl', 'wb') as file:
                pickle.dump(userData, file)
        print("Successfully Updated Database")
        return True
    def createDatabase(user):
        currentUserData = {'name': user.name, 'assigned_channel_id': 0, 'new': 0}
        bot_data = []
        bot_data.append(currentUserData)
        with open('bot_data.pkl', 'wb') as file:
            pickle.dump(bot_data, file)
        print("Created a new file 'bot_data.pkl' with inital data stored.")
        return True
    def getUserInfo(user):
        with open('bot_data.pkl', 'rb') as file:
            userData = pickle.load(file)
        for x in userData:
            if x['name'] == user.name:
                return x
    #USER/OPENAI CHAT HELPER FUNCTIONS
    async def createUserEnv(user, channel):
        guild = channel.guild
        category = discord.utils.get(guild.categories, name = "chats")
        if category is None:
            category = await guild.create_category("chats")
        chatName = f"{user.name}'s Log"
        createdChannel = await guild.create_text_channel(chatName, category=category)
        await createdChannel.set_permissions(user, read_messages=True, send_messages=False)
        await createdChannel.set_permissions(channel.guild.me, read_messages=True, send_messages=True)
        await createdChannel.set_permissions(guild.default_role, read_messages=False)
        with open('bot_data.pkl','rb') as file:
            userData = pickle.load(file)
        for x in userData:
            if x['name'] == user.name:
                x['assigned_channel_id'] = createdChannel.id
                x['new'] = 1
                print(f"updated user info: {x}")
                break
        with open('bot_data.pkl', 'wb') as file:
            pickle.dump(userData, file)
        print(f"{user.name}'s enviroment succesfully created!")
        await createdChannel.send(f"__This is the start of [{user.name}]'s History.__")
    async def sendResponse(OGChannel, uInfo, message, OGmsg_id):
        channel = bot.get_channel(int(uInfo['assigned_channel_id']))
        data = f"[{uInfo['name'].capitalize()}'s question / comment:] {message}"
        await channel.send(data)
        OGmessage = await OGChannel.fetch_message(int(OGmsg_id))
        await OGmessage.delete()
        model = "text-davinci-003"
        response = openai.Completion.create(engine=model, prompt=message, max_tokens=1000)
        generated_text = response.choices[0].text
        await channel.send(f"**[{channel.guild.me.name}'s answer:]** ```{generated_text}```") 
        #send response in log
        usage = response['usage']['total_tokens']
        print(f"{uInfo['name']}'s message transaction completed. token used: {usage}")
    
    bot.run(TOKEN)
