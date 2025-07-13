from enum import Enum
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
import math
from .core import Element, Direction, Season, Polarity


class TrigramLine(Enum):
    """Represents a single line in a trigram"""
    YANG = "⚊"  # Unbroken line
    YIN = "⚋"  # Broken line


class Trigram:
    """Represents a complete trigram with all its metaphysical attributes"""

    def __init__(self, chinese: str, pinyin: str, english: str,
                 lines: Tuple[TrigramLine, TrigramLine, TrigramLine],
                 element: Element, direction: Direction, season: Season,
                 family_position: str, quality: str, attributes: List[str],
                 strategic_application: str, shadow_aspect: str,
                 cultivation_practices: Dict[str, str],
                 symbolic_associations: Dict[str, str]):
        self.chinese = chinese
        self.pinyin = pinyin
        self.english = english
        self.lines = lines  # Bottom to top
        self.element = element
        self.direction = direction
        self.season = season
        self.family_position = family_position
        self.quality = quality
        self.attributes = attributes
        self.strategic_application = strategic_application
        self.shadow_aspect = shadow_aspect
        self.cultivation_practices = cultivation_practices
        self.symbolic_associations = symbolic_associations

    def __str__(self):
        """Visual representation of the trigram"""
        line_symbols = [line.value for line in reversed(self.lines)]  # Top to bottom for display
        return f"{self.chinese} ({self.pinyin})\n" + "\n".join(line_symbols)

    def __repr__(self):
        return f"Trigram({self.chinese}, {self.english})"

    def get_visual_symbol(self) -> str:
        """Get the Unicode symbol for this trigram"""
        symbols = {
            ("⚊", "⚊", "⚊"): "☰",  # Qian
            ("⚋", "⚋", "⚋"): "☷",  # Kun
            ("⚊", "⚋", "⚋"): "☳",  # Zhen
            ("⚋", "⚊", "⚊"): "☴",  # Xun
            ("⚋", "⚊", "⚋"): "☵",  # Kan
            ("⚊", "⚋", "⚊"): "☲",  # Li
            ("⚋", "⚋", "⚊"): "☶",  # Gen
            ("⚊", "⚊", "⚋"): "☱",  # Dui
        }
        line_pattern = tuple(line.value for line in reversed(self.lines))
        return symbols.get(line_pattern, "?")

    def is_yang_trigram(self) -> bool:
        """Check if this is a yang trigram (more yang lines than yin)"""
        yang_count = sum(1 for line in self.lines if line == TrigramLine.YANG)
        return yang_count > len(self.lines) / 2

    def get_dominant_polarity(self) -> Polarity:
        """Get the dominant polarity of this trigram"""
        return Polarity.YANG if self.is_yang_trigram() else Polarity.YIN


class EightTrigrams:
    """Container class for all eight trigrams with complete metaphysical data"""

    def __init__(self):
        self.trigrams = [
            # ☰ 乾 (Qian) - Heaven
            Trigram(
                chinese="乾", pinyin="qián", english="Heaven",
                lines=(TrigramLine.YANG, TrigramLine.YANG, TrigramLine.YANG),
                element=Element.METAL, direction=Direction.NORTH, season=Season.AUTUMN,
                family_position="Father",
                quality="Pure yang creativity, leadership, father principle, initiation",
                attributes=["Strength", "Persistence", "Authority", "Nobility", "Creative power"],
                strategic_application="Taking command, initiating projects, establishing authority",
                shadow_aspect="Rigidity, domination, inflexibility, excessive force",
                cultivation_practices={
                    "physical": "Standing meditation facing northwest, dragon breathing",
                    "mental": "Develop unwavering determination and clear decision-making",
                    "spiritual": "Connect with creative principle that initiates all manifestation"
                },
                symbolic_associations={
                    "animal": "Dragon, Horse",
                    "body_part": "Head, Brain",
                    "time": "Late autumn, 7-11 PM",
                    "weather": "Clear sky, Dry wind",
                    "landscape": "Heaven, High mountains"
                }
            ),

            # ☷ 坤 (Kun) - Earth
            Trigram(
                chinese="坤", pinyin="kūn", english="Earth",
                lines=(TrigramLine.YIN, TrigramLine.YIN, TrigramLine.YIN),
                element=Element.EARTH, direction=Direction.SOUTH, season=Season.LATE_SUMMER,
                family_position="Mother",
                quality="Pure yin receptivity, nourishment, mother principle, completion",
                attributes=["Devotion", "Yielding", "Support", "Fertility", "Receptive power"],
                strategic_application="Providing foundation, supporting others, patient development",
                shadow_aspect="Passivity, dependency, lack of initiative, excessive yielding",
                cultivation_practices={
                    "physical": "Earth-sitting meditation, connecting directly with soil",
                    "mental": "Develop infinite patience and supportive awareness",
                    "spiritual": "Embody receptive principle that nourishes all growth"
                },
                symbolic_associations={
                    "animal": "Ox, Mare",
                    "body_part": "Abdomen, Stomach",
                    "time": "Late summer, 1-3 PM",
                    "weather": "Cloudy, Humid",
                    "landscape": "Plains, Fields"
                }
            ),

            # ☳ 震 (Zhen) - Thunder
            Trigram(
                chinese="震", pinyin="zhèn", english="Thunder",
                lines=(TrigramLine.YANG, TrigramLine.YIN, TrigramLine.YIN),
                element=Element.WOOD, direction=Direction.EAST, season=Season.SPRING,
                family_position="Eldest Son",
                quality="Sudden movement, awakening, eldest son, shocking action",
                attributes=["Initiative", "Surprise", "Arousal", "Movement", "Breakthrough"],
                strategic_application="Breakthrough moments, decisive action, overcoming inertia",
                shadow_aspect="Impulsiveness, shock without purpose, restlessness",
                cultivation_practices={
                    "physical": "Explosive movement exercises followed by stillness",
                    "mental": "Develop capacity for sudden insight and immediate action",
                    "spiritual": "Align with awakening force that breaks through stagnation"
                },
                symbolic_associations={
                    "animal": "Dragon emerging, Young horse",
                    "body_part": "Feet, Legs",
                    "time": "Spring dawn, 3-7 AM",
                    "weather": "Thunder, Lightning",
                    "landscape": "Forest, Bamboo grove"
                }
            ),

            # ☴ 巽 (Xun) - Wind
            Trigram(
                chinese="巽", pinyin="xùn", english="Wind",
                lines=(TrigramLine.YIN, TrigramLine.YANG, TrigramLine.YANG),
                element=Element.WOOD, direction=Direction.SOUTH, season=Season.SPRING,
                family_position="Eldest Daughter",
                quality="Gentle penetration, gradual influence, eldest daughter, subtle power",
                attributes=["Persistence", "Flexibility", "Influence", "Gradual progress", "Penetration"],
                strategic_application="Long-term influence, gentle persuasion, gradual change",
                shadow_aspect="Indecisiveness, lack of force when needed, over-subtlety",
                cultivation_practices={
                    "physical": "Flowing movements that gradually increase in intensity",
                    "mental": "Develop subtle influence and persistent gentle pressure",
                    "spiritual": "Embody penetrating power that works through patience"
                },
                symbolic_associations={
                    "animal": "Rooster, Crane",
                    "body_part": "Thighs, Breathing",
                    "time": "Late spring, 7-11 AM",
                    "weather": "Gentle wind, Breeze",
                    "landscape": "Tall trees, Valleys"
                }
            ),

            # ☵ 坎 (Kan) - Water
            Trigram(
                chinese="坎", pinyin="kǎn", english="Water",
                lines=(TrigramLine.YIN, TrigramLine.YANG, TrigramLine.YIN),
                element=Element.WATER, direction=Direction.NORTH, season=Season.WINTER,
                family_position="Middle Son",
                quality="Danger and depth, middle son, flowing around obstacles",
                attributes=["Adaptability", "Depth", "Danger", "Wisdom", "Flow"],
                strategic_application="Navigating difficulties, finding hidden paths, depth strategy",
                shadow_aspect="Excessive caution, getting lost in complexity, avoiding necessary risks",
                cultivation_practices={
                    "physical": "Swimming or water meditation, cold exposure",
                    "mental": "Develop ability to flow around obstacles while maintaining direction",
                    "spiritual": "Connect with wisdom that emerges from navigating difficulties"
                },
                symbolic_associations={
                    "animal": "Pig, Fish",
                    "body_part": "Ears, Kidneys",
                    "time": "Winter midnight, 11 PM-1 AM",
                    "weather": "Rain, Snow",
                    "landscape": "Rivers, Gorges"
                }
            ),

            # ☲ 離 (Li) - Fire
            Trigram(
                chinese="離", pinyin="lí", english="Fire",
                lines=(TrigramLine.YANG, TrigramLine.YIN, TrigramLine.YANG),
                element=Element.FIRE, direction=Direction.SOUTH, season=Season.SUMMER,
                family_position="Middle Daughter",
                quality="Brilliance and clarity, middle daughter, illumination",
                attributes=["Intelligence", "Beauty", "Clarity", "Attachment", "Illumination"],
                strategic_application="Brilliant manifestation, clear communication, inspiring others",
                shadow_aspect="Excessive attachment, superficial brilliance, burning out",
                cultivation_practices={
                    "physical": "Safe sun gazing and fire meditation, light therapy",
                    "mental": "Develop brilliant clarity and inspiring communication",
                    "spiritual": "Embody illuminating principle that reveals truth"
                },
                symbolic_associations={
                    "animal": "Pheasant, Firebird",
                    "body_part": "Eyes, Heart",
                    "time": "Summer noon, 11 AM-1 PM",
                    "weather": "Bright sun, Heat",
                    "landscape": "Bright places, Gardens"
                }
            ),

            # ☶ 艮 (Gen) - Mountain
            Trigram(
                chinese="艮", pinyin="gèn", english="Mountain",
                lines=(TrigramLine.YIN, TrigramLine.YIN, TrigramLine.YANG),
                element=Element.EARTH, direction=Direction.NORTH, season=Season.WINTER,
                family_position="Youngest Son",
                quality="Stillness and stopping, youngest son, meditation",
                attributes=["Stability", "Meditation", "Stopping", "Boundaries", "Stillness"],
                strategic_application="Strategic pauses, establishing boundaries, deep reflection",
                shadow_aspect="Stubbornness, isolation, inability to move when necessary",
                cultivation_practices={
                    "physical": "Mountain meditation, sitting in absolute stillness",
                    "mental": "Develop ability to stop mental activity completely",
                    "spiritual": "Connect with stillness that underlies all movement"
                },
                symbolic_associations={
                    "animal": "Dog, Bear",
                    "body_part": "Hands, Back",
                    "time": "Late winter, 1-7 AM",
                    "weather": "Mist, Fog",
                    "landscape": "Mountains, Hills"
                }
            ),

            # ☱ 兌 (Dui) - Lake
            Trigram(
                chinese="兌", pinyin="duì", english="Lake",
                lines=(TrigramLine.YANG, TrigramLine.YANG, TrigramLine.YIN),
                element=Element.METAL, direction=Direction.WEST, season=Season.AUTUMN,
                family_position="Youngest Daughter",
                quality="Joy and completion, youngest daughter, satisfaction",
                attributes=["Joy", "Completion", "Communication", "Pleasure", "Satisfaction"],
                strategic_application="Bringing joy to completion, celebrating success, harmonious communication",
                shadow_aspect="Superficial pleasure, avoiding necessary difficulties, excessive indulgence",
                cultivation_practices={
                    "physical": "Joyful movement and celebration, singing",
                    "mental": "Develop genuine appreciation and communicative joy",
                    "spiritual": "Embody satisfaction that comes from authentic completion"
                },
                symbolic_associations={
                    "animal": "Sheep, Swan",
                    "body_part": "Mouth, Lungs",
                    "time": "Autumn evening, 5-11 PM",
                    "weather": "Pleasant breeze, Autumn air",
                    "landscape": "Lakes, Marshes"
                }
            )
        ]

        # Create lookup dictionaries
        self.by_chinese = {trigram.chinese: trigram for trigram in self.trigrams}
        self.by_english = {trigram.english.lower(): trigram for trigram in self.trigrams}
        self.by_direction = {trigram.direction: trigram for trigram in self.trigrams}
        self.by_element = {}
        for trigram in self.trigrams:
            if trigram.element not in self.by_element:
                self.by_element[trigram.element] = []
            self.by_element[trigram.element].append(trigram)

    def get_by_chinese(self, chinese: str) -> Optional[Trigram]:
        """Get trigram by Chinese character"""
        return self.by_chinese.get(chinese)

    def get_by_english(self, english: str) -> Optional[Trigram]:
        """Get trigram by English name"""
        return self.by_english.get(english.lower())

    def get_by_direction(self, direction: Direction) -> Optional[Trigram]:
        """Get trigram by direction"""
        return self.by_direction.get(direction)

    def get_by_element(self, element: Element) -> List[Trigram]:
        """Get all trigrams of a specific element"""
        return self.by_element.get(element, [])


class Palace:
    """Represents a single palace in the Nine Palaces system"""

    def __init__(self, number: int, chinese_name: str, trigram: Optional[Trigram],
                 direction: Direction, element: Element, season: Season,
                 quality: str, strategic_use: str, cultivation_focus: str,
                 palace_attributes: Dict[str, str],
                 energy_characteristics: Dict[str, str]):
        self.number = number
        self.chinese_name = chinese_name
        self.trigram = trigram
        self.direction = direction
        self.element = element
        self.season = season
        self.quality = quality
        self.strategic_use = strategic_use
        self.cultivation_focus = cultivation_focus
        self.palace_attributes = palace_attributes
        self.energy_characteristics = energy_characteristics

    def __str__(self):
        trigram_symbol = self.trigram.get_visual_symbol() if self.trigram else "⚬"
        return f"Palace {self.number} ({self.chinese_name}) {trigram_symbol}"

    def __repr__(self):
        return f"Palace({self.number}, {self.chinese_name})"

    def is_center_palace(self) -> bool:
        """Check if this is the center palace"""
        return self.number == 5

    def get_opposing_palace(self, nine_palaces) -> 'Palace':
        """Get the palace opposite to this one"""
        # In the 3x3 grid, opposing palace numbers sum to 10 (except center)
        if self.number == 5:
            return self  # Center opposes itself
        opposing_number = 10 - self.number
        return nine_palaces.get_palace_by_number(opposing_number)


class LoShuSquare:
    """The Lo Shu magic square - foundation of Nine Palaces arrangement"""

    def __init__(self):
        # The classical Lo Shu arrangement
        self.square = [
            [4, 9, 2],  # Top row    (SE, S, SW)
            [3, 5, 7],  # Middle row (E,  C, W)
            [8, 1, 6]  # Bottom row (NE, N, NW)
        ]

        # Direction mapping for each position
        self.position_directions = {
            (0, 0): Direction.SOUTH,  # 4 - Southeast (corrected mapping)
            (0, 1): Direction.SOUTH,  # 9 - South
            (0, 2): Direction.SOUTH,  # 2 - Southwest (corrected mapping)
            (1, 0): Direction.EAST,  # 3 - East
            (1, 1): Direction.CENTER,  # 5 - Center
            (1, 2): Direction.WEST,  # 7 - West
            (2, 0): Direction.NORTH,  # 8 - Northeast (corrected mapping)
            (2, 1): Direction.NORTH,  # 1 - North
            (2, 2): Direction.NORTH  # 6 - Northwest (corrected mapping)
        }

    def get_number_at_position(self, row: int, col: int) -> int:
        """Get the Lo Shu number at a specific grid position"""
        return self.square[row][col]

    def get_position_of_number(self, number: int) -> Tuple[int, int]:
        """Get the grid position of a specific number"""
        for row in range(3):
            for col in range(3):
                if self.square[row][col] == number:
                    return (row, col)
        raise ValueError(f"Number {number} not found in Lo Shu square")

    def verify_magic_properties(self) -> bool:
        """Verify that this is a valid magic square (all rows, columns, diagonals sum to 15)"""
        target_sum = 15

        # Check rows
        for row in self.square:
            if sum(row) != target_sum:
                return False

        # Check columns
        for col in range(3):
            if sum(self.square[row][col] for row in range(3)) != target_sum:
                return False

        # Check diagonals
        if sum(self.square[i][i] for i in range(3)) != target_sum:
            return False
        if sum(self.square[i][2 - i] for i in range(3)) != target_sum:
            return False

        return True


class NinePalaces:
    """The complete Nine Palaces system combining trigrams, directions, and cosmic forces"""

    def __init__(self):
        self.eight_trigrams = EightTrigrams()
        self.lo_shu = LoShuSquare()

        # Create the nine palaces
        self.palaces = [
            # Palace 1 - North Water Palace (坎宮)
            Palace(
                number=1, chinese_name="坎宮",
                trigram=self.eight_trigrams.get_by_chinese("坎"),
                direction=Direction.NORTH, element=Element.WATER, season=Season.WINTER,
                quality="Hidden depth, secret knowledge, mysterious resources",
                strategic_use="Accessing hidden information, developing deep strategies, working with subconscious forces",
                cultivation_focus="Deep meditation, accessing inner wisdom, patience development",
                palace_attributes={
                    "cosmic_function": "Storage of potential, hidden wisdom",
                    "temporal_quality": "Deep time, ancestral memory",
                    "consciousness_state": "Unconscious wisdom, intuitive knowing"
                },
                energy_characteristics={
                    "yin_yang_balance": "Deep yin with hidden yang core",
                    "movement_pattern": "Downward and inward flow",
                    "transformation_type": "Dissolution and regeneration"
                }
            ),

            # Palace 2 - Southwest Earth Palace (坤宮)
            Palace(
                number=2, chinese_name="坤宮",
                trigram=self.eight_trigrams.get_by_chinese("坤"),
                direction=Direction.SOUTH, element=Element.EARTH, season=Season.LATE_SUMMER,
                quality="Supportive foundation, maternal nourishment, receptive power",
                strategic_use="Building support networks, providing foundation for others, receptive leadership",
                cultivation_focus="Earth connection, supportive practices, developing infinite patience",
                palace_attributes={
                    "cosmic_function": "Universal nourishment, supportive matrix",
                    "temporal_quality": "Cyclical time, seasonal rhythms",
                    "consciousness_state": "Receptive awareness, maternal wisdom"
                },
                energy_characteristics={
                    "yin_yang_balance": "Pure yin receptivity",
                    "movement_pattern": "Horizontal spreading, nurturing embrace",
                    "transformation_type": "Gradual nourishment and growth"
                }
            ),

            # Palace 3 - East Thunder Palace (震宮)
            Palace(
                number=3, chinese_name="震宮",
                trigram=self.eight_trigrams.get_by_chinese("震"),
                direction=Direction.EAST, element=Element.WOOD, season=Season.SPRING,
                quality="Sudden breakthrough, initiating movement, shocking action",
                strategic_use="Breakthrough moments, initiating new phases, overcoming stagnation",
                cultivation_focus="Breakthrough meditation, sudden insight practices, dynamic action",
                palace_attributes={
                    "cosmic_function": "Initiating force, breakthrough energy",
                    "temporal_quality": "Sudden time, breakthrough moments",
                    "consciousness_state": "Awakening awareness, sudden insight"
                },
                energy_characteristics={
                    "yin_yang_balance": "Yang emerging from yin",
                    "movement_pattern": "Explosive upward and outward",
                    "transformation_type": "Sudden breakthrough and awakening"
                }
            ),

            # Palace 4 - Southeast Wind Palace (巽宮)
            Palace(
                number=4, chinese_name="巽宮",
                trigram=self.eight_trigrams.get_by_chinese("巽"),
                direction=Direction.SOUTH, element=Element.WOOD, season=Season.SPRING,
                quality="Gentle penetration, gradual influence, persistent pressure",
                strategic_use="Long-term influence campaigns, subtle persuasion, gradual change",
                cultivation_focus="Gentle persistence, subtle influence development, patient pressure",
                palace_attributes={
                    "cosmic_function": "Gradual penetration, subtle influence",
                    "temporal_quality": "Extended time, gradual process",
                    "consciousness_state": "Persistent awareness, gentle focus"
                },
                energy_characteristics={
                    "yin_yang_balance": "Gentle yang with yin foundation",
                    "movement_pattern": "Penetrating and dispersing",
                    "transformation_type": "Gradual infiltration and change"
                }
            ),

            # Palace 5 - Center Earth Palace (中宮)
            Palace(
                number=5, chinese_name="中宮",
                trigram=None,  # Center has no trigram
                direction=Direction.CENTER, element=Element.EARTH, season=Season.LATE_SUMMER,
                quality="Central command, integration point, cosmic axis",
                strategic_use="Coordinating all other palaces, maintaining balance, central command",
                cultivation_focus="Balance development, integration practices, central awareness",
                palace_attributes={
                    "cosmic_function": "Integration center, cosmic axis",
                    "temporal_quality": "Eternal present, timeless moment",
                    "consciousness_state": "Unified awareness, central consciousness"
                },
                energy_characteristics={
                    "yin_yang_balance": "Perfect equilibrium of all forces",
                    "movement_pattern": "Spiral integration, all directions",
                    "transformation_type": "Synthesis and unification"
                }
            ),

            # Palace 6 - Northwest Heaven Palace (乾宮)
            Palace(
                number=6, chinese_name="乾宮",
                trigram=self.eight_trigrams.get_by_chinese("乾"),
                direction=Direction.NORTH, element=Element.METAL, season=Season.AUTUMN,
                quality="Creative authority, leadership power, paternal strength",
                strategic_use="Establishing authority, creative leadership, initiating major projects",
                cultivation_focus="Leadership development, creative authority, paternal strength",
                palace_attributes={
                    "cosmic_function": "Creative force, divine authority",
                    "temporal_quality": "Initiating time, creative moments",
                    "consciousness_state": "Commanding awareness, creative consciousness"
                },
                energy_characteristics={
                    "yin_yang_balance": "Pure yang creativity",
                    "movement_pattern": "Upward and expansive, commanding",
                    "transformation_type": "Creative manifestation and leadership"
                }
            ),

            # Palace 7 - West Lake Palace (兌宮)
            Palace(
                number=7, chinese_name="兌宮",
                trigram=self.eight_trigrams.get_by_chinese("兌"),
                direction=Direction.WEST, element=Element.METAL, season=Season.AUTUMN,
                quality="Joyful completion, harmonious communication, satisfying results",
                strategic_use="Bringing projects to joyful completion, harmonious negotiations, celebration",
                cultivation_focus="Joy development, harmonious communication, completion satisfaction",
                palace_attributes={
                    "cosmic_function": "Completion force, joyful culmination",
                    "temporal_quality": "Completion time, harvest moments",
                    "consciousness_state": "Joyful awareness, satisfied consciousness"
                },
                energy_characteristics={
                    "yin_yang_balance": "Yang completion with yin satisfaction",
                    "movement_pattern": "Gathering and completing, celebratory",
                    "transformation_type": "Joyful completion and satisfaction"
                }
            ),

            # Palace 8 - Northeast Mountain Palace (艮宮)
            Palace(
                number=8, chinese_name="艮宮",
                trigram=self.eight_trigrams.get_by_chinese("艮"),
                direction=Direction.NORTH, element=Element.EARTH, season=Season.WINTER,
                quality="Still meditation, strategic pause, firm boundaries",
                strategic_use="Strategic pauses, establishing boundaries, deep reflection periods",
                cultivation_focus="Stillness meditation, boundary development, reflective practices",
                palace_attributes={
                    "cosmic_function": "Stabilizing force, boundary establishment",
                    "temporal_quality": "Pause time, reflective moments",
                    "consciousness_state": "Still awareness, meditative consciousness"
                },
                energy_characteristics={
                    "yin_yang_balance": "Stable yin with yang summit",
                    "movement_pattern": "Stopping and stabilizing, boundary-setting",
                    "transformation_type": "Stabilization and boundary formation"
                }
            ),

            # Palace 9 - South Fire Palace (離宮)
            Palace(
                number=9, chinese_name="離宮",
                trigram=self.eight_trigrams.get_by_chinese("離"),
                direction=Direction.SOUTH, element=Element.FIRE, season=Season.SUMMER,
                quality="Brilliant manifestation, clear illumination, inspiring beauty",
                strategic_use="Brilliant manifestation, clear communication, inspiring others",
                cultivation_focus="Clarity development, brilliant manifestation, inspiring communication",
                palace_attributes={
                    "cosmic_function": "Illuminating force, brilliant manifestation",
                    "temporal_quality": "Peak time, illumination moments",
                    "consciousness_state": "Clear awareness, illuminated consciousness"
                },
                energy_characteristics={
                    "yin_yang_balance": "Yang illumination with yin core",
                    "movement_pattern": "Radiating and illuminating, inspiring",
                    "transformation_type": "Illumination and brilliant manifestation"
                }
            )
        ]

        # Create lookup dictionaries
        self.by_number = {palace.number: palace for palace in self.palaces}
        self.by_chinese_name = {palace.chinese_name: palace for palace in self.palaces}
        self.by_direction = {palace.direction: palace for palace in self.palaces}
        self.by_element = {}
        for palace in self.palaces:
            if palace.element not in self.by_element:
                self.by_element[palace.element] = []
            self.by_element[palace.element].append(palace)

    def get_palace_by_number(self, number: int) -> Optional[Palace]:
        """Get palace by its number (1-9)"""
        return self.by_number.get(number)

    def get_palace_by_direction(self, direction: Direction) -> Optional[Palace]:
        """Get palace by its direction"""
        return self.by_direction.get(direction)

    def get_palace_by_chinese_name(self, name: str) -> Optional[Palace]:
        """Get palace by its Chinese name"""
        return self.by_chinese_name.get(name)

    def get_palaces_by_element(self, element: Element) -> List[Palace]:
        """Get all palaces of a specific element"""
        return self.by_element.get(element, [])

    def get_palace_grid_layout(self) -> List[List[Palace]]:
        """Get the palaces arranged in their traditional 3x3 grid layout"""
        grid = [[None for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                palace_number = self.lo_shu.get_number_at_position(row, col)
                grid[row][col] = self.get_palace_by_number(palace_number)

        return grid

    def display_palace_grid(self) -> str:
        """Display the Nine Palaces in their traditional grid arrangement"""
        grid = self.get_palace_grid_layout()
        result = "Nine Palaces Grid (九宮圖):\n\n"

        for row in grid:
            # Palace numbers and symbols
            symbols = []
            names = []
            for palace in row:
                if palace.trigram:
                    symbols.append(f"{palace.number}({palace.trigram.get_visual_symbol()})")
                else:
                    symbols.append(f"{palace.number}(⚬)")
                names.append(palace.chinese_name)

            result += "  ".join(f"{s:6}" for s in symbols) + "\n"
            result += "  ".join(f"{n:6}" for n in names) + "\n\n"

        return result