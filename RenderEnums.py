from enum import IntEnum


class ChatBubbleType(IntEnum):
    Random = 0
    Normal = 1
    Thought = 2


class EyeType(IntEnum):
    Random = 0
    NormalOpen = 1
    NormalClosed = 2
    AngryOpen = 3
    AngryClosed = 4
    SadOpen = 5
    SadClosed = 6


class MuzzleType(IntEnum):
    Random = 0
    Neutral = 1
    Angry = 2
    Laugh = 3
    Sad = 4
    Shock = 5


class FrameType(IntEnum):
    Random = 0
    Headshot = 1
    Bodyshot = 2
    TopToons = 3


class RenderType(IntEnum):
    Random = 0
    Toon = 1
    NPC = 2
    Doodle = 3
    Suit = 4
