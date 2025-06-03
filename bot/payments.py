
from aiosend import CryptoPay, TESTNET
from aiosend.webhook import FastAPIManager
from aiosend.types import Invoice

from bot.config import CRYPTOPAY_TOKEN

from fastapi import FastAPI
from aiosend.webhook import FastAPIManager

def init_cryptopay(app: FastAPI):
    return CryptoPay(
        CRYPTOPAY_TOKEN,
        webhook_manager=FastAPIManager(app, "/handler"),
        network=TESTNET,
    )

# @cp.webhook()
# async def handler(invoice: Invoice) -> None:
#     print(f"Received {invoice.amount} {invoice.asset}")


# async def main() -> None:
#     invoice = await cp.create_invoice(1, "USDT")
#     print("invoice link:", invoice.bot_invoice_url)

