import time
import pytest
import requests
from unittest.mock import AsyncMock, patch, MagicMock
from telegram import Update, Message
from telegram.ext import ContextTypes
from genie_bot import *
import statistics
from config import CONSTANTS

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

    update.message.reply_text.assert_called_once_with(CONSTANTS.HELP_COMMAND_TEXT)

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

@patch('requests.post')
async def test_question_command_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "Here is your coding question."}
    mock_update = AsyncMock(Update)
    mock_context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    message = AsyncMock(Message)
    
    mock_update.message = message
    await question_command(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("Server response: Here is your coding question.")

@patch('requests.post')
async def test_question_command_failure():
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "Here is your coding question."}
    mock_update = AsyncMock(Update)
    mock_context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    
    with patch('genie_bot.requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.RequestException("Network error")
        await question_command(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_with("An error occurred: Network error")

@patch('requests.post')
async def test_question_command_latency():
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "Here is your coding question."}
    mock_update = AsyncMock(Update)
    mock_context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "Here is your coding question."}
    with patch('genie_bot.requests.post') as mock_post:
        mock_post.return_value = mock_response
        latencies = []
        num_tests = 10

        for _ in range(num_tests):
            start_time = time.time()
            await question_command(mock_update, mock_context)
            end_time = time.time()
            latencies.append(end_time - start_time)

        average_latency = statistics.mean(latencies)
        print(f"Average latency: {average_latency:.4f} seconds")

        assert average_latency > 0  # Ensure latency is measured
        mock_update.message.reply_text.assert_called_with("Server response: Here is your coding question.")

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
        