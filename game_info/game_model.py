from typing import List, Optional, Tuple, Union
from pydantic import BaseModel
from datetime import datetime


# Title
class StarRating(BaseModel):
    rating: Optional[float]
    count: Optional[Union[int, str]]


class Title(BaseModel):
    edition: Optional[str] = None
    name: str
    platforms: Optional[List[str]] = None
    publisher: Optional[str]
    release: Optional[str]
    star_rating: Optional[StarRating] = None
    category: Optional[str] = None


# Price
class PriceInfo(BaseModel):
    basePrice: Optional[str]
    discountedPrice: Optional[str]
    discountText: Optional[str]
    serviceBranding: Optional[List[str]]
    endTime: Optional[str]
    upsellText: Optional[str]
    basePriceValue: Optional[int]
    discountedValue: Optional[int]
    currencyCode: Optional[str]
    qualifications: Optional[Union[List[str], List]]
    applicability: Optional[str]
    campaignId: Optional[str]
    rewardId: Optional[str]
    isFree: Optional[bool]
    isExclusive: Optional[bool]
    isTiedToSubscription: Optional[bool]


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
    publisher: Optional[str]
    release: str
    spoken_languages: Optional[List[str]] = None
    screen_languages: Optional[List[str]] = None
    platforms: Optional[List[str]] = None
    description: List[Tuple[str, str]]
    type: Optional[str] = None


class AddonPrice(BaseModel):
    discountedPrice: Optional[str]
    discountText: Optional[str]
    isExclusive: Optional[bool]
    upsellText: Optional[str]
    upsellServiceBranding: Optional[List[str]]
    serviceBranding: Optional[List[str]]
    basePrice: Optional[str]
    isFree: Optional[bool]
    isTiedToSubscription: Optional[bool]


class Addon(BaseModel):
    id: str
    image: str
    genres: Optional[List[str]]
    classification: str
    name: str
    platforms: List[str]
    type: str
    price: Optional[AddonPrice]


class Edition(BaseModel):
    name: Optional[str]
    features: List[str]
    type: Optional[str]


class EditionItem(BaseModel):
    id: str
    category: str
    platforms: List[str]
    image: List[Tuple[str, str]]
    edition: Optional[Edition]
    content_rating: Optional[str]
    genres: Optional[List[str]]
    name: str
    price: List[PriceType1]


class Game(BaseModel):
    id: str
    product_id: Tuple[str, str]
    image: Union[List[Tuple[str, str]], str]
    title: Title
    price: Union[List[PriceType1], List[PriceType2]]
    content_rating: Optional[ContentRating]
    editions: Optional[List[EditionItem]]
    addons: Optional[List[Addon]]
    info: Info
    info_date: str
