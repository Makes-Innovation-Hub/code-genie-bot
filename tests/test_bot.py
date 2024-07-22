import pytest
import requests
from unittest.mock import AsyncMock, patch
from telegram import Update, Message
from telegram.ext import ContextTypes
from genie_bot import *

@pytest.mark.asyncio
async def test_start_command():
    update = AsyncMock(Update)
    context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    message = AsyncMock(Message)
    update.message = message

    await start_command(update, context)

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
        "/ip -  get public ip\n"
        "/api - connect to server"
    )
    update.message.reply_text.assert_called_once_with(help_text)

@pytest.mark.asyncio
async def test_get_public_ip_command_success():
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
        result = await get_public_ip_command(update, context)

        # Assertions
        update.message.reply_text.assert_called_once_with('The public IP address of the bot is: 123.123.123.123')
        assert result is True

@pytest.mark.asyncio
async def test_get_public_ip_command_failure():
    # Setup Mocks
    update = AsyncMock(Update)
    context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    message = AsyncMock(Message)
    update.message = message

    # Mock the requests.get to simulate a failed API response
    with patch('genie_bot.requests.get') as mocked_get:
        mocked_get.side_effect = requests.RequestException('Failed to connect')

        # Run the function
        result = await get_public_ip_command(update, context)

        # Assertions
        expected_error_message = 'Failed to get public IP address: Failed to connect'
        update.message.reply_text.assert_called_once_with(expected_error_message)
        assert result is False


@pytest.mark.asyncio
async def test_api_command_success():
    # Setup Mocks
    update = AsyncMock(Update)
    context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    message = AsyncMock(Message)
    update.message = message

    # Mock the requests.get to simulate a successful API response
    with patch('genie_bot.requests.get') as mocked_get:
        mocked_get.return_value.json.return_value = "Hello from FastAPI server"
        mocked_get.return_value.status_code = 200

        # Run the function
        await api_command(update, context)

        # Assertions
        update.message.reply_text.assert_called_once_with("Hello from FastAPI server")


@pytest.mark.asyncio
async def test_api_command_request_failure():
    # Setup Mocks
    update = AsyncMock(Update)
    context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    message = AsyncMock(Message)
    update.message = message

    # Mock the requests.get to simulate a failed API response
    with patch('genie_bot.requests.get') as mocked_get:
        mocked_get.side_effect = requests.RequestException('Failed to connect')

        # Run the function
        await api_command(update, context)

        # Assertions
        update.message.reply_text.assert_called_once_with('Request failed: Failed to connect')

@pytest.mark.asyncio
async def test_api_command_unexpected_error():
    # Setup Mocks
    update = AsyncMock(Update)
    context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    message = AsyncMock(Message)
    update.message = message

    # Mock the requests.get to simulate an unexpected error
    with patch('genie_bot.requests.get') as mocked_get:
        mocked_get.side_effect = Exception('Unexpected error')

        # Run the function
        await api_command(update, context)

        # Assertions
        update.message.reply_text.assert_called_once_with('An unexpected error occurred: Unexpected error')