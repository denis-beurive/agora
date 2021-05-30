class Record:

    def __init__(self,
                 in_hash: str,
                 in_date: str,
                 in_btc: str,
                 in_usd: str,
                 in_rate: str,
                 in_ship_from: str,
                 in_vendor_name: str,
                 in_name: str,
                 in_description: str):
        self._hash: str = in_hash
        self._date: str = in_date
        self._btc: float = float(in_btc)
        self._usd: float = float(in_usd)
        self._rate: float = float(in_rate)
        self._ship_from: str = in_ship_from
        self._vendor_name: str = in_vendor_name
        self._name: str = in_name
        self._description: str = in_description

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def date(self) -> str:
        return self._date

    @property
    def btc(self) -> float:
        return self._btc

    @property
    def usd(self) -> float:
        return self._usd

    @property
    def rate(self) -> float:
        return self._rate

    @property
    def ship_from(self) -> str:
        return self._ship_from

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description
