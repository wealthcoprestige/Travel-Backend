import requests
from travel.models.rate import Rate
from decimal import Decimal



def process_payment(tx, call_back_url, amount):
    url = f'https://dreamway.store/api/v1/paystack/transfer/payment/78233644?call_back_url={call_back_url}'
    
    rate_obj = Rate.objects.first()
    rate_amount = rate_obj.amount if rate_obj else Decimal('12.35')
    
    amount = Decimal(str(amount)) * Decimal(str(rate_amount))  
    
    data = {
        "reference": tx.transaction_id,
        "amount": str(round(amount, 2))
    }

    response = requests.post(url, json=data)
    return response


def confirm_transaction(reference):
    """Verify transaction with payment provider."""
    url = f"https://dreamway.store/api/v1/verify/transaction/pay?reference={reference}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
       
        return resp.json()
    except (requests.RequestException, ValueError):
     
        return {"success": False, "data": {"status": "failed"}}