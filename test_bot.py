import pytest
from unittest.mock import AsyncMock
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
        "/help - Show this help message"
    )
    update.message.reply_text.assert_called_once_with(help_text)

@pytest.mark.asyncio
async def test_get_public_ip():
    update = AsyncMock(Update)
    context = AsyncMock(ContextTypes.DEFAULT_TYPE)
    message = AsyncMock(Message)
    update.message = message

    with patch('genie_bot.bot.requests.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = {'ip': '123.123.123.123'}
        mock_get.return_value = mock_response

        await get_public_ip(update, context)

        called_args = update.message.reply_text.call_args[0][0]
        ip_address = called_args.split()[-1]
        
        # Regular expression to validate an IPv4 address
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        assert ip_pattern.match(ip_address), f"IP address format is incorrect: {ip_address}"