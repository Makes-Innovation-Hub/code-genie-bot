import pytest
import requests
# from bot import genie_bot
from unittest.mock import AsyncMock, patch
from telegram import Update, Message
from telegram.ext import ContextTypes
from genie_bot import start, help_command, get_public_ip

@pytest.mark.asyncio
async def test_start():
    update = AsyncMock(Update)
    context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    message = AsyncMock(Message)
    update.message = message

    await start(update, context)

    update.message.reply_text.assert_called_once_with('Hello! I am your bot. How can I help you?')

@pytest.mark.asyncio
async def test_help_command():
    update = AsyncMock(Update)
    context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    message = AsyncMock(Message)
    update.message = message

    await help_command(update, context)

    help_text = (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/ip -  get public ip"
    )
    update.message.reply_text.assert_called_once_with(help_text)

@pytest.mark.asyncio
async def test_get_public_ip_success():
    # Setup Mocks
    update = AsyncMock(Update)
    context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    message = AsyncMock(Message)
    update.message = message
    
    # Mock the requests.get to simulate a successful API response
    with patch('genie_bot.requests.get') as mocked_get:
        mocked_get.return_value.json.return_value = {'ip': '123.123.123.123'}
        mocked_get.return_value.status_code = 200

        # Run the function
        result = await get_public_ip(update, context)

        # Assertions
        update.message.reply_text.assert_called_once_with('The public IP address of the bot is: 123.123.123.123')
        assert result is True

@pytest.mark.asyncio
async def test_get_public_ip_failure():
    # Setup Mocks
    update = AsyncMock(Update)
    context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    message = AsyncMock(Message)
    update.message = message

    # Mock the requests.get to simulate a failed API response
    with patch('genie_bot.requests.get') as mocked_get:
        mocked_get.side_effect = requests.RequestException('Failed to connect')

        # Run the function
        result = await get_public_ip(update, context)

        # Assertions
        expected_error_message = 'Failed to get public IP address: Failed to connect'
        update.message.reply_text.assert_called_once_with(expected_error_message)
        assert result is False