import os

from dotenv import load_dotenv


def create_config_env(env_name):
    try:
        if env_name in ['dev', 'prod']:
            env_file = f'.env_{env_name}'
            suffix = env_name.upper()
            load_dotenv(env_file)
            bot_token = os.getenv(f'BOT_TOKEN_{suffix}')
            server_url = os.getenv(f'SERVER_URL_{suffix}')
        else:
            raise ValueError(f"Unknown environment: {env_name}")

        if not bot_token or not server_url:
            raise ValueError(f"Missing environment variables for {env_name}")

        with open('.env', 'w') as f:
            f.write(f"BOT_TOKEN={bot_token}\n")
            f.write(f"SERVER_URL={server_url}\n")

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}. Ensure that the .env_dev or .env_prod file exists.")
    except ValueError as val_error:
        print(f"Error: {val_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
