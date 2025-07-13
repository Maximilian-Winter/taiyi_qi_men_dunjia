# taiyi.py - Updated with English translations

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
from enum import Enum
import math

from .core import Element, Direction, Season, Polarity
from .calendar import ChineseLunarCalendar, LunarDate, HeavenlyStem, EarthlyBranch
from .trigrams import NinePalaces, Palace, EightTrigrams, Trigram


class TaiyiStar(Enum):
    """The sixteen stars used in Taiyi calculation"""
    # Master Stars (主星)
    TAIYI = "太乙"  # Supreme Unity
    WENCHANG = "文昌"  # Literary Brightness
    SHETI = "摄提"  # Regulator
    XUANYUAN = "轩辕"  # Yellow Emperor
    ZHAOYAO = "招摇"  # Beckoning Distant
    TIANFU = "天符"  # Celestial Talisman
    QINGLONG = "青龙"  # Azure Dragon
    XIANCHI = "咸池"  # Universal Pool
    TAICHONG = "太冲"  # Great Rushing
    TIANYING = "天英"  # Celestial Hero

    # Guest Stars (客星)
    DADE = "大德"  # Great Virtue
    XIAODE = "小德"  # Small Virtue
    TIANGAN = "天刑"  # Celestial Punishment
    TAIYIN = "太阴"  # Great Yin
    TIANYI = "天乙"  # Celestial Unity
    TAIYUAN = "太元"  # Great Origin


class TaiyiCycle:
    """Represents a complete Taiyi cycle calculation"""

    def __init__(self, start_year: int):
        self.start_year = start_year
        self.cycle_length = 72  # Years in one Taiyi cycle
        self.palace_sequence = [1, 2, 3, 4, 6, 7, 8, 9]  # Palace 5 (center) is skipped in movement

    def get_year_in_cycle(self, year: int) -> int:
        """Get the position of a year within the 72-year cycle"""
        return ((year - self.start_year) % self.cycle_length) + 1

    def get_cycle_number(self, year: int) -> int:
        """Get which cycle number this year belongs to"""
        return ((year - self.start_year) // self.cycle_length) + 1


@dataclass
class AccumulatedYears:
    """Taiyi accumulated years calculation (积年)"""
    total_years: int
    cycle_years: int
    remainder_years: int
    palace_position: int

    def __str__(self):
        return f"Accumulated Years: {self.total_years}, Cycles: {self.cycle_years}, Remainder: {self.remainder_years}, Palace Position: {self.palace_position}"


@dataclass
class TaiyiStarPosition:
    """Position of a Taiyi star in the palace system"""
    star: TaiyiStar
    palace: Palace
    is_master: bool  # True for master star, False for guest star
    influence_strength: float  # 0.0 to 1.0

    def __str__(self):
        star_type = "Master Star" if self.is_master else "Guest Star"
        return f"{self.star.value} ({star_type}) resides in {self.palace.chinese_name}"


@dataclass
class TaiyiDivination:
    """Complete Taiyi divination result"""
    query_date: datetime
    lunar_date: LunarDate
    accumulated_years: AccumulatedYears
    master_star_position: TaiyiStarPosition
    guest_star_position: TaiyiStarPosition
    active_palace: Palace
    supporting_palaces: List[Palace]
    conflicting_palaces: List[Palace]
    overall_assessment: str
    strategic_guidance: str
    timing_analysis: Dict[str, str]
    elemental_influences: Dict[Element, float]

    def __str__(self):
        return f"Taiyi Divine Calculation - {self.query_date.strftime('%Y-%m-%d %H:%M')}\n{self.overall_assessment}"


class TaiyiCalculator:
    """Complete Taiyi Divine Calculation system"""

    def __init__(self):
        self.calendar = ChineseLunarCalendar()
        self.nine_palaces = NinePalaces()
        self.eight_trigrams = EightTrigrams()

        # Taiyi reference epoch: 1864 (甲子年)
        self.epoch_year = 1864
        self.taiyi_cycle = TaiyiCycle(self.epoch_year)

        # Star movement patterns
        self.master_star_sequence = [
            TaiyiStar.TAIYI, TaiyiStar.WENCHANG, TaiyiStar.SHETI, TaiyiStar.XUANYUAN,
            TaiyiStar.ZHAOYAO, TaiyiStar.TIANFU, TaiyiStar.QINGLONG, TaiyiStar.XIANCHI,
            TaiyiStar.TAICHONG, TaiyiStar.TIANYING
        ]

        self.guest_star_sequence = [
            TaiyiStar.DADE, TaiyiStar.XIAODE, TaiyiStar.TIANGAN,
            TaiyiStar.TAIYIN, TaiyiStar.TIANYI, TaiyiStar.TAIYUAN
        ]

        # Palace movement patterns for different stars
        self.palace_sequences = {
            "forward": [1, 2, 3, 4, 6, 7, 8, 9],  # Normal forward movement
            "reverse": [9, 8, 7, 6, 4, 3, 2, 1],  # Reverse movement
            "center_out": [5, 1, 9, 2, 8, 3, 7, 4, 6],  # From center outward
        }

    def calculate_accumulated_years(self, target_year: int) -> AccumulatedYears:
        """
        Calculate the Taiyi accumulated years (积年) for a given year
        This is the foundational calculation for all Taiyi divination
        """
        total_years = target_year - self.epoch_year

        # Taiyi uses a 72-year cycle divided into 8 palace positions
        cycle_years = total_years // 72
        remainder_years = total_years % 72

        # Calculate palace position based on remainder
        # Each palace governs 9 years in the cycle
        palace_cycle_position = (remainder_years // 9) % 8
        palace_position = self.palace_sequences["forward"][palace_cycle_position]

        return AccumulatedYears(
            total_years=total_years,
            cycle_years=cycle_years,
            remainder_years=remainder_years,
            palace_position=palace_position
        )

    def calculate_master_star_position(self, accumulated_years: AccumulatedYears,
                                       lunar_date: LunarDate) -> TaiyiStarPosition:
        """Calculate the position of the master star (主星)"""

        # Master star selection based on year stem
        year_stem_index = self.calendar.heavenly_stems.stems.index(lunar_date.year_stem)
        master_star = self.master_star_sequence[year_stem_index % len(self.master_star_sequence)]

        # Palace calculation incorporating multiple factors
        base_palace = accumulated_years.palace_position
        month_adjustment = (lunar_date.month - 1) % 8
        day_adjustment = (lunar_date.day - 1) % 8

        # Complex palace calculation
        adjusted_palace_index = (base_palace - 1 + month_adjustment + day_adjustment) % 8
        final_palace_number = self.palace_sequences["forward"][adjusted_palace_index]

        palace = self.nine_palaces.get_palace_by_number(final_palace_number)

        # Calculate influence strength based on elemental harmony
        influence_strength = self._calculate_influence_strength(
            lunar_date.year_stem.element, palace.element
        )

        return TaiyiStarPosition(
            star=master_star,
            palace=palace,
            is_master=True,
            influence_strength=influence_strength
        )

    def calculate_guest_star_position(self, accumulated_years: AccumulatedYears,
                                      lunar_date: LunarDate, hour: int) -> TaiyiStarPosition:
        """Calculate the position of the guest star (客星)"""

        # Guest star selection based on day branch
        day_branch_index = self.calendar.earthly_branches.branches.index(lunar_date.day_branch)
        guest_star = self.guest_star_sequence[day_branch_index % len(self.guest_star_sequence)]

        # Guest star moves more dynamically, incorporating hour
        base_palace = accumulated_years.palace_position
        hour_adjustment = (hour // 2) % 8  # Each branch covers 2 hours
        seasonal_adjustment = self._get_seasonal_adjustment(lunar_date.month)

        adjusted_palace_index = (base_palace - 1 + hour_adjustment + seasonal_adjustment) % 8
        final_palace_number = self.palace_sequences["reverse"][adjusted_palace_index]

        palace = self.nine_palaces.get_palace_by_number(final_palace_number)

        # Guest star influence varies by time
        influence_strength = self._calculate_time_based_influence(hour, lunar_date.day)

        return TaiyiStarPosition(
            star=guest_star,
            palace=palace,
            is_master=False,
            influence_strength=influence_strength
        )

    def _calculate_influence_strength(self, stem_element: Element, palace_element: Element) -> float:
        """Calculate the influence strength based on elemental relationships"""

        # Five Element generation and destruction cycles
        generation_cycle = {
            Element.WOOD: Element.FIRE,
            Element.FIRE: Element.EARTH,
            Element.EARTH: Element.METAL,
            Element.METAL: Element.WATER,
            Element.WATER: Element.WOOD
        }

        destruction_cycle = {
            Element.WOOD: Element.EARTH,
            Element.EARTH: Element.WATER,
            Element.WATER: Element.FIRE,
            Element.FIRE: Element.METAL,
            Element.METAL: Element.WOOD
        }

        if stem_element == palace_element:
            return 1.0  # Perfect harmony
        elif generation_cycle.get(stem_element) == palace_element:
            return 0.8  # Generating relationship
        elif generation_cycle.get(palace_element) == stem_element:
            return 0.7  # Being generated
        elif destruction_cycle.get(stem_element) == palace_element:
            return 0.3  # Destructive relationship
        elif destruction_cycle.get(palace_element) == stem_element:
            return 0.2  # Being destroyed
        else:
            return 0.5  # Neutral relationship

    def _calculate_time_based_influence(self, hour: int, day: int) -> float:
        """Calculate influence strength based on temporal factors"""
        # Peak influence during certain hours
        peak_hours = [5, 11, 17, 23]  # Dawn, noon, dusk, midnight
        hour_factor = 1.0 if hour in peak_hours else 0.6

        # Day cycle influence
        day_factor = 0.5 + 0.5 * math.sin(2 * math.pi * day / 30)

        return min(1.0, hour_factor * day_factor)

    def _get_seasonal_adjustment(self, month: int) -> int:
        """Get seasonal adjustment for palace calculations"""
        seasonal_adjustments = {
            1: 0, 2: 0, 3: 1,  # Spring
            4: 1, 5: 1, 6: 2,  # Summer
            7: 2, 8: 2, 9: 3,  # Autumn
            10: 3, 11: 3, 12: 0  # Winter
        }
        return seasonal_adjustments.get(month, 0)

    def analyze_palace_relationships(self, master_position: TaiyiStarPosition,
                                     guest_position: TaiyiStarPosition) -> Tuple[List[Palace], List[Palace]]:
        """Analyze supporting and conflicting palace relationships"""

        supporting_palaces = []
        conflicting_palaces = []

        master_palace = master_position.palace
        guest_palace = guest_position.palace

        # Analyze all palaces for relationships
        for palace in self.nine_palaces.palaces:
            if palace == master_palace or palace == guest_palace:
                continue

            # Check elemental relationships
            master_harmony = self._calculate_influence_strength(
                master_palace.element, palace.element
            )
            guest_harmony = self._calculate_influence_strength(
                guest_palace.element, palace.element
            )

            average_harmony = (master_harmony + guest_harmony) / 2

            if average_harmony >= 0.7:
                supporting_palaces.append(palace)
            elif average_harmony <= 0.3:
                conflicting_palaces.append(palace)

        return supporting_palaces, conflicting_palaces

    def calculate_elemental_influences(self, master_position: TaiyiStarPosition,
                                       guest_position: TaiyiStarPosition,
                                       lunar_date: LunarDate) -> Dict[Element, float]:
        """Calculate the influence of each element in the current configuration"""

        influences = {element: 0.0 for element in Element}

        # Master star influence
        influences[master_position.palace.element] += master_position.influence_strength * 0.4

        # Guest star influence
        influences[guest_position.palace.element] += guest_position.influence_strength * 0.3

        # Four pillars influence
        pillar_elements = [
            lunar_date.year_stem.element,
            lunar_date.month_stem.element,
            lunar_date.day_stem.element,
            lunar_date.hour_stem.element
        ]

        for element in pillar_elements:
            influences[element] += 0.075  # 0.3 / 4

        return influences

    def generate_overall_assessment(self, master_position: TaiyiStarPosition,
                                    guest_position: TaiyiStarPosition,
                                    supporting_palaces: List[Palace],
                                    conflicting_palaces: List[Palace]) -> str:
        """Generate overall assessment of the Taiyi configuration"""

        assessment_parts = []

        # Master star assessment
        master_strength = "strong" if master_position.influence_strength >= 0.7 else "moderate" if master_position.influence_strength >= 0.4 else "weak"
        assessment_parts.append(
            f"Master star {master_position.star.value} resides in {master_position.palace.chinese_name}, with {master_strength} influence")

        # Guest star assessment
        guest_strength = "strong" if guest_position.influence_strength >= 0.7 else "moderate" if guest_position.influence_strength >= 0.4 else "weak"
        assessment_parts.append(
            f"Guest star {guest_position.star.value} resides in {guest_position.palace.chinese_name}, with {guest_strength} influence")

        # Palace relationship assessment
        if len(supporting_palaces) > len(conflicting_palaces):
            assessment_parts.append("Palace positions provide mutual support, creating favorable circumstances")
        elif len(conflicting_palaces) > len(supporting_palaces):
            assessment_parts.append("Palace positions show conflicts, requiring cautious action")
        else:
            assessment_parts.append("Palace positions are balanced, suggesting a path of moderation")

        return "; ".join(assessment_parts) + "."

    def generate_strategic_guidance(self, master_position: TaiyiStarPosition,
                                    guest_position: TaiyiStarPosition,
                                    elemental_influences: Dict[Element, float]) -> str:
        """Generate strategic guidance based on the Taiyi configuration"""

        guidance_parts = []

        # Master palace guidance
        guidance_parts.append(f"Primary strategy: {master_position.palace.strategic_use}")

        # Guest palace guidance
        guidance_parts.append(f"Supporting strategy: {guest_position.palace.strategic_use}")

        # Elemental guidance
        dominant_element = max(elemental_influences.keys(), key=lambda x: elemental_influences[x])
        element_attributes = self.calendar.get_element_attributes(dominant_element)
        guidance_parts.append(f"Elemental guidance: {element_attributes['strategic_application']}")

        return "; ".join(guidance_parts) + "."

    def generate_timing_analysis(self, lunar_date: LunarDate,
                                 master_position: TaiyiStarPosition) -> Dict[str, str]:
        """Generate timing analysis for different time periods"""

        return {
            "Today": f"Favorable for {lunar_date.hour_branch.optimal_activities[0]}, avoid {lunar_date.hour_branch.avoid_activities[0]}",
            "This Month": f"Focus on developing {master_position.palace.element.value} element activities",
            "This Year": f"Year fortune guided by {lunar_date.year_stem.element.value} element dominance",
            "Long-term": f"Cultivate {master_position.palace.cultivation_focus}"
        }

    def perform_divination(self, query_date: datetime) -> TaiyiDivination:
        """Perform complete Taiyi divination for a given date and time"""

        # Convert to lunar date
        lunar_date = self.calendar.gregorian_to_lunar(query_date)

        # Calculate accumulated years
        accumulated_years = self.calculate_accumulated_years(lunar_date.year)

        # Calculate star positions
        master_position = self.calculate_master_star_position(accumulated_years, lunar_date)
        guest_position = self.calculate_guest_star_position(accumulated_years, lunar_date, query_date.hour)

        # Determine active palace (where the main energy is focused)
        active_palace = master_position.palace

        # Analyze palace relationships
        supporting_palaces, conflicting_palaces = self.analyze_palace_relationships(
            master_position, guest_position
        )

        # Calculate elemental influences
        elemental_influences = self.calculate_elemental_influences(
            master_position, guest_position, lunar_date
        )

        # Generate assessments
        overall_assessment = self.generate_overall_assessment(
            master_position, guest_position, supporting_palaces, conflicting_palaces
        )

        strategic_guidance = self.generate_strategic_guidance(
            master_position, guest_position, elemental_influences
        )

        timing_analysis = self.generate_timing_analysis(lunar_date, master_position)

        return TaiyiDivination(
            query_date=query_date,
            lunar_date=lunar_date,
            accumulated_years=accumulated_years,
            master_star_position=master_position,
            guest_star_position=guest_position,
            active_palace=active_palace,
            supporting_palaces=supporting_palaces,
            conflicting_palaces=conflicting_palaces,
            overall_assessment=overall_assessment,
            strategic_guidance=strategic_guidance,
            timing_analysis=timing_analysis,
            elemental_influences=elemental_influences
        )

    def display_divination_result(self, divination: TaiyiDivination) -> str:
        """Display formatted Taiyi divination result"""

        result = f"""
Taiyi Divine Calculation Result
{'=' * 50}

Query Time: {divination.query_date.strftime('%B %d, %Y at %H:%M')}
Lunar Time: Year {divination.lunar_date.year}, Month {divination.lunar_date.month}, Day {divination.lunar_date.day}

Accumulated Years Calculation:
{divination.accumulated_years}

Star Position Analysis:
{divination.master_star_position}
{divination.guest_star_position}

Active Palace: {divination.active_palace.chinese_name} - {divination.active_palace.quality}

Supporting Palaces: {', '.join([p.chinese_name for p in divination.supporting_palaces])}
Conflicting Palaces: {', '.join([p.chinese_name for p in divination.conflicting_palaces])}

Elemental Influences:
"""

        for element, influence in divination.elemental_influences.items():
            result += f"  {element.value}: {influence:.2f}\n"

        result += f"""
Overall Assessment:
{divination.overall_assessment}

Strategic Guidance:
{divination.strategic_guidance}

Timing Analysis:
"""

        for period, analysis in divination.timing_analysis.items():
            result += f"  {period}: {analysis}\n"

        return result