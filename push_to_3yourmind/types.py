import datetime
import decimal
import typing as t


class NoValue:
    pass


ResponseDict = t.Dict[str, t.Any]
AnyResponse = t.Union[str, ResponseDict, t.List[ResponseDict], t.List[str]]
RequestMethod = t.Literal["GET", "PUT", "POST", "DELETE", "PATCH", "HEAD"]
Unit = t.Literal["mm", "inch"]

OptionalNumber = t.Union[int, float, decimal.Decimal, t.Type[NoValue]]
OptionalString = t.Union[str, bytes, t.Type[NoValue]]
OptionalDate = t.Union[datetime.date, t.Type[NoValue]]
OptionalDateTime = t.Union[datetime.datetime, t.Type[NoValue]]
