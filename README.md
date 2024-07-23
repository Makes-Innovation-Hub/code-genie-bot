# code-genie-bot
telegram bot for code genie

=======
# Environment Variables (Explanation)

- `BOT_TOKEN`: The telegram bot token for full control. Example: **123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi_jklmnopqrstuvwx
**
- `SERVER_URL`: The backend server url for making requests. Example: **http://localhost:8000/"**

# Environment Variables (Usage)

To load environment variables from a `.env` file in Python, you can use the `python-dotenv` package. Here’s how you can do it:

1. Save an `.env` file in your project. **WARNING**: make sure it is found in `.gitignore`. Save the above [Variables](#environment-variables-explanation) in the `.env` file using the exact provided names.

2. **Install the `python-dotenv` package** (if you haven’t already):
   ```sh
   pip install python-dotenv
   
3. A brief example on how to load a specific environment variable:
    ```python
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    bot_token = os.getenv('BOT_TOKEN')
    ```


# Running the Bot on AWS with PM2
**1.** Connect to AWS EC2 Instance:
```sh
	ssh -i "path/to/your-key-pair.pem" ubuntu@ec2-instance_ip
```  
**2.** Change the directory to the repo:  
```sh 
	cd code-genie-bot
```  
**3.** Pull the changes on dev branch:  
```sh 
	git pull origin dev
```  
**4.** Install the requirements (Its recommended to use virtual env):  
```sh
	pip install -r requirements.txt
```  
**5.** Run the bot using pm2 tool (make sure that it's installed globally on your EC2 instance):  
```sh 
	pm2 restart code_genie_bot
```  
**Note**: To stop the bot run   ```pm2 stop code_genie_bot```  

## the structure of the bot 
├── code-genie-bot \
│  # Package initia lization \
│  # Main bot entry point \
│ ├── handlers \
│ │  # Handlers package initialization \
│ │  # Handle bot commands \
│ ├── utils \
│ │  # Utils package initialization \
│ │  # Helper functions \
│ │  # Input validation  \
├── tests \
│  # Tests package initialization \
│  # Handlers tests \
│  # Utils tests \
├ # Environment variables \
├ # Git ignore file \
├ # requermint list \
├ # readme 
