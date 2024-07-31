from typing import List, Optional, Tuple, Union
from pydantic import BaseModel
from datetime import datetime


# Title
class StarRating(BaseModel):
    rating: Optional[float]
    count: Optional[int]


class Title(BaseModel):
    edition: Optional[str] = None
    name: str
    platforms: Optional[List[str]] = None
    publisher: str
    release: str
    star_rating: Optional[StarRating] = None
    category: Optional[str] = None


# Price
class PriceInfo(BaseModel):
    basePrice: str
    discountedPrice: str
    discountText: Optional[str]
    serviceBranding: List[str]
    endTime: Optional[str]
    upsellText: Optional[str]
    basePriceValue: int
    discountedValue: int
    currencyCode: str
    qualifications: Union[List[str], List]
    applicability: str
    campaignId: Optional[str]
    rewardId: str
    isFree: bool
    isExclusive: bool
    isTiedToSubscription: bool


class PriceType1(BaseModel):
    type: str
    info: PriceInfo


class PriceType2(BaseModel):
    is_announce: bool


# Content rating
class ContentRating(BaseModel):
    name: str
    image: str
    interactive_elements: List[Optional[str]]
    descriptors: List[Optional[str]]


# Info
class Info(BaseModel):
    genres: Optional[List[str]]
    publisher: str
    release: str
    spoken_languages: Optional[List[str]] = None
    screen_languages: Optional[List[str]] = None
    platforms: Optional[List[str]] = None
    description: List[Tuple[str, str]]
    type: Optional[str] = None


class Game(BaseModel):
    id: str
    product_id: Tuple[str, str]
    href: str
    image: List[Tuple[str, str]]
    title: Title
    price: Union[List[PriceType1], List[PriceType2]]
    content_rating: Optional[ContentRating]
    info: Info
    info_date: datetime
