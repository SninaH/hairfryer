from urllib.parse import urlparse, parse_qs
from typing import Optional

def get_query_param_value(url: str, param: str) -> Optional[str]:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    values = query_params.get(param)
    return values[0] if values else None