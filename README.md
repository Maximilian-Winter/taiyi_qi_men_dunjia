# Taiyi Qi Men Dunjia - Chinese Divination Framework

A comprehensive Python implementation of traditional Chinese divination systems, featuring an astronomically accurate lunisolar calendar and two major divination methods: **Taiyi Shenshu** (太乙神数) and **Qi Men Dun Jia** (奇門遁甲).

## 🌟 Overview

This framework provides a complete computational foundation for Chinese metaphysical sciences, combining:

- **Astronomical Calculations**: Precise lunisolar calendar with actual lunar phases and solar terms
- **Taiyi Divine Number**: A sophisticated astrological system for strategic guidance
- **Qi Men Dun Jia**: The "Mysterious Gates Escaping Techniques" for tactical decision-making
- **I Ching Trigrams**: Complete Eight Trigrams and Nine Palaces system
- **Four Pillars**: Comprehensive temporal analysis using Heavenly Stems and Earthly Branches

## 📁 Project Structure

```
taiyi_qi_men_dunjia/
├── divination/
│   ├── __init__.py           # Package initialization
│   ├── core.py              # Core enums and translation dictionaries
│   ├── calendar.py          # Lunisolar calendar and Four Pillars system
│   ├── trigrams.py          # Eight Trigrams and Nine Palaces
│   ├── taiyi.py            # Taiyi Shenshu divination system
│   └── qi_men_dunjia.py    # Qi Men Dun Jia system
└── example.py              # Usage examples
```

## ✨ Features

### 🗓️ Chinese Lunisolar Calendar (`calendar.py`)
- **Astronomical Accuracy**: Uses Jean Meeus algorithms for lunar phases and solar terms
- **Heavenly Stems & Earthly Branches**: Complete sexagenary cycle calculations
- **Four Pillars Analysis**: Year, Month, Day, and Hour pillar generation
- **Leap Month Detection**: Automatic identification of intercalary months
- **Element Analysis**: Five Element composition and balance assessment
- **Time-based Recommendations**: Strategic guidance based on temporal energies

**Key Classes:**
- `ChineseLunarCalendar`: Main conversion and calculation engine
- `HeavenlyStem` / `EarthlyBranch`: Detailed stem/branch attributes with strategic applications
- `LunarDate`: Complete lunar date representation with all four pillars

### 🏛️ Trigrams & Nine Palaces (`trigrams.py`)
- **Eight Trigrams**: Complete I Ching trigram system with metaphysical attributes
- **Nine Palaces**: Lo Shu square-based palace system
- **Visual Representation**: Unicode trigram symbols and ASCII art
- **Strategic Applications**: Cultivation practices and strategic uses for each trigram/palace
- **Elemental Correspondences**: Five Element associations and directional mappings

**Key Classes:**
- `EightTrigrams`: Container for all eight trigrams with lookup methods
- `NinePalaces`: Complete Nine Palaces system with Lo Shu integration
- `Palace`: Individual palace with cosmic functions and energy characteristics

### ⭐ Taiyi Divine Number (`taiyi.py`)
A sophisticated astrological system for strategic planning and life guidance.

**Core Concepts:**
- **Accumulated Years Calculation**: 72-year Taiyi cycles with palace positioning
- **Master & Guest Stars**: Dual star system for comprehensive analysis
- **Palace Relationships**: Supporting and conflicting palace dynamics
- **Elemental Influences**: Five Element strength calculations
- **Strategic Guidance**: Actionable recommendations based on star positions

**Key Classes:**
- `TaiyiCalculator`: Main calculation engine
- `TaiyiDivination`: Complete divination result with assessments
- `TaiyiStarPosition`: Star placement with influence calculations

**Example Output:**
```
Master star 太乙 resides in 坎宮, with strong influence
Guest star 大德 resides in 離宮, with moderate influence
Palace positions provide mutual support, creating favorable circumstances
```

### 🎯 Qi Men Dun Jia (`qi_men_dunjia.py`)
The "Mysterious Gates Escaping Techniques" - a tactical divination system for timing and positioning.

**Core Components:**
- **Eight Gates**: Strategic gates (休門, 生門, 傷門, etc.) with tactical applications
- **Nine Stars**: Celestial influences (天蓬, 天任, 天沖, etc.)
- **Eight Spirits**: Divine entities governing different aspects
- **Duty Chief Calculation**: Dynamic palace positioning based on time
- **Yang/Yin Time Cycles**: Seasonal movement patterns

**Key Classes:**
- `QiMenCalculator`: Complete chart calculation system
- `QiMenChart`: Full chart with all palace configurations
- `QiMenConfiguration`: Individual palace setup with gates, stars, and spirits

**Chart Layout Example:**
```
Palace 4 ✓: 休門 | 天蓬 | 太陰    Palace 9 ✗: 生門 | 天任 | 騰蛇    Palace 2 ✓: 傷門 | 天沖 | 六合
Palace 3 ✗: 杜門 | 天輔 | 白虎    Palace 5 (Center): 天禽         Palace 7 ✓: 景門 | 天英 | 玄武
Palace 8 ✓: 死門 | 天芮 | 九地    Palace 1 ✗: 驚門 | 天柱 | 九天    Palace 6 ✓: 開門 | 天心 | 值符
```

## 🚀 Quick Start

### Basic Usage

```python
import datetime
from divination.taiyi import TaiyiCalculator
from divination.qi_men_dunjia import QiMenCalculator

# Initialize calculators
taiyi = TaiyiCalculator()
qimen = QiMenCalculator()

# Perform Taiyi divination
current_time = datetime.datetime.now()
taiyi_result = taiyi.perform_divination(current_time)
print(taiyi.display_divination_result(taiyi_result))

# Calculate Qi Men chart
qimen_chart = qimen.calculate_qi_men_chart(current_time)
print(qimen.display_qi_men_chart(qimen_chart))
```

### Calendar Conversion

```python
from divination.calendar import ChineseLunarCalendar

calendar = ChineseLunarCalendar()

# Convert Gregorian to Lunar
gregorian_date = datetime.datetime(2024, 7, 13, 15, 30)
lunar_date = calendar.gregorian_to_lunar(gregorian_date)

print(f"Lunar Date: Year {lunar_date.year}, Month {lunar_date.month}, Day {lunar_date.day}")
print(f"Four Pillars: {lunar_date.year_stem}{lunar_date.year_branch} | "
      f"{lunar_date.month_stem}{lunar_date.month_branch} | "
      f"{lunar_date.day_stem}{lunar_date.day_branch} | "
      f"{lunar_date.hour_stem}{lunar_date.hour_branch}")

# Get detailed analysis
analysis = calendar.analyze_lunar_date(lunar_date)
print(f"Elemental composition: {analysis['elemental_composition']['element_distribution']}")
```

## 🔬 Technical Details

### Dependencies
- **Python 3.7+** (tested with Python 3.13.2)
- **Standard Library Only**: No external dependencies required
  - `datetime`, `math`, `enum`, `typing`, `dataclasses`

### Astronomical Algorithms
- **Lunar Calculations**: Jean Meeus's "Astronomical Algorithms" for new moon timing
- **Solar Terms**: Precise solar longitude calculations for 24 solar terms
- **Julian Day Conversion**: High-precision date conversion system
- **Leap Month Detection**: Traditional Chinese algorithm based on solar term distribution

### Calculation Methods

#### Taiyi System
1. **Accumulated Years**: `(target_year - 1864) % 72` with 8-palace cycle
2. **Master Star**: Based on year stem with monthly/daily adjustments
3. **Guest Star**: Dynamic calculation using day branch and hour
4. **Palace Relationships**: Five Element generation/destruction cycles
5. **Influence Strength**: Elemental harmony calculations (0.0-1.0 scale)

#### Qi Men Dun Jia
1. **Duty Chief**: Complex formula using day stem, hour branch, and time frame
2. **Gate Arrangement**: Sequential placement starting from duty chief position
3. **Star Distribution**: Time-based rotation with 9-star cycle
4. **Spirit Assignment**: Hierarchical placement following traditional patterns
5. **Auspiciousness**: Multi-factor evaluation of gate/star/spirit combinations

## 📊 Output Examples

### Taiyi Divine Calculation
```
Taiyi Divine Calculation Result
==================================================

Query Time: July 13, 2024 at 15:30
Lunar Time: Year 2024, Month 6, Day 8

Accumulated Years Calculation:
Accumulated Years: 160, Cycles: 2, Remainder: 16, Palace Position: 3

Star Position Analysis:
太乙 (Master Star) resides in 震宮
大德 (Guest Star) resides in 離宮

Active Palace: 震宮 - Sudden breakthrough, initiating movement, shocking action

Supporting Palaces: 巽宮, 離宮
Conflicting Palaces: 坤宮, 兌宮

Elemental Influences:
  木: 0.55
  火: 0.45
  土: 0.15
  金: 0.10
  水: 0.25

Strategic Guidance:
Primary strategy: Breakthrough moments, initiating new phases, overcoming stagnation;
Supporting strategy: Brilliant manifestation, clear communication, inspiring others;
Elemental guidance: Initiation, new projects, creative breakthrough.
```

### Qi Men Dun Jia Chart
```
Qi Men Dun Jia Chart - Mysterious Gates Escaping Techniques
======================================================================

Calculation Time: 2024-07-13 15:30
Lunar Date: Year 2024, Month 6, Day 8
Time Frame: 時家
Duty Chief Palace: 1

Overall Pattern: Moderately Favorable - Balanced energies with good opportunities

Palace Configurations:
Palace 4 ✓: 休門 | 天蓬 | 太陰
Palace 9 ✗: 生門 | 天任 | 騰蛇  
Palace 2 ✓: 傷門 | 天沖 | 六合

Palace 3 ✗: 杜門 | 天輔 | 白虎
Palace 5 (Center): 天禽
Palace 7 ✓: 景門 | 天英 | 玄武

Palace 8 ✓: 死門 | 天芮 | 九地
Palace 1 ✗: 驚門 | 天柱 | 九天
Palace 6 ✓: 開門 | 天心 | 值符

Strategic Assessment: Command center faces challenges in Palace 1; Primary strategy follows 驚門 - Surprising enemies, emergency action; Energy quality: Sudden change and alarm, unexpected events.

Favorable Directions: 北, 西
Unfavorable Directions: 南, 東

Optimal Timing: Current 時家 period shows moderately favorable conditions
```

## 🎯 Applications

### Strategic Planning
- **Business Decisions**: Timing for launches, negotiations, investments
- **Personal Development**: Optimal timing for major life changes
- **Project Management**: Phase timing and resource allocation

### Academic Research
- **Chinese Studies**: Authentic implementation of traditional systems
- **Computational Archaeology**: Historical date verification and analysis
- **Cultural Preservation**: Digital preservation of ancient knowledge

### Software Integration
- **Modular Design**: Easy integration into larger applications
- **API-Ready**: Clean interfaces for web service development
- **Educational Tools**: Foundation for teaching Chinese metaphysics

## 🏛️ Cultural Context

### Historical Background
- **Taiyi Shenshu**: Imperial divination system used by Chinese dynasties
- **Qi Men Dun Jia**: Military strategy system attributed to the Yellow Emperor
- **Astronomical Heritage**: Continuation of 4000+ years of Chinese astronomy

### Philosophical Foundations
- **Yin-Yang Theory**: Fundamental polarity principles
- **Five Elements**: Wood, Fire, Earth, Metal, Water transformation cycles
- **Heavenly Stems & Earthly Branches**: 60-year cycles of cosmic influence
- **I Ching Integration**: Trigram-based analysis and interpretation

## 🔮 Advanced Features

### Temporal Analysis
- **Multi-timeframe Calculations**: Year, month, day, and hour-based charts
- **Seasonal Adjustments**: Automatic yang/yin time detection
- **Cyclical Patterns**: 60-year, 72-year, and other traditional cycles

### Elemental Dynamics
- **Generation Cycles**: Wood→Fire→Earth→Metal→Water→Wood
- **Destruction Cycles**: Wood destroys Earth, Earth destroys Water, etc.
- **Balance Assessment**: Automatic detection of elemental imbalances
- **Remedial Suggestions**: Strategic recommendations for elemental harmony

### Palace Relationships
- **Supporting Networks**: Identification of mutually beneficial palace configurations
- **Conflict Resolution**: Analysis of opposing forces and mitigation strategies
- **Energy Flow**: Understanding of cosmic energy circulation patterns

## 🛠️ Extension Points

The framework is designed for extensibility:

### Adding New Divination Systems
```python
from divination.core import Element, Direction
from divination.calendar import ChineseLunarCalendar

class NewDivinationSystem:
    def __init__(self):
        self.calendar = ChineseLunarCalendar()
    
    def calculate(self, date):
        lunar_date = self.calendar.gregorian_to_lunar(date)
        # Implement your system here
        return result
```

### Custom Translation Systems
- Extend `TranslationDict` in `core.py` for additional languages
- Add cultural-specific interpretations and meanings
- Implement region-specific calculation variations

### Integration with Modern APIs
- Weather correlation with elemental influences
- Astronomical event integration
- Geographic location adjustments

## 📚 Further Reading

### Classical Texts
- **太乙神数** (Taiyi Shenshu): Ancient astrological manual
- **奇門遁甲** (Qi Men Dun Jia): Strategic divination classic  
- **易經** (I Ching): Book of Changes and trigram theory
- **干支历** (Ganzhi Calendar): Stem-branch calendar system

### Modern References
- Jean Meeus: "Astronomical Algorithms" (lunar/solar calculations)
- Joseph Needham: "Science and Civilisation in China" (historical context)
- Ho Peng Yoke: "Chinese Mathematical Astrology" (computational methods)

## 💡 Contributing

This implementation represents a faithful computational translation of traditional Chinese divination systems. Contributions should maintain:

- **Historical Accuracy**: Adherence to classical calculation methods
- **Cultural Sensitivity**: Respectful treatment of sacred knowledge
- **Technical Excellence**: Clean, well-documented code
- **Educational Value**: Clear explanations and examples

## 📄 License

This project preserves and digitizes traditional Chinese cultural knowledge for educational and research purposes. Please use responsibly and with appropriate cultural sensitivity.

---

*"The sage is guided by what he feels and not by what he sees."* - I Ching

**Note**: This software is for educational and cultural preservation purposes. While the calculations are mathematically accurate, divination results should be considered as philosophical and cultural insights rather than absolute predictions.