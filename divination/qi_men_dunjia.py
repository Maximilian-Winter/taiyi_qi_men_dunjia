# qimen.py - Qi Men Dun Jia Implementation

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
from enum import Enum
import math

from .core import Element, Direction, Season, Polarity
from .calendar import ChineseLunarCalendar, LunarDate, HeavenlyStem, EarthlyBranch
from .trigrams import NinePalaces, Palace


class QiMenGate(Enum):
    """The Eight Gates of Qi Men Dun Jia"""
    REST = "休門"  # Northwest - Withdrawal, recuperation
    LIFE = "生門"  # Northeast - Growth, opportunity
    HARM = "傷門"  # East - Conflict, wounding
    BLOCK = "杜門"  # Southeast - Obstruction, closure
    VIEW = "景門"  # South - Illumination, revelation
    DEATH = "死門"  # Southwest - Endings, transformation
    SHOCK = "驚門"  # West - Sudden change, alarm
    OPEN = "開門"  # North - Beginnings, breakthrough


class QiMenStar(Enum):
    """The Nine Stars of Qi Men Dun Jia"""
    PENGBIRD = "天蓬"  # Heavenly Canopy
    RENSEAL = "天任"  # Heavenly Responsibility
    CHONG = "天沖"  # Heavenly Rushing
    FU = "天輔"  # Heavenly Assistant
    YINGBIRD = "天英"  # Heavenly Hero
    RUIBIRD = "天芮"  # Heavenly Auspicious
    ZHU = "天柱"  # Heavenly Pillar
    XIN = "天心"  # Heavenly Heart
    QIN = "天禽"  # Heavenly Bird


class QiMenSpirit(Enum):
    """The Eight Spirits (Deities) of Qi Men Dun Jia"""
    ZHIFU = "值符"  # Duty Chief
    TENGSHE = "騰蛇"  # Soaring Snake
    TAIYIN = "太陰"  # Great Yin
    LIUHE = "六合"  # Six Harmonies
    BAIHU = "白虎"  # White Tiger
    XUANWU = "玄武"  # Black Tortoise
    JIUDI = "九地"  # Nine Earth
    JIUTIAN = "九天"  # Nine Heaven


class TimeFrame(Enum):
    """Different time frames for Qi Men calculation"""
    YEAR = "年家"  # Annual
    MONTH = "月家"  # Monthly
    DAY = "日家"  # Daily
    HOUR = "時家"  # Hourly


@dataclass
class QiMenConfiguration:
    """Complete configuration for one palace in Qi Men Dun Jia"""
    palace_number: int
    heavenly_stem: HeavenlyStem
    earthly_branch: EarthlyBranch
    gate: QiMenGate
    star: QiMenStar
    spirit: QiMenSpirit
    element: Element
    is_auspicious: bool
    energy_quality: str
    strategic_application: str


@dataclass
class QiMenChart:
    """Complete Qi Men Dun Jia chart"""
    calculation_time: datetime
    lunar_date: LunarDate
    time_frame: TimeFrame
    duty_chief_palace: int
    configurations: Dict[int, QiMenConfiguration]
    overall_pattern: str
    favorable_directions: List[Direction]
    unfavorable_directions: List[Direction]
    optimal_timing: str
    strategic_assessment: str


class QiMenCalculator:
    """Complete Qi Men Dun Jia calculation system"""

    def __init__(self):
        self.calendar = ChineseLunarCalendar()
        self.nine_palaces = NinePalaces()

        # Initialize gate sequences
        self.gate_sequence = [
            QiMenGate.REST, QiMenGate.LIFE, QiMenGate.HARM, QiMenGate.BLOCK,
            QiMenGate.VIEW, QiMenGate.DEATH, QiMenGate.SHOCK, QiMenGate.OPEN
        ]

        # Initialize star sequences
        self.star_sequence = [
            QiMenStar.PENGBIRD, QiMenStar.RENSEAL, QiMenStar.CHONG, QiMenStar.FU,
            QiMenStar.YINGBIRD, QiMenStar.RUIBIRD, QiMenStar.ZHU, QiMenStar.XIN, QiMenStar.QIN
        ]

        # Initialize spirit sequences
        self.spirit_sequence = [
            QiMenSpirit.ZHIFU, QiMenSpirit.TENGSHE, QiMenSpirit.TAIYIN, QiMenSpirit.LIUHE,
            QiMenSpirit.BAIHU, QiMenSpirit.XUANWU, QiMenSpirit.JIUDI, QiMenSpirit.JIUTIAN
        ]

        # Palace movement sequences
        self.yang_sequence = [1, 8, 3, 4, 9, 2, 7, 6]  # Yang time movement
        self.yin_sequence = [1, 6, 7, 2, 9, 4, 3, 8]  # Yin time movement

        # Auspicious gates
        self.auspicious_gates = {QiMenGate.REST, QiMenGate.LIFE, QiMenGate.OPEN}

        # Gate attributes
        self.gate_attributes = {
            QiMenGate.REST: {
                "element": Element.WATER,
                "quality": "Withdrawal and recuperation, strategic pause",
                "application": "Rest, planning, avoiding conflict"
            },
            QiMenGate.LIFE: {
                "element": Element.EARTH,
                "quality": "Growth and vitality, new opportunities",
                "application": "Starting projects, seeking advancement"
            },
            QiMenGate.HARM: {
                "element": Element.WOOD,
                "quality": "Conflict and injury, aggressive action",
                "application": "Military action, competitive situations"
            },
            QiMenGate.BLOCK: {
                "element": Element.WOOD,
                "quality": "Obstruction and closure, hidden activities",
                "application": "Secret operations, blocking enemies"
            },
            QiMenGate.VIEW: {
                "element": Element.FIRE,
                "quality": "Illumination and revelation, clear sight",
                "application": "Examinations, seeking clarity"
            },
            QiMenGate.DEATH: {
                "element": Element.EARTH,
                "quality": "Endings and transformation, dangerous power",
                "application": "Eliminating obstacles, dangerous missions"
            },
            QiMenGate.SHOCK: {
                "element": Element.METAL,
                "quality": "Sudden change and alarm, unexpected events",
                "application": "Surprising enemies, emergency action"
            },
            QiMenGate.OPEN: {
                "element": Element.METAL,
                "quality": "New beginnings and breakthrough, open paths",
                "application": "Important meetings, new ventures"
            }
        }

    def calculate_duty_chief(self, lunar_date: LunarDate, time_frame: TimeFrame) -> int:
        """Calculate the Duty Chief (值符) position"""

        if time_frame == TimeFrame.HOUR:
            # Hour-based calculation using day stem
            day_stem_index = self.calendar.heavenly_stems.stems.index(lunar_date.day_stem)
            hour_branch_index = self.calendar.earthly_branches.branches.index(lunar_date.hour_branch)

            # Complex calculation based on day stem and hour
            base_position = (day_stem_index * 6 + hour_branch_index) % 8
            return self.yang_sequence[base_position] if self._is_yang_time(lunar_date) else self.yin_sequence[
                base_position]

        elif time_frame == TimeFrame.DAY:
            # Day-based calculation
            day_stem_index = self.calendar.heavenly_stems.stems.index(lunar_date.day_stem)
            return self.yang_sequence[day_stem_index % 8]

        elif time_frame == TimeFrame.MONTH:
            # Month-based calculation
            month_stem_index = self.calendar.heavenly_stems.stems.index(lunar_date.month_stem)
            return self.yang_sequence[month_stem_index % 8]

        else:  # YEAR
            year_stem_index = self.calendar.heavenly_stems.stems.index(lunar_date.year_stem)
            return self.yang_sequence[year_stem_index % 8]

    def _is_yang_time(self, lunar_date: LunarDate) -> bool:
        """Determine if current time is yang or yin"""
        # Yang months: 1, 2, 3, 4, 5, 6 (Spring and Summer)
        # Yin months: 7, 8, 9, 10, 11, 12 (Autumn and Winter)
        return lunar_date.month <= 6

    def calculate_gate_positions(self, duty_chief_palace: int, is_yang_time: bool) -> Dict[int, QiMenGate]:
        """Calculate gate positions based on duty chief"""

        gate_positions = {}
        sequence = self.yang_sequence if is_yang_time else self.yin_sequence

        # Find duty chief position in sequence
        duty_chief_index = sequence.index(duty_chief_palace)

        # Arrange gates starting from duty chief position
        for i, gate in enumerate(self.gate_sequence):
            palace_index = (duty_chief_index + i) % 8
            palace_number = sequence[palace_index]
            gate_positions[palace_number] = gate

        return gate_positions

    def calculate_star_positions(self, duty_chief_palace: int, lunar_date: LunarDate) -> Dict[int, QiMenStar]:
        """Calculate star positions"""

        star_positions = {}

        # Star arrangement based on time factors
        time_factor = (lunar_date.day + lunar_date.hour_branch.hour_range[0]) % 9

        for i, star in enumerate(self.star_sequence):
            palace_number = ((duty_chief_palace - 1 + i + time_factor) % 8) + 1
            if palace_number == 5:  # Skip center palace
                palace_number = 9
            star_positions[palace_number] = star

        # Center palace always has specific star
        star_positions[5] = QiMenStar.QIN

        return star_positions

    def calculate_spirit_positions(self, duty_chief_palace: int, gate_positions: Dict[int, QiMenGate]) -> Dict[
        int, QiMenSpirit]:
        """Calculate spirit positions"""

        spirit_positions = {}

        # Duty Chief spirit always in duty chief palace
        spirit_positions[duty_chief_palace] = QiMenSpirit.ZHIFU

        # Other spirits follow specific patterns
        palace_sequence = [1, 2, 3, 4, 6, 7, 8, 9]  # Skip center
        duty_index = palace_sequence.index(duty_chief_palace)

        for i, spirit in enumerate(self.spirit_sequence[1:], 1):  # Skip ZHIFU
            palace_index = (duty_index + i) % 8
            palace_number = palace_sequence[palace_index]
            spirit_positions[palace_number] = spirit

        return spirit_positions

    def create_palace_configuration(self, palace_number: int, lunar_date: LunarDate,
                                    gate: QiMenGate, star: QiMenStar,
                                    spirit: QiMenSpirit) -> QiMenConfiguration:
        """Create complete configuration for one palace"""

        palace = self.nine_palaces.get_palace_by_number(palace_number)

        # Determine heavenly stem and earthly branch for this palace
        # This is a complex calculation based on the time and palace position
        stem_index = (palace_number + lunar_date.day - 1) % 10
        branch_index = (palace_number + lunar_date.hour_branch.hour_range[0] - 1) % 12

        heavenly_stem = self.calendar.heavenly_stems.get_by_index(stem_index)
        earthly_branch = self.calendar.earthly_branches.get_by_index(branch_index)

        # Determine if configuration is auspicious
        is_auspicious = self._evaluate_auspiciousness(gate, star, spirit, palace.element)

        # Get gate attributes
        gate_attr = self.gate_attributes[gate]

        return QiMenConfiguration(
            palace_number=palace_number,
            heavenly_stem=heavenly_stem,
            earthly_branch=earthly_branch,
            gate=gate,
            star=star,
            spirit=spirit,
            element=gate_attr["element"],
            is_auspicious=is_auspicious,
            energy_quality=gate_attr["quality"],
            strategic_application=gate_attr["application"]
        )

    def _evaluate_auspiciousness(self, gate: QiMenGate, star: QiMenStar,
                                 spirit: QiMenSpirit, palace_element: Element) -> bool:
        """Evaluate if a configuration is auspicious"""

        # Basic auspiciousness from gate
        gate_auspicious = gate in self.auspicious_gates

        # Auspicious stars
        auspicious_stars = {QiMenStar.FU, QiMenStar.XIN, QiMenStar.QIN}
        star_auspicious = star in auspicious_stars

        # Auspicious spirits
        auspicious_spirits = {QiMenSpirit.ZHIFU, QiMenSpirit.LIUHE, QiMenSpirit.JIUTIAN}
        spirit_auspicious = spirit in auspicious_spirits

        # Overall evaluation
        return sum([gate_auspicious, star_auspicious, spirit_auspicious]) >= 2

    def analyze_chart_pattern(self, configurations: Dict[int, QiMenConfiguration]) -> str:
        """Analyze overall chart pattern"""

        auspicious_count = sum(1 for config in configurations.values() if config.is_auspicious)
        total_count = len(configurations)

        if auspicious_count >= total_count * 0.7:
            return "Highly Favorable - Multiple auspicious configurations support success"
        elif auspicious_count >= total_count * 0.5:
            return "Moderately Favorable - Balanced energies with good opportunities"
        elif auspicious_count >= total_count * 0.3:
            return "Mixed Pattern - Careful timing and positioning required"
        else:
            return "Challenging Pattern - Significant obstacles require strategic patience"

    def determine_favorable_directions(self, configurations: Dict[int, QiMenConfiguration]) -> Tuple[
        List[Direction], List[Direction]]:
        """Determine favorable and unfavorable directions"""

        favorable = []
        unfavorable = []

        direction_map = {
            1: Direction.NORTH, 2: Direction.SOUTH, 3: Direction.EAST, 4: Direction.SOUTH,
            6: Direction.NORTH, 7: Direction.WEST, 8: Direction.NORTH, 9: Direction.SOUTH
        }

        for palace_num, config in configurations.items():
            if palace_num == 5:  # Skip center
                continue

            direction = direction_map.get(palace_num)
            if direction:
                if config.is_auspicious:
                    if direction not in favorable:
                        favorable.append(direction)
                else:
                    if direction not in unfavorable:
                        unfavorable.append(direction)

        return favorable, unfavorable

    def generate_strategic_assessment(self, configurations: Dict[int, QiMenConfiguration],
                                      duty_chief_palace: int) -> str:
        """Generate strategic assessment"""

        duty_config = configurations[duty_chief_palace]

        assessment_parts = []

        # Duty chief analysis
        if duty_config.is_auspicious:
            assessment_parts.append(f"Command center is favorable in Palace {duty_chief_palace}")
        else:
            assessment_parts.append(f"Command center faces challenges in Palace {duty_chief_palace}")

        # Gate analysis
        assessment_parts.append(
            f"Primary strategy follows {duty_config.gate.value} - {duty_config.strategic_application}")

        # Overall energy
        assessment_parts.append(f"Energy quality: {duty_config.energy_quality}")

        return "; ".join(assessment_parts) + "."

    def calculate_qi_men_chart(self, calculation_time: datetime,
                               time_frame: TimeFrame = TimeFrame.HOUR) -> QiMenChart:
        """Calculate complete Qi Men Dun Jia chart"""

        # Convert to lunar date
        lunar_date = self.calendar.gregorian_to_lunar(calculation_time)

        # Calculate duty chief position
        duty_chief_palace = self.calculate_duty_chief(lunar_date, time_frame)

        # Determine yang/yin time
        is_yang_time = self._is_yang_time(lunar_date)

        # Calculate positions
        gate_positions = self.calculate_gate_positions(duty_chief_palace, is_yang_time)
        star_positions = self.calculate_star_positions(duty_chief_palace, lunar_date)
        spirit_positions = self.calculate_spirit_positions(duty_chief_palace, gate_positions)

        # Create configurations for all palaces
        configurations = {}
        for palace_num in range(1, 10):
            if palace_num == 5:  # Center palace special handling
                configurations[palace_num] = QiMenConfiguration(
                    palace_number=5,
                    heavenly_stem=lunar_date.day_stem,
                    earthly_branch=lunar_date.hour_branch,
                    gate=None,  # No gate in center
                    star=star_positions.get(5, QiMenStar.QIN),
                    spirit=None,  # No spirit in center
                    element=Element.EARTH,
                    is_auspicious=True,
                    energy_quality="Central command, coordination point",
                    strategic_application="Overall coordination and balance"
                )
            else:
                configurations[palace_num] = self.create_palace_configuration(
                    palace_num, lunar_date,
                    gate_positions.get(palace_num, QiMenGate.REST),
                    star_positions.get(palace_num, QiMenStar.PENGBIRD),
                    spirit_positions.get(palace_num, QiMenSpirit.ZHIFU)
                )

        # Analyze chart
        overall_pattern = self.analyze_chart_pattern(configurations)
        favorable_dirs, unfavorable_dirs = self.determine_favorable_directions(configurations)
        strategic_assessment = self.generate_strategic_assessment(configurations, duty_chief_palace)

        # Optimal timing
        optimal_timing = f"Current {time_frame.value} period shows {overall_pattern.split(' - ')[0].lower()} conditions"

        return QiMenChart(
            calculation_time=calculation_time,
            lunar_date=lunar_date,
            time_frame=time_frame,
            duty_chief_palace=duty_chief_palace,
            configurations=configurations,
            overall_pattern=overall_pattern,
            favorable_directions=favorable_dirs,
            unfavorable_directions=unfavorable_dirs,
            optimal_timing=optimal_timing,
            strategic_assessment=strategic_assessment
        )

    def display_qi_men_chart(self, chart: QiMenChart) -> str:
        """Display formatted Qi Men Dun Jia chart"""

        result = f"""
Qi Men Dun Jia Chart - Mysterious Gates Escaping Techniques
{'=' * 70}

Calculation Time: {chart.calculation_time.strftime('%Y-%m-%d %H:%M')}
Lunar Date: Year {chart.lunar_date.year}, Month {chart.lunar_date.month}, Day {chart.lunar_date.day}
Time Frame: {chart.time_frame.value}
Duty Chief Palace: {chart.duty_chief_palace}

Overall Pattern: {chart.overall_pattern}

Palace Configurations:
"""

        # Display in traditional 3x3 grid
        grid_layout = [
            [4, 9, 2],  # Top row
            [3, 5, 7],  # Middle row
            [8, 1, 6]  # Bottom row
        ]

        for row in grid_layout:
            for palace_num in row:
                config = chart.configurations[palace_num]
                if palace_num == 5:
                    result += f"Palace {palace_num} (Center): {config.star.value}\n"
                else:
                    auspicious_mark = "✓" if config.is_auspicious else "✗"
                    result += f"Palace {palace_num} {auspicious_mark}: {config.gate.value} | {config.star.value} | {config.spirit.value}\n"
            result += "\n"

        result += f"""
Strategic Assessment: {chart.strategic_assessment}

Favorable Directions: {', '.join([d.value for d in chart.favorable_directions])}
Unfavorable Directions: {', '.join([d.value for d in chart.unfavorable_directions])}

Optimal Timing: {chart.optimal_timing}
"""

        return result


# Integration example
def integrate_with_existing_framework():
    """Example of how to integrate Qi Men with existing Taiyi system"""

