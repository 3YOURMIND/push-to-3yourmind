"""
This module contains NoValue class and type aliases for type annotations
"""

import datetime
import decimal
import typing as t


__all__ = ["NoValue"]


class NoValue:
    """
    Some class methods accept arguments that are optional. Skipping them means
    "no data changed" and will lead to not sending them to the 3YD API. To skip such an
    argument give it a `NoValue` value.

    For example, `client.my_profile.set_preferences` can accept 4 arguments:
    country, currency, language, unit. If you need to update user's unit but leave other
    settings unchanged:

    >>> client.my_profile.set_preferences(unit="inch", country=NoValue, currency=NoValue, language=NoValue)
    # or shorter
    >>> client.my_profile.set_preferences(unit="inch")

    The following:

    >>> client.my_profile.set_preferences(unit="inch", country=None, currency=None, language=None)

    ... it will mean that you want to set user's country, currency and language setting to NULL.
    """

NoValueType = t.Type[NoValue]
ResponseDict = t.Dict[str, t.Any]
AnyResponse = t.Union[str, ResponseDict, t.List[ResponseDict], t.List[str]]
RequestMethod = t.Literal["GET", "PUT", "POST", "DELETE", "PATCH", "HEAD"]
Unit = t.Literal["mm", "inch"]
AttachmentFileSpecifier = CadFileSpecifier = t.Union[str, t.IO]

OptionalInteger = t.Union[int, NoValueType]
OptionalIntegerSequence = t.Sequence[OptionalInteger]
OptionalNumber = t.Union[int, float, decimal.Decimal, NoValueType]
OptionalNumberSequence = t.Sequence[OptionalNumber]
OptionalString = t.Union[str, bytes, NoValueType]
OptionalDate = t.Union[datetime.date, NoValueType]
OptionalDateTime = t.Union[datetime.datetime, NoValueType]
