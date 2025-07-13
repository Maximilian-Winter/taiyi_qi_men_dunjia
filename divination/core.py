from enum import Enum


class Element(Enum):
    """Five Elements (Wu Xing) enumeration"""
    WOOD = "木"
    FIRE = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"


class Polarity(Enum):
    """Yin-Yang polarity"""
    YANG = "阳"
    YIN = "阴"


class Season(Enum):
    """Seasonal associations"""
    SPRING = "春"
    SUMMER = "夏"
    LATE_SUMMER = "长夏"
    AUTUMN = "秋"
    WINTER = "冬"


class Direction(Enum):
    """Directional associations"""
    EAST = "东"
    SOUTH = "南"
    CENTER = "中"
    WEST = "西"
    NORTH = "北"


class TranslationDict:
    """Comprehensive translation dictionary for all Chinese divination terms"""

    # Heavenly Stems
    STEMS = {
        "甲": "Jia (Wood Yang)",
        "乙": "Yi (Wood Yin)",
        "丙": "Bing (Fire Yang)",
        "丁": "Ding (Fire Yin)",
        "戊": "Wu (Earth Yang)",
        "己": "Ji (Earth Yin)",
        "庚": "Geng (Metal Yang)",
        "辛": "Xin (Metal Yin)",
        "壬": "Ren (Water Yang)",
        "癸": "Gui (Water Yin)"
    }

    # Earthly Branches
    BRANCHES = {
        "子": "Zi (Rat)",
        "丑": "Chou (Ox)",
        "寅": "Yin (Tiger)",
        "卯": "Mao (Rabbit)",
        "辰": "Chen (Dragon)",
        "巳": "Si (Snake)",
        "午": "Wu (Horse)",
        "未": "Wei (Goat)",
        "申": "Shen (Monkey)",
        "酉": "You (Rooster)",
        "戌": "Xu (Dog)",
        "亥": "Hai (Pig)"
    }

    # Five Elements
    ELEMENTS = {
        "木": "Wood",
        "火": "Fire",
        "土": "Earth",
        "金": "Metal",
        "水": "Water"
    }

    # Trigrams
    TRIGRAMS = {
        "乾": "Qian (Heaven)",
        "兌": "Dui (Lake)",
        "離": "Li (Fire)",
        "震": "Zhen (Thunder)",
        "巽": "Xun (Wind)",
        "坎": "Kan (Water)",
        "艮": "Gen (Mountain)",
        "坤": "Kun (Earth)"
    }

    # Nine Palaces
    PALACES = {
        "坎宮": "Kan Palace (North)",
        "坤宮": "Kun Palace (Southwest)",
        "震宮": "Zhen Palace (East)",
        "巽宮": "Xun Palace (Southeast)",
        "中宮": "Center Palace",
        "乾宮": "Qian Palace (Northwest)",
        "兌宮": "Dui Palace (West)",
        "艮宮": "Gen Palace (Northeast)",
        "離宮": "Li Palace (South)"
    }

    # Taiyi Nine Stars
    TAIYI_STARS = {
        "貪狼": "Greedy Wolf",
        "巨門": "Great Gate",
        "祿存": "Wealth Preservation",
        "文曲": "Literary Melody",
        "廉貞": "Pure Virtue",
        "武曲": "Military Music",
        "破軍": "Army Breaker",
        "左輔": "Left Assistant",
        "右弼": "Right Assistant"
    }

    # Eight Gates
    EIGHT_GATES = {
        "休門": "Rest Gate",
        "生門": "Life Gate",
        "傷門": "Injury Gate",
        "杜門": "Du Gate",
        "景門": "View Gate",
        "死門": "Death Gate",
        "驚門": "Fright Gate",
        "開門": "Open Gate"
    }

    # Nine Stars (Dunjia)
    DUNJIA_STARS = {
        "天蓬": "Heavenly Canopy",
        "天芮": "Heavenly Kernel",
        "天沖": "Heavenly Impulse",
        "天輔": "Heavenly Assistant",
        "天禽": "Heavenly Bird",
        "天心": "Heavenly Heart",
        "天柱": "Heavenly Pillar",
        "天任": "Heavenly Responsibility",
        "天英": "Heavenly Hero"
    }

    # Eight Spirits
    EIGHT_SPIRITS = {
        "值符": "Value Spirit",
        "騰蛇": "Soaring Snake",
        "太陰": "Grand Yin",
        "六合": "Six Harmony",
        "白虎": "White Tiger",
        "玄武": "Black Tortoise",
        "九地": "Nine Earth",
        "九天": "Nine Heaven"
    }

    # Twelve Generals (Liuren)
    TWELVE_GENERALS = {
        "貴人": "Noble Person",
        "螣蛇": "Soaring Snake",
        "朱雀": "Red Bird",
        "六合": "Six Harmony",
        "勾陳": "Hook Chen",
        "青龍": "Azure Dragon",
        "天空": "Heavenly Void",
        "白虎": "White Tiger",
        "太常": "Grand Constancy",
        "玄武": "Black Tortoise",
        "太陰": "Grand Yin",
        "天后": "Heavenly Empress"
    }

    # General Terms
    GENERAL_TERMS = {
        "吉": "Auspicious",
        "凶": "Inauspicious",
        "平": "Neutral",
        "大吉": "Very Auspicious",
        "陽遁": "Yang Escape",
        "陰遁": "Yin Escape",
        "上元": "Upper Yuan",
        "中元": "Middle Yuan",
        "下元": "Lower Yuan",
        "四課": "Four Courses",
        "三傳": "Three Transmissions",
        "初傳": "First Transmission",
        "中傳": "Middle Transmission",
        "末傳": "Final Transmission",
        "事之始": "Beginning of Matter",
        "事之中": "Middle of Matter",
        "事之終": "End of Matter",
        "幹上": "Stem Above",
        "支上": "Branch Above",
        "時幹": "Hour Stem",
        "遙克": "Remote Control",
        "順利發展": "Smooth Development",
        "多有阻礙": "Many Obstacles",
        "宜速不宜遲": "Better to Act Quickly",
        "宜緩不宜急": "Better to Act Slowly",
        "需防衝突": "Need to Prevent Conflicts",
        "有貴人相助，可積極行動": "Noble Person's Help, Can Act Actively",
        "需謹慎行事，防小人暗害": "Need to Act Cautiously, Beware of Hidden Harm",
        "注意": "Pay Attention To",
        "貴人相助": "Noble Person's Help",
        "驚恐怪異": "Fear and Strange Events",
        "文書口舌": "Documents and Speech",
        "和合喜慶": "Harmony and Celebration",
        "爭鬥官司": "Fighting and Lawsuits",
        "財帛喜事": "Wealth and Good News",
        "虛詐不實": "False and Deceptive",
        "刑傷凶喪": "Punishment and Mourning",
        "飲食喜慶": "Food and Celebration",
        "盜賊暗昧": "Thieves and Darkness",
        "陰私密事": "Secret Private Matters",
        "婦女陰事": "Women's Private Affairs",
        "統領": "Command",
        "驚恐": "Terror",
        "隱秘": "Secrecy",
        "和合": "Harmony",
        "刑傷": "Punishment",
        "盜失": "Theft",
        "隱藏": "Hiding",
        "顯揚": "Display",
        "北": "North",
        "西南": "Southwest",
        "東": "East",
        "東南": "Southeast",
        "中": "Center",
        "西北": "Northwest",
        "西": "West",
        "東北": "Northeast",
        "南": "South",
        "北北東": "North-Northeast",
        "東北東": "East-Northeast",
        "東南東": "East-Southeast",
        "南南東": "South-Southeast",
        "南南西": "South-Southwest",
        "西南西": "West-Southwest",
        "西北西": "West-Northwest",
        "北北西": "North-Northwest"
    }
