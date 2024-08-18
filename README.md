
# code-genie-bot  
telegram bot for code genie  
  
=======  
# Environment Variables (Explanation)  
 In `.env_dev` file save the following vars:
- `BOT_TOKEN_DEV`: The telegram bot token for full control. Example: **123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi_jklmnopqrstuvwx  
**  
- `SERVER_URL_DEV`: The backend server url for making requests. Example: **http://localhost:8000/"**    

 In `.env_prod` file save the following vars:
- `BOT_TOKEN_PROD`: The telegram bot token for full control. Example: **123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi_jklmnopqrstuvwx  
**  
- `SERVER_URL_PROD`: The backend server url for making requests. Example: **http://localhost:8000/"**  
# Environment Variables (Usage)   
To load environment variables from a `.env` file in Python, you can use the `python-dotenv` package. Here’s how you can do it:  
  
1. Save an `.env` file in your project. **WARNING**: make sure it is found in `.gitignore`. Save the above [Variables](#environment-variables-explanation) in the `.env` file using the exact provided names.   
2. **Install the `python-dotenv` package** (if you haven’t already):  
   ```sh  
   pip install python-dotenv  
	  ```
 3. A brief example on how to load a specific environment variable:  
	   ```python  
	  import os  
	 from dotenv import load_dotenv     
	 load_dotenv('.env')  
	 bot_token = os.getenv('BOT_TOKEN')  
	 ```
Run command for genie_bot :   
1. To run in dev env there are two options:

- ```shell
  python genie_bot.py dev # Explicit run
  ```

- ```shell
  python genie_bot.py # Implicit run
  ```

2. To run in production env:

	```shell 
	python genie_bot.py prod
	``` 

# Testing

In order to run tests for the project you have to run the following commands:

```shell
cd path/to/your/project # Replace with the path to your project (root)
pytest
```

# Project Structure

├── code-genie-bot \  
│  # Package initialization \  
│  # Main bot entry point \  
│ ├── config\  
│ │  # managing and loading configuration settings   
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
