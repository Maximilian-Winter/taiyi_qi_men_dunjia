# visualizations.py - Chart visualization module for Chinese divination systems

import math
from typing import Dict, List, Tuple, Optional
from datetime import datetime

from .qi_men_dunjia import QiMenChart, QiMenConfiguration
from .taiyi import TaiyiDivination, TaiyiStarPosition
from .core import Direction, Element, TranslationDict


class ChartVisualizer:
    """Main visualization class for divination charts"""
    
    def __init__(self):
        self.translator = TranslationDict()
        
    def render_qimen_ascii(self, chart: QiMenChart, show_stems_branches: bool = False) -> str:
        """Render Qi Men Dun Jia chart in beautiful ASCII format"""
        
        # Grid layout: Traditional Lo Shu arrangement
        grid_layout = [
            [4, 9, 2],  # Top row (SE, S, SW)
            [3, 5, 7],  # Middle row (E, Center, W)  
            [8, 1, 6]   # Bottom row (NE, N, NW)
        ]
        
        result = []
        result.append("+" + "=" * 67 + "+")
        result.append("|                    Qi Men Dun Jia Chart                        |")
        result.append("+" + "=" * 67 + "+")
        result.append(f"| Time: {chart.calculation_time.strftime('%Y-%m-%d %H:%M')}    Duty Chief: Palace {chart.duty_chief_palace}    |")
        result.append("+" + "=" * 67 + "+")
        
        # Create the 3x3 grid
        for row_idx, row in enumerate(grid_layout):
            # Top border of palaces
            if row_idx == 0:
                result.append("║ ┌─────────────────┬─────────────────┬─────────────────┐ ║")
            else:
                result.append("║ ├─────────────────┼─────────────────┼─────────────────┤ ║")
            
            # Palace content - 4 lines per palace for detailed info
            palace_lines = [[], [], [], []]
            
            for col_idx, palace_num in enumerate(row):
                config = chart.configurations[palace_num]
                
                # Line 1: Palace number and auspiciousness
                if palace_num == 5:
                    palace_lines[0].append(f" Palace {palace_num} 中宮  ")
                else:
                    auspicious = "吉" if config.is_auspicious else "凶"
                    palace_lines[0].append(f" Palace {palace_num} {auspicious}   ")
                
                # Line 2: Gate (or center indicator)
                if palace_num == 5:
                    palace_lines[1].append(f" ⚬ CENTER ⚬     ")
                else:
                    gate_short = config.gate.value[:2] if config.gate else "──"
                    palace_lines[1].append(f" 門:{gate_short}         ")
                
                # Line 3: Star
                if config.star:
                    star_short = config.star.value[:2]
                    palace_lines[2].append(f" 星:{star_short}         ")
                else:
                    palace_lines[2].append(" ──────         ")
                
                # Line 4: Spirit
                if palace_num != 5 and config.spirit:
                    spirit_short = config.spirit.value[:2]
                    palace_lines[3].append(f" 神:{spirit_short}         ")
                else:
                    palace_lines[3].append("               ")
            
            # Add the 4 lines for this row of palaces
            for line_set in palace_lines:
                line = "║ │" + "│".join(line_set) + "│ ║"
                result.append(line)
        
        # Bottom border
        result.append("║ └─────────────────┴─────────────────┴─────────────────┘ ║")
        result.append("╠═══════════════════════════════════════════════════════════════════╣")
        
        # Summary information
        result.append(f"║ Pattern: {chart.overall_pattern[:50]:<50} ║")
        result.append(f"║ Favorable: {', '.join([d.value for d in chart.favorable_directions]):<53} ║")
        result.append(f"║ Strategy: {chart.strategic_assessment[:51]:<51} ║")
        result.append("╚═══════════════════════════════════════════════════════════════════╝")
        
        return "\n".join(result)
    
    def render_qimen_detailed(self, chart: QiMenChart) -> str:
        """Render detailed Qi Men chart with full information"""
        
        grid_layout = [
            [4, 9, 2],
            [3, 5, 7], 
            [8, 1, 6]
        ]
        
        result = []
        result.append("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        result.append("┃                           奇門遁甲 QI MEN DUN JIA CHART                              ┃")
        result.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        result.append(f"┃ Time: {chart.calculation_time.strftime('%Y-%m-%d %H:%M')} | Lunar: {chart.lunar_date.year}/{chart.lunar_date.month}/{chart.lunar_date.day} | Duty Chief: Palace {chart.duty_chief_palace} ┃")
        result.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        
        for row_idx, row in enumerate(grid_layout):
            if row_idx > 0:
                result.append("┃ ┠─────────────────────────┼─────────────────────────┼─────────────────────────┨ ┃")
            else:
                result.append("┃ ┌─────────────────────────┬─────────────────────────┬─────────────────────────┐ ┃")
            
            # Create 6 lines per palace for detailed info
            palace_lines = [[] for _ in range(6)]
            
            for palace_num in row:
                config = chart.configurations[palace_num]
                
                if palace_num == 5:
                    # Center palace special formatting
                    palace_lines[0].append(f" Palace 5 - CENTER 中宮  ")
                    palace_lines[1].append(f" {config.star.value:<23}")
                    palace_lines[2].append(f" Earth Element 土       ")
                    palace_lines[3].append(f" Coordination Point     ")
                    palace_lines[4].append(f" {config.heavenly_stem.chinese}{config.earthly_branch.chinese}                   ")
                    palace_lines[5].append(" ─────────────────────── ")
                else:
                    # Regular palace
                    auspicious = "吉 AUSPICIOUS" if config.is_auspicious else "凶 INAUSPICIOUS"
                    palace_lines[0].append(f" Palace {palace_num} - {auspicious:<11}")
                    palace_lines[1].append(f" 門 {config.gate.value:<19}")
                    palace_lines[2].append(f" 星 {config.star.value:<19}")
                    palace_lines[3].append(f" 神 {config.spirit.value:<19}")
                    palace_lines[4].append(f" {config.heavenly_stem.chinese}{config.earthly_branch.chinese} {config.element.value}Element        ")
                    palace_lines[5].append(f" {config.strategic_application[:23]}")
            
            for line_set in palace_lines:
                line = "┃ │" + "│".join(line_set) + "│ ┃"
                result.append(line)
        
        result.append("┃ └─────────────────────────┴─────────────────────────┴─────────────────────────┘ ┃")
        result.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        result.append(f"┃ OVERALL PATTERN: {chart.overall_pattern:<65} ┃")
        result.append(f"┃ FAVORABLE DIRECTIONS: {', '.join([d.value for d in chart.favorable_directions]):<57} ┃")
        result.append(f"┃ UNFAVORABLE DIRECTIONS: {', '.join([d.value for d in chart.unfavorable_directions]):<55} ┃")
        result.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        result.append(f"┃ STRATEGIC ASSESSMENT: {chart.strategic_assessment:<61} ┃")
        result.append("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        
        return "\n".join(result)
    
    def render_taiyi_circular(self, divination: TaiyiDivination) -> str:
        """Render Taiyi chart in circular format showing palace positions and star movements"""
        
        result = []
        result.append("╔═══════════════════════════════════════════════════════════════════╗")
        result.append("║                     太乙神數 TAIYI DIVINE NUMBER                    ║")
        result.append("╠═══════════════════════════════════════════════════════════════════╣")
        result.append(f"║ Query: {divination.query_date.strftime('%Y-%m-%d %H:%M')}   Lunar: {divination.lunar_date.year}/{divination.lunar_date.month}/{divination.lunar_date.day} ║")
        result.append("╠═══════════════════════════════════════════════════════════════════╣")
        
        # Create circular arrangement of palaces
        # Traditional arrangement with 8 palaces around center (palace 5)
        result.append("║                                                                   ║")
        result.append("║                      6(乾)     1(坎)     8(艮)                      ║")
        result.append("║                        ╲        │        ╱                        ║")
        result.append("║                         ╲       │       ╱                         ║")
        result.append("║                          ╲      │      ╱                          ║")
        result.append("║               7(兌) ──────  5(中)  ────── 3(震)                   ║")
        result.append("║                          ╱      │      ╲                          ║")
        result.append("║                         ╱       │       ╲                         ║")
        result.append("║                        ╱        │        ╲                        ║")
        result.append("║                      2(坤)     9(離)     4(巽)                      ║")
        result.append("║                                                                   ║")
        
        # Show star positions
        master_palace = divination.master_star_position.palace.number
        guest_palace = divination.guest_star_position.palace.number
        
        result.append("╠═══════════════════════════════════════════════════════════════════╣")
        result.append("║                          STAR POSITIONS                          ║")
        result.append("╠═══════════════════════════════════════════════════════════════════╣")
        result.append(f"║ 主星 Master Star: {divination.master_star_position.star.value:<10} in Palace {master_palace} ║")
        result.append(f"║ 客星 Guest Star:  {divination.guest_star_position.star.value:<10} in Palace {guest_palace} ║")
        result.append(f"║ 積年 Accumulated Years: {divination.accumulated_years.total_years:<6} Palace: {divination.accumulated_years.palace_position} ║")
        result.append("╠═══════════════════════════════════════════════════════════════════╣")
        
        # Show elemental influences
        result.append("║                       ELEMENTAL INFLUENCES                       ║")
        result.append("╠═══════════════════════════════════════════════════════════════════╣")
        for element, influence in divination.elemental_influences.items():
            bar_length = int(influence * 20)  # Scale to 20 chars
            bar = "█" * bar_length + "░" * (20 - bar_length)
            result.append(f"║ {element.value} {bar} {influence:.2f} ║")
        
        result.append("╠═══════════════════════════════════════════════════════════════════╣")
        result.append("║                      STRATEGIC GUIDANCE                          ║")
        result.append("╠═══════════════════════════════════════════════════════════════════╣")
        
        # Split long guidance into multiple lines
        guidance_lines = self._wrap_text(divination.strategic_guidance, 60)
        for line in guidance_lines:
            result.append(f"║ {line:<65} ║")
        
        result.append("╚═══════════════════════════════════════════════════════════════════╝")
        
        return "\n".join(result)
    
    def render_taiyi_detailed_circular(self, divination: TaiyiDivination) -> str:
        """Render detailed circular Taiyi chart with palace relationships"""
        
        result = []
        result.append("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        result.append("┃                              太乙神數 TAIYI DIVINE NUMBER                              ┃")
        result.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        result.append(f"┃ Query Time: {divination.query_date.strftime('%B %d, %Y at %H:%M')} | Lunar: {divination.lunar_date.year}/{divination.lunar_date.month}/{divination.lunar_date.day} ┃")
        result.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        
        # Detailed circular layout
        result.append("┃                                                                                      ┃")
        result.append("┃           6(乾宮) Northwest            1(坎宮) North            8(艮宮) Northeast      ┃")
        result.append("┃              Heaven                      Water                    Mountain           ┃")
        result.append("┃                 ╲                         │                         ╱               ┃")
        result.append("┃                  ╲                        │                        ╱                ┃")
        result.append("┃                   ╲                       │                       ╱                 ┃")
        result.append("┃  7(兌宮) West ──────╲         5(中宮) CENTER         ╱────── 3(震宮) East           ┃")
        result.append("┃     Lake             ╲          Earth           ╱              Thunder            ┃")
        result.append("┃                       ╲                       ╱                                   ┃")
        result.append("┃                        ╲                     ╱                                    ┃")
        result.append("┃                         ╲                   ╱                                     ┃")
        result.append("┃           2(坤宮) Southwest            9(離宮) South            4(巽宮) Southeast      ┃")
        result.append("┃              Earth                      Fire                     Wind             ┃")
        result.append("┃                                                                                      ┃")
        
        # Mark star positions on the diagram
        master_palace = divination.master_star_position.palace.number
        guest_palace = divination.guest_star_position.palace.number
        
        result.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        result.append("┃                                 STAR POSITIONS                                      ┃")
        result.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        
        # Master star details
        master_star = divination.master_star_position
        result.append(f"┃ ⭐ MASTER STAR: {master_star.star.value} ({self.translator.TAIYI_STARS.get(master_star.star.value, 'Unknown')})")
        result.append(f"┃    Location: Palace {master_palace} - {master_star.palace.chinese_name}")
        result.append(f"┃    Influence: {master_star.influence_strength:.2f} | Quality: {master_star.palace.quality}")
        result.append(f"┃    Strategy: {master_star.palace.strategic_use}")
        result.append("┃")
        
        # Guest star details  
        guest_star = divination.guest_star_position
        result.append(f"┃ 🌟 GUEST STAR: {guest_star.star.value} ({self.translator.TAIYI_STARS.get(guest_star.star.value, 'Unknown')})")
        result.append(f"┃    Location: Palace {guest_palace} - {guest_star.palace.chinese_name}")
        result.append(f"┃    Influence: {guest_star.influence_strength:.2f} | Quality: {guest_star.palace.quality}")
        result.append(f"┃    Strategy: {guest_star.palace.strategic_use}")
        
        result.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        result.append("┃                              PALACE RELATIONSHIPS                                   ┃")
        result.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        
        if divination.supporting_palaces:
            result.append(f"┃ 🤝 SUPPORTING: {', '.join([p.chinese_name for p in divination.supporting_palaces])}")
        if divination.conflicting_palaces:
            result.append(f"┃ ⚔️  CONFLICTING: {', '.join([p.chinese_name for p in divination.conflicting_palaces])}")
        
        result.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        result.append("┃                                TIMING ANALYSIS                                      ┃")
        result.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
        
        for period, analysis in divination.timing_analysis.items():
            result.append(f"┃ {period}: {analysis}")
        
        result.append("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        
        return "\n".join(result)
    
    def render_html_qimen(self, chart: QiMenChart) -> str:
        """Render Qi Men chart as HTML table"""
        
        grid_layout = [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Qi Men Dun Jia Chart - {chart.calculation_time.strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', SimSun, serif; background-color: #f5f5dc; }}
        .chart-container {{ max-width: 800px; margin: 20px auto; }}
        .chart-title {{ text-align: center; font-size: 24px; font-weight: bold; color: #8B4513; margin-bottom: 20px; }}
        .qimen-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; grid-gap: 2px; background-color: #8B4513; border: 3px solid #8B4513; }}
        .palace {{ background-color: white; padding: 15px; min-height: 120px; position: relative; }}
        .palace.center {{ background-color: #fffacd; }}
        .palace.auspicious {{ border-left: 5px solid #228B22; }}
        .palace.inauspicious {{ border-left: 5px solid #DC143C; }}
        .palace-number {{ font-weight: bold; font-size: 14px; color: #8B4513; }}
        .gate {{ color: #DC143C; font-weight: bold; }}
        .star {{ color: #4169E1; font-weight: bold; }}
        .spirit {{ color: #9932CC; font-weight: bold; }}
        .info-panel {{ margin-top: 20px; padding: 15px; background-color: white; border: 1px solid #8B4513; }}
    </style>
</head>
<body>
    <div class="chart-container">
        <div class="chart-title">奇門遁甲 Qi Men Dun Jia Chart</div>
        <div style="text-align: center; margin-bottom: 15px;">
            Time: {chart.calculation_time.strftime('%Y-%m-%d %H:%M')} | 
            Lunar: {chart.lunar_date.year}/{chart.lunar_date.month}/{chart.lunar_date.day} |
            Duty Chief: Palace {chart.duty_chief_palace}
        </div>
        
        <div class="qimen-grid">
"""
        
        for row in grid_layout:
            for palace_num in row:
                config = chart.configurations[palace_num]
                
                if palace_num == 5:
                    # Center palace
                    html += f"""
            <div class="palace center">
                <div class="palace-number">Palace {palace_num} 中宮</div>
                <div class="star">⚬ CENTER ⚬</div>
                <div class="star">{config.star.value if config.star else '天禽'}</div>
                <div style="margin-top: 10px; font-size: 12px;">Coordination Point</div>
            </div>
"""
                else:
                    # Regular palace
                    auspicious_class = "auspicious" if config.is_auspicious else "inauspicious"
                    auspicious_text = "吉" if config.is_auspicious else "凶"
                    
                    html += f"""
            <div class="palace {auspicious_class}">
                <div class="palace-number">Palace {palace_num} {auspicious_text}</div>
                <div class="gate">門: {config.gate.value if config.gate else '──'}</div>
                <div class="star">星: {config.star.value if config.star else '──'}</div>
                <div class="spirit">神: {config.spirit.value if config.spirit else '──'}</div>
                <div style="margin-top: 5px; font-size: 11px;">{config.heavenly_stem.chinese if config.heavenly_stem else ''}
                {config.earthly_branch.chinese if config.earthly_branch else ''}</div>
            </div>
"""
        
        html += f"""
        </div>
        
        <div class="info-panel">
            <h3>Chart Analysis</h3>
            <p><strong>Overall Pattern:</strong> {chart.overall_pattern}</p>
            <p><strong>Favorable Directions:</strong> {', '.join([d.value for d in chart.favorable_directions])}</p>
            <p><strong>Unfavorable Directions:</strong> {', '.join([d.value for d in chart.unfavorable_directions])}</p>
            <p><strong>Strategic Assessment:</strong> {chart.strategic_assessment}</p>
            <p><strong>Optimal Timing:</strong> {chart.optimal_timing}</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def render_html_taiyi(self, divination: TaiyiDivination) -> str:
        """Render Taiyi chart as HTML with circular layout"""
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Taiyi Divine Number - {divination.query_date.strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', SimSun, serif; background-color: #1a1a2e; color: #eee; }}
        .chart-container {{ max-width: 900px; margin: 20px auto; }}
        .chart-title {{ text-align: center; font-size: 28px; font-weight: bold; color: #ffd700; margin-bottom: 20px; }}
        .circular-chart {{ position: relative; width: 500px; height: 500px; margin: 0 auto; }}
        .palace {{ position: absolute; width: 80px; height: 80px; border: 2px solid #ffd700; border-radius: 50%; 
                   background-color: #16213e; display: flex; flex-direction: column; align-items: center; 
                   justify-content: center; font-size: 12px; text-align: center; }}
        .palace.master-star {{ background-color: #ff6b6b; border-color: #ff6b6b; color: white; }}
        .palace.guest-star {{ background-color: #4ecdc4; border-color: #4ecdc4; color: white; }}
        .palace.center {{ width: 100px; height: 100px; background-color: #ffd700; color: #1a1a2e; font-weight: bold; }}
        .star-info {{ margin: 20px 0; padding: 20px; background-color: #16213e; border-radius: 10px; }}
        .element-bar {{ display: flex; align-items: center; margin: 5px 0; }}
        .element-name {{ width: 60px; }}
        .bar {{ height: 20px; background-color: #333; border-radius: 10px; flex-grow: 1; margin: 0 10px; position: relative; }}
        .bar-fill {{ height: 100%; border-radius: 10px; }}
        .wood {{ background-color: #228B22; }}
        .fire {{ background-color: #DC143C; }}
        .earth {{ background-color: #DAA520; }}
        .metal {{ background-color: #C0C0C0; }}
        .water {{ background-color: #4169E1; }}
    </style>
</head>
<body>
    <div class="chart-container">
        <div class="chart-title">太乙神數 Taiyi Divine Number</div>
        <div style="text-align: center; margin-bottom: 30px; font-size: 16px;">
            Query: {divination.query_date.strftime('%B %d, %Y at %H:%M')} | 
            Lunar: {divination.lunar_date.year}/{divination.lunar_date.month}/{divination.lunar_date.day} |
            Accumulated Years: {divination.accumulated_years.total_years}
        </div>
        
        <div class="circular-chart">
            <!-- Center Palace -->
            <div class="palace center" style="top: 210px; left: 210px;">
                <div>中宮</div>
                <div>CENTER</div>
            </div>
"""
        
        # Palace positions in circular arrangement
        palace_positions = {
            1: {"top": "50px", "left": "210px", "name": "坎宮<br>North"},     # North
            2: {"top": "350px", "left": "110px", "name": "坤宮<br>SW"},      # Southwest  
            3: {"top": "210px", "left": "350px", "name": "震宮<br>East"},    # East
            4: {"top": "350px", "left": "310px", "name": "巽宮<br>SE"},      # Southeast
            6: {"top": "50px", "left": "110px", "name": "乾宮<br>NW"},       # Northwest
            7: {"top": "210px", "left": "50px", "name": "兌宮<br>West"},     # West
            8: {"top": "50px", "left": "310px", "name": "艮宮<br>NE"},       # Northeast
            9: {"top": "350px", "left": "210px", "name": "離宮<br>South"}    # South
        }
        
        master_palace = divination.master_star_position.palace.number
        guest_palace = divination.guest_star_position.palace.number
        
        for palace_num, pos in palace_positions.items():
            star_class = ""
            if palace_num == master_palace:
                star_class = "master-star"
            elif palace_num == guest_palace:
                star_class = "guest-star"
                
            html += f"""
            <div class="palace {star_class}" style="top: {pos['top']}; left: {pos['left']};">
                <div>{palace_num}</div>
                <div>{pos['name']}</div>
            </div>
"""
        
        html += f"""
        </div>
        
        <div class="star-info">
            <h3>⭐ Master Star: {divination.master_star_position.star.value}</h3>
            <p>Location: Palace {master_palace} - {divination.master_star_position.palace.chinese_name}</p>
            <p>Influence: {divination.master_star_position.influence_strength:.2f}</p>
            <p>Strategy: {divination.master_star_position.palace.strategic_use}</p>
        </div>
        
        <div class="star-info">
            <h3>🌟 Guest Star: {divination.guest_star_position.star.value}</h3>
            <p>Location: Palace {guest_palace} - {divination.guest_star_position.palace.chinese_name}</p>
            <p>Influence: {divination.guest_star_position.influence_strength:.2f}</p>
            <p>Strategy: {divination.guest_star_position.palace.strategic_use}</p>
        </div>
        
        <div class="star-info">
            <h3>🌟 Elemental Influences</h3>
"""
        
        element_colors = {
            "木": "wood", "火": "fire", "土": "earth", "金": "metal", "水": "water"
        }
        
        for element, influence in divination.elemental_influences.items():
            color_class = element_colors.get(element.value, "")
            percentage = influence * 100
            
            html += f"""
            <div class="element-bar">
                <div class="element-name">{element.value}</div>
                <div class="bar">
                    <div class="bar-fill {color_class}" style="width: {percentage}%;"></div>
                </div>
                <div>{influence:.2f}</div>
            </div>
"""
        
        html += f"""
        </div>
        
        <div class="star-info">
            <h3>🎯 Strategic Guidance</h3>
            <p>{divination.strategic_guidance}</p>
        </div>
        
        <div class="star-info">
            <h3>⏰ Timing Analysis</h3>
"""
        
        for period, analysis in divination.timing_analysis.items():
            html += f"<p><strong>{period}:</strong> {analysis}</p>"
        
        html += """
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Helper function to wrap text to specified width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= width:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines


# Matplotlib support (optional)
def create_matplotlib_qimen(chart: QiMenChart, save_path: Optional[str] = None):
    """Create Qi Men chart using matplotlib (requires matplotlib)"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        from matplotlib.font_manager import FontProperties
        
        # Try to use a Chinese font
        try:
            chinese_font = FontProperties(fname='C:/Windows/Fonts/msyh.ttc')  # Microsoft YaHei
        except:
            chinese_font = FontProperties()
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 3)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Grid layout
        grid_layout = [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]
        
        # Draw grid
        for i in range(4):
            ax.axhline(y=i, color='brown', linewidth=2)
            ax.axvline(x=i, color='brown', linewidth=2)
        
        # Fill palaces
        for row_idx, row in enumerate(grid_layout):
            for col_idx, palace_num in enumerate(row):
                config = chart.configurations[palace_num]
                
                x, y = col_idx, 2 - row_idx  # Flip y-axis for display
                
                # Color based on auspiciousness
                if palace_num == 5:
                    color = 'lightyellow'
                elif config.is_auspicious:
                    color = 'lightgreen'
                else:
                    color = 'lightcoral'
                
                rect = patches.Rectangle((x, y), 1, 1, linewidth=2, 
                                       edgecolor='brown', facecolor=color, alpha=0.7)
                ax.add_patch(rect)
                
                # Add text
                if palace_num == 5:
                    ax.text(x + 0.5, y + 0.5, f'Palace {palace_num}\n中宮\n{config.star.value if config.star else ""}', 
                           ha='center', va='center', fontproperties=chinese_font, fontsize=10)
                else:
                    auspicious = "吉" if config.is_auspicious else "凶"
                    text = f'Palace {palace_num} {auspicious}\n'
                    text += f'門: {config.gate.value[:2] if config.gate else "──"}\n'
                    text += f'星: {config.star.value[:2] if config.star else "──"}\n'
                    text += f'神: {config.spirit.value[:2] if config.spirit else "──"}'
                    
                    ax.text(x + 0.5, y + 0.5, text, ha='center', va='center', 
                           fontproperties=chinese_font, fontsize=8)
        
        plt.title(f'奇門遁甲 Qi Men Dun Jia Chart\n{chart.calculation_time.strftime("%Y-%m-%d %H:%M")}', 
                 fontproperties=chinese_font, fontsize=16, pad=20)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    except ImportError:
        print("Matplotlib not available. Install with: pip install matplotlib")
        return None


def create_matplotlib_taiyi(divination: TaiyiDivination, save_path: Optional[str] = None):
    """Create Taiyi circular chart using matplotlib (requires matplotlib)"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        from matplotlib.font_manager import FontProperties
        import numpy as np
        
        # Try to use a Chinese font
        try:
            chinese_font = FontProperties(fname='C:/Windows/Fonts/msyh.ttc')  # Microsoft YaHei
        except:
            chinese_font = FontProperties()
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Palace positions in circle
        palace_positions = {
            1: (0, 4),      # North
            2: (-3, -3),    # Southwest
            3: (4, 0),      # East
            4: (3, -3),     # Southeast
            5: (0, 0),      # Center
            6: (-3, 3),     # Northwest
            7: (-4, 0),     # West
            8: (3, 3),      # Northeast
            9: (0, -4)      # South
        }
        
        palace_names = {
            1: "坎宮\nNorth", 2: "坤宮\nSW", 3: "震宮\nEast", 4: "巽宮\nSE",
            5: "中宮\nCenter", 6: "乾宮\nNW", 7: "兌宮\nWest", 8: "艮宮\nNE", 9: "離宮\nSouth"
        }
        
        master_palace = divination.master_star_position.palace.number
        guest_palace = divination.guest_star_position.palace.number
        
        # Draw palaces
        for palace_num, (x, y) in palace_positions.items():
            if palace_num == 5:
                # Center palace
                circle = patches.Circle((x, y), 0.8, color='gold', alpha=0.8)
                ax.add_patch(circle)
                ax.text(x, y, palace_names[palace_num], ha='center', va='center', 
                       fontproperties=chinese_font, fontsize=12, weight='bold')
            else:
                # Outer palaces
                if palace_num == master_palace:
                    color = 'red'
                    alpha = 0.9
                elif palace_num == guest_palace:
                    color = 'blue'
                    alpha = 0.9
                else:
                    color = 'lightblue'
                    alpha = 0.6
                
                circle = patches.Circle((x, y), 0.6, color=color, alpha=alpha)
                ax.add_patch(circle)
                ax.text(x, y, f'{palace_num}\n{palace_names[palace_num]}', ha='center', va='center', 
                       fontproperties=chinese_font, fontsize=10)
        
        # Draw connections
        center = palace_positions[5]
        for palace_num, (x, y) in palace_positions.items():
            if palace_num != 5:
                ax.plot([center[0], x], [center[1], y], 'k-', alpha=0.3, linewidth=1)
        
        # Add star information
        title_text = f'太乙神數 Taiyi Divine Number\n{divination.query_date.strftime("%Y-%m-%d %H:%M")}'
        plt.title(title_text, fontproperties=chinese_font, fontsize=16, pad=20)
        
        # Add legend
        legend_text = f'⭐ Master Star: {divination.master_star_position.star.value} (Palace {master_palace})\n'
        legend_text += f'🌟 Guest Star: {divination.guest_star_position.star.value} (Palace {guest_palace})\n'
        legend_text += f'積年: {divination.accumulated_years.total_years} years'
        
        ax.text(-5.5, 5.5, legend_text, fontproperties=chinese_font, fontsize=10, 
               bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.8))
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    except ImportError:
        print("Matplotlib not available. Install with: pip install matplotlib")
        return None