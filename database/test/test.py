from datetime import datetime

market_last_update = (datetime.fromisoformat("2024-08-15T00:02:42Z".rstrip('Z'))).timestamp()
print(market_last_update)
print(type(market_last_update))