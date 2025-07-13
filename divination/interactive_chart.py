# interactive_charts.py - Interactive Chart System for Chinese Divination

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
import math

from .qi_men_dunjia import QiMenChart, QiMenCalculator, QiMenConfiguration, TimeFrame
from .taiyi import TaiyiDivination, TaiyiCalculator
from .core import Element, Direction, TranslationDict
from .visualizations import ChartVisualizer


@dataclass
class InteractionEvent:
    """Represents a user interaction with the chart"""
    event_type: str  # 'click', 'hover', 'time_change', 'query'
    target: str  # 'palace_1', 'star_position', 'time_slider'
    data: Dict[str, Any]
    timestamp: datetime


@dataclass
class ChartState:
    """Maintains the current state of interactive chart"""
    current_time: datetime
    selected_palace: Optional[int]
    hover_palace: Optional[int]
    time_range_start: datetime
    time_range_end: datetime
    animation_speed: float
    show_predictions: bool
    comparison_time: Optional[datetime]
    user_query: str
    interaction_history: List[InteractionEvent]


class InteractiveQiMenChart:
    """Interactive Qi Men Dun Jia chart with real-time updates and user interaction"""

    def __init__(self, initial_time: datetime = None):
        self.calculator = QiMenCalculator()
        self.visualizer = ChartVisualizer()
        self.translator = TranslationDict()

        self.initial_time = initial_time or datetime.now()
        self.state = ChartState(
            current_time=self.initial_time,
            selected_palace=None,
            hover_palace=None,
            time_range_start=self.initial_time - timedelta(hours=12),
            time_range_end=self.initial_time + timedelta(hours=12),
            animation_speed=1.0,
            show_predictions=False,
            comparison_time=None,
            user_query="",
            interaction_history=[]
        )

        self.current_chart = self.calculator.calculate_qi_men_chart(self.initial_time)
        self.cached_charts = {}  # Cache for performance

        # Event handlers
        self.event_handlers = {
            'palace_click': self._handle_palace_click,
            'palace_hover': self._handle_palace_hover,
            'time_change': self._handle_time_change,
            'animation_toggle': self._handle_animation_toggle,
            'comparison_mode': self._handle_comparison_mode,
            'query_submit': self._handle_query_submit
        }

    def _handle_palace_click(self, palace_number: int, event_data: Dict) -> Dict:
        """Handle palace click interaction"""
        self.state.selected_palace = palace_number
        config = self.current_chart.configurations[palace_number]

        # Log interaction
        self._log_interaction('palace_click', f'palace_{palace_number}', {
            'palace_number': palace_number,
            'configuration': asdict(config)
        })

        # Generate detailed analysis
        analysis = self._generate_palace_analysis(palace_number, config)

        return {
            'action': 'palace_selected',
            'palace_number': palace_number,
            'analysis': analysis,
            'recommendations': self._generate_palace_recommendations(config),
            'related_palaces': self._find_related_palaces(palace_number),
            'timing_advice': self._generate_timing_advice(config)
        }

    def _handle_palace_hover(self, palace_number: int, event_data: Dict) -> Dict:
        """Handle palace hover interaction"""
        self.state.hover_palace = palace_number
        config = self.current_chart.configurations[palace_number]

        return {
            'action': 'palace_hover',
            'palace_number': palace_number,
            'quick_info': {
                'gate': config.gate.value if config.gate else "Center",
                'star': config.star.value if config.star else "",
                'spirit': config.spirit.value if config.spirit else "",
                'auspicious': config.is_auspicious,
                'energy': config.energy_quality,
                'element': config.element.value
            },
            'tooltip_html': self._generate_tooltip_html(config)
        }

    def _handle_time_change(self, new_time: datetime, event_data: Dict) -> Dict:
        """Handle time slider change"""
        old_time = self.state.current_time
        self.state.current_time = new_time

        # Calculate new chart
        new_chart = self._get_cached_chart(new_time)

        # Analyze changes
        changes = self._analyze_chart_changes(self.current_chart, new_chart)

        self.current_chart = new_chart

        self._log_interaction('time_change', 'time_slider', {
            'old_time': old_time.isoformat(),
            'new_time': new_time.isoformat(),
            'changes': changes
        })

        return {
            'action': 'chart_updated',
            'new_chart': self._serialize_chart(new_chart),
            'changes': changes,
            'animation_data': self._generate_animation_data(changes)
        }

    def _handle_animation_toggle(self, event_data: Dict) -> Dict:
        """Handle animation controls"""
        action = event_data.get('action', 'play')

        if action == 'play':
            return self._start_time_animation()
        elif action == 'pause':
            return self._pause_animation()
        elif action == 'speed_change':
            self.state.animation_speed = event_data.get('speed', 1.0)
            return {'action': 'speed_updated', 'speed': self.state.animation_speed}

    def _handle_comparison_mode(self, comparison_time: datetime, event_data: Dict) -> Dict:
        """Handle side-by-side comparison mode"""
        self.state.comparison_time = comparison_time

        current_chart = self.current_chart
        comparison_chart = self._get_cached_chart(comparison_time)

        comparison_analysis = self._compare_charts(current_chart, comparison_chart)

        return {
            'action': 'comparison_ready',
            'current_chart': self._serialize_chart(current_chart),
            'comparison_chart': self._serialize_chart(comparison_chart),
            'analysis': comparison_analysis,
            'differences': self._highlight_differences(current_chart, comparison_chart)
        }

    def _handle_query_submit(self, query: str, event_data: Dict) -> Dict:
        """Handle specific divination query"""
        self.state.user_query = query

        # Analyze chart in context of query
        query_analysis = self._analyze_for_query(query, self.current_chart)

        # Generate targeted recommendations
        recommendations = self._generate_query_recommendations(query, self.current_chart)

        # Find optimal timing
        optimal_times = self._find_optimal_times_for_query(query)

        self._log_interaction('query_submit', 'query_form', {
            'query': query,
            'analysis_type': query_analysis['type'],
            'recommendations_count': len(recommendations)
        })

        return {
            'action': 'query_analyzed',
            'query': query,
            'analysis': query_analysis,
            'recommendations': recommendations,
            'optimal_times': optimal_times,
            'relevant_palaces': query_analysis['relevant_palaces']
        }

    def _generate_palace_analysis(self, palace_number: int, config: QiMenConfiguration) -> Dict:
        """Generate detailed palace analysis"""
        palace = self.calculator.nine_palaces.get_palace_by_number(palace_number)

        analysis = {
            'basic_info': {
                'number': palace_number,
                'chinese_name': palace.chinese_name if palace else f"Palace {palace_number}",
                'direction': palace.direction.value if palace else "Center",
                'element': config.element.value,
                'is_auspicious': config.is_auspicious
            },
            'configuration': {
                'gate': {
                    'chinese': config.gate.value if config.gate else "无门",
                    'english': self.translator.EIGHT_GATES.get(config.gate.value,
                                                               "No Gate") if config.gate else "No Gate",
                    'quality': config.energy_quality,
                    'application': config.strategic_application
                },
                'star': {
                    'chinese': config.star.value if config.star else "",
                    'english': self.translator.DUNJIA_STARS.get(config.star.value, "") if config.star else "",
                    'influence': self._calculate_star_influence(config.star)
                },
                'spirit': {
                    'chinese': config.spirit.value if config.spirit else "",
                    'english': self.translator.EIGHT_SPIRITS.get(config.spirit.value, "") if config.spirit else "",
                    'meaning': self._get_spirit_meaning(config.spirit)
                }
            },
            'stems_branches': {
                'heavenly_stem': {
                    'chinese': config.heavenly_stem.chinese,
                    'element': config.heavenly_stem.element.value,
                    'polarity': config.heavenly_stem.polarity.value,
                    'description': config.heavenly_stem.description
                },
                'earthly_branch': {
                    'chinese': config.earthly_branch.chinese,
                    'zodiac': config.earthly_branch.zodiac_english,
                    'time_period': config.earthly_branch.time_period,
                    'energy_quality': config.earthly_branch.energy_quality
                }
            },
            'elemental_relationships': self._analyze_elemental_relationships(config),
            'temporal_influences': self._analyze_temporal_influences(palace_number)
        }

        return analysis

    def _generate_palace_recommendations(self, config: QiMenConfiguration) -> List[Dict]:
        """Generate specific recommendations for palace configuration"""
        recommendations = []

        if config.is_auspicious:
            recommendations.extend([
                {
                    'type': 'action',
                    'priority': 'high',
                    'title': 'Favorable Action Window',
                    'description': f'This palace shows auspicious energy. {config.strategic_application}',
                    'timing': 'Act within the next 2 hours for maximum benefit'
                },
                {
                    'type': 'strategy',
                    'priority': 'medium',
                    'title': 'Strategic Approach',
                    'description': f'Energy quality: {config.energy_quality}',
                    'timing': 'Plan major initiatives during this period'
                }
            ])
        else:
            recommendations.extend([
                {
                    'type': 'caution',
                    'priority': 'high',
                    'title': 'Exercise Caution',
                    'description': 'This palace shows challenging energy. Avoid major decisions.',
                    'timing': 'Wait for more favorable timing'
                },
                {
                    'type': 'alternative',
                    'priority': 'medium',
                    'title': 'Alternative Approach',
                    'description': f'Consider indirect methods. {config.strategic_application}',
                    'timing': 'Use this time for preparation and planning'
                }
            ])

        # Add element-specific recommendations
        element_advice = self._get_element_advice(config.element)
        recommendations.append({
            'type': 'elemental',
            'priority': 'medium',
            'title': f'{config.element.value} Element Guidance',
            'description': element_advice,
            'timing': 'Integrate this elemental approach throughout the day'
        })

        return recommendations

    def _find_related_palaces(self, palace_number: int) -> List[Dict]:
        """Find palaces with related energies"""
        current_config = self.current_chart.configurations[palace_number]
        related = []

        for num, config in self.current_chart.configurations.items():
            if num == palace_number:
                continue

            relationship_strength = 0
            relationship_type = []

            # Same element
            if config.element == current_config.element:
                relationship_strength += 0.8
                relationship_type.append('same_element')

            # Complementary gates
            if self._are_complementary_gates(current_config.gate, config.gate):
                relationship_strength += 0.6
                relationship_type.append('complementary_gates')

            # Star relationships
            if self._have_star_relationship(current_config.star, config.star):
                relationship_strength += 0.5
                relationship_type.append('star_harmony')

            if relationship_strength > 0.5:
                related.append({
                    'palace_number': num,
                    'relationship_strength': relationship_strength,
                    'relationship_types': relationship_type,
                    'description': self._describe_relationship(relationship_type)
                })

        return sorted(related, key=lambda x: x['relationship_strength'], reverse=True)[:3]

    def _generate_timing_advice(self, config: QiMenConfiguration) -> Dict:
        """Generate timing advice for palace configuration"""
        current_hour = self.state.current_time.hour

        # Find optimal hours based on configuration
        optimal_hours = []
        avoid_hours = []

        if config.is_auspicious:
            # Current hour and next 2 hours are good
            for i in range(3):
                hour = (current_hour + i) % 24
                optimal_hours.append({
                    'hour': hour,
                    'period': self._get_time_period_name(hour),
                    'strength': 1.0 - (i * 0.2),
                    'reason': f'Auspicious palace energy peaks during this time'
                })
        else:
            # Find better hours
            for i in range(1, 13):  # Check next 12 hours
                future_time = self.state.current_time + timedelta(hours=i)
                future_chart = self._get_cached_chart(future_time)
                future_config = future_chart.configurations[config.palace_number]

                if future_config.is_auspicious:
                    optimal_hours.append({
                        'hour': future_time.hour,
                        'period': self._get_time_period_name(future_time.hour),
                        'strength': 0.8,
                        'reason': f'Palace becomes auspicious in {i} hours'
                    })
                    break

        return {
            'optimal_hours': optimal_hours,
            'avoid_hours': avoid_hours,
            'current_assessment': 'favorable' if config.is_auspicious else 'challenging',
            'next_change': self._predict_next_change(config.palace_number)
        }

    def _generate_tooltip_html(self, config: QiMenConfiguration) -> str:
        """Generate HTML tooltip for palace hover"""
        auspicious_class = 'auspicious' if config.is_auspicious else 'inauspicious'
        auspicious_text = '吉 Auspicious' if config.is_auspicious else '凶 Inauspicious'

        html = f"""
        <div class="palace-tooltip {auspicious_class}">
            <div class="tooltip-header">
                <span class="palace-number">Palace {config.palace_number}</span>
                <span class="auspicious-indicator">{auspicious_text}</span>
            </div>
            <div class="tooltip-content">
                <div class="config-line">
                    <span class="label">門 Gate:</span>
                    <span class="value">{config.gate.value if config.gate else "Center"}</span>
                </div>
                <div class="config-line">
                    <span class="label">星 Star:</span>
                    <span class="value">{config.star.value if config.star else ""}</span>
                </div>
                <div class="config-line">
                    <span class="label">神 Spirit:</span>
                    <span class="value">{config.spirit.value if config.spirit else ""}</span>
                </div>
                <div class="config-line">
                    <span class="label">Element:</span>
                    <span class="value">{config.element.value}</span>
                </div>
                <div class="energy-quality">
                    {config.energy_quality}
                </div>
            </div>
            <div class="tooltip-footer">
                Click for detailed analysis
            </div>
        </div>
        """
        return html

    def _get_cached_chart(self, time: datetime) -> QiMenChart:
        """Get chart from cache or calculate new one"""
        time_key = time.strftime('%Y%m%d%H')

        if time_key not in self.cached_charts:
            self.cached_charts[time_key] = self.calculator.calculate_qi_men_chart(time)

            # Limit cache size
            if len(self.cached_charts) > 100:
                oldest_key = min(self.cached_charts.keys())
                del self.cached_charts[oldest_key]

        return self.cached_charts[time_key]

    def _analyze_chart_changes(self, old_chart: QiMenChart, new_chart: QiMenChart) -> Dict:
        """Analyze changes between two charts"""
        changes = {
            'duty_chief_moved': old_chart.duty_chief_palace != new_chart.duty_chief_palace,
            'palace_changes': {},
            'overall_pattern_change': old_chart.overall_pattern != new_chart.overall_pattern,
            'significant_changes': []
        }

        for palace_num in range(1, 10):
            old_config = old_chart.configurations[palace_num]
            new_config = new_chart.configurations[palace_num]

            palace_changes = {
                'auspiciousness_changed': old_config.is_auspicious != new_config.is_auspicious,
                'gate_changed': old_config.gate != new_config.gate,
                'star_changed': old_config.star != new_config.star,
                'spirit_changed': old_config.spirit != new_config.spirit
            }

            if any(palace_changes.values()):
                changes['palace_changes'][palace_num] = palace_changes

                if palace_changes['auspiciousness_changed']:
                    changes['significant_changes'].append({
                        'type': 'auspiciousness_flip',
                        'palace': palace_num,
                        'from': 'auspicious' if old_config.is_auspicious else 'inauspicious',
                        'to': 'auspicious' if new_config.is_auspicious else 'inauspicious'
                    })

        return changes

    def _generate_animation_data(self, changes: Dict) -> Dict:
        """Generate data for smooth chart transitions"""
        animations = []

        # Duty chief movement
        if changes['duty_chief_moved']:
            animations.append({
                'type': 'duty_chief_move',
                'duration': 1000,  # milliseconds
                'easing': 'ease-in-out'
            })

        # Palace changes
        for palace_num, palace_changes in changes['palace_changes'].items():
            if palace_changes['auspiciousness_changed']:
                animations.append({
                    'type': 'auspiciousness_change',
                    'target': f'palace_{palace_num}',
                    'duration': 500,
                    'easing': 'ease'
                })

            if palace_changes['gate_changed']:
                animations.append({
                    'type': 'gate_change',
                    'target': f'palace_{palace_num}',
                    'duration': 800,
                    'easing': 'ease-in-out'
                })

        return {
            'animations': animations,
            'total_duration': max([a['duration'] for a in animations]) if animations else 0
        }

    def _serialize_chart(self, chart: QiMenChart) -> Dict:
        """Serialize chart for JSON transmission"""
        return {
            'calculation_time': chart.calculation_time.isoformat(),
            'duty_chief_palace': chart.duty_chief_palace,
            'overall_pattern': chart.overall_pattern,
            'favorable_directions': [d.value for d in chart.favorable_directions],
            'unfavorable_directions': [d.value for d in chart.unfavorable_directions],
            'configurations': {
                str(num): {
                    'palace_number': config.palace_number,
                    'gate': config.gate.value if config.gate else None,
                    'star': config.star.value if config.star else None,
                    'spirit': config.spirit.value if config.spirit else None,
                    'element': config.element.value,
                    'is_auspicious': config.is_auspicious,
                    'energy_quality': config.energy_quality,
                    'strategic_application': config.strategic_application,
                    'heavenly_stem': config.heavenly_stem.chinese if config.heavenly_stem else None,
                    'earthly_branch': config.earthly_branch.chinese if config.earthly_branch else None
                }
                for num, config in chart.configurations.items()
            }
        }

    def _log_interaction(self, event_type: str, target: str, data: Dict):
        """Log user interaction for analytics"""
        event = InteractionEvent(
            event_type=event_type,
            target=target,
            data=data,
            timestamp=datetime.now()
        )
        self.state.interaction_history.append(event)

        # Keep only last 100 interactions
        if len(self.state.interaction_history) > 100:
            self.state.interaction_history = self.state.interaction_history[-100:]

    def generate_interactive_html(self) -> str:
        """Generate complete interactive HTML interface"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Interactive Qi Men Dun Jia Chart</title>
    <style>
        {self._get_interactive_css()}
    </style>
</head>
<body>
    <div id="app">
        <header class="chart-header">
            <h1>奇門遁甲 Interactive Qi Men Dun Jia Chart</h1>
            <div class="controls">
                <div class="time-controls">
                    <input type="datetime-local" id="time-selector" 
                           value="{self.state.current_time.strftime('%Y-%m-%dT%H:%M')}">
                    <button id="now-button">Now</button>
                    <button id="animate-button">▶ Animate</button>
                    <input type="range" id="speed-slider" min="0.1" max="5" step="0.1" value="1">
                </div>
                <div class="view-controls">
                    <button id="comparison-button">Compare Times</button>
                    <button id="predictions-button">Show Predictions</button>
                </div>
            </div>
        </header>

        <main class="chart-container">
            <div class="chart-grid" id="chart-grid">
                {self._generate_interactive_grid_html()}
            </div>

            <div class="side-panel" id="side-panel">
                <div class="panel-content">
                    <h3>Chart Information</h3>
                    <div id="chart-info">
                        <p>Click on a palace for detailed analysis</p>
                    </div>
                </div>
            </div>
        </main>

        <div class="query-panel">
            <h3>Ask a Question</h3>
            <input type="text" id="query-input" placeholder="Enter your divination question...">
            <button id="query-submit">Analyze</button>
        </div>

        <div id="tooltip" class="tooltip hidden"></div>

        <div id="comparison-modal" class="modal hidden">
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2>Compare Two Time Periods</h2>
                <div class="comparison-container">
                    <div class="comparison-chart" id="comparison-chart-1"></div>
                    <div class="comparison-chart" id="comparison-chart-2"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        {self._get_interactive_javascript()}
    </script>
</body>
</html>
        """

    def _get_interactive_css(self) -> str:
        """Generate CSS for interactive interface"""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Microsoft YaHei', SimSun, serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #eee;
            min-height: 100vh;
        }

        .chart-header {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-bottom: 2px solid #ffd700;
        }

        .chart-header h1 {
            color: #ffd700;
            text-align: center;
            margin-bottom: 15px;
            font-size: 28px;
        }

        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }

        .time-controls, .view-controls {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        button {
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            color: #1a1a2e;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        button:hover {
            background: linear-gradient(45deg, #ffed4e, #ffd700);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(255,215,0,0.3);
        }

        input[type="datetime-local"], input[type="text"] {
            background: rgba(255,255,255,0.1);
            border: 1px solid #ffd700;
            color: #eee;
            padding: 8px;
            border-radius: 5px;
        }

        .chart-container {
            display: flex;
            padding: 20px;
            gap: 20px;
            min-height: calc(100vh - 200px);
        }

        .chart-grid {
            flex: 1;
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            grid-template-rows: 1fr 1fr 1fr;
            gap: 3px;
            background: #ffd700;
            border: 3px solid #ffd700;
            border-radius: 10px;
            max-width: 600px;
            height: 600px;
        }

        .palace {
            background: rgba(255,255,255,0.95);
            color: #1a1a2e;
            padding: 15px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            border-radius: 5px;
        }

        .palace:hover {
            background: rgba(255,255,255,1);
            transform: scale(1.05);
            z-index: 10;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        }

        .palace.selected {
            background: #ffed4e;
            border: 2px solid #ffd700;
        }

        .palace.auspicious {
            border-left: 5px solid #228B22;
        }

        .palace.inauspicious {
            border-left: 5px solid #DC143C;
        }

        .palace.center {
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            font-weight: bold;
        }

        .palace-number {
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 5px;
        }

        .gate { color: #DC143C; font-weight: bold; }
        .star { color: #4169E1; font-weight: bold; }
        .spirit { color: #9932CC; font-weight: bold; }

        .side-panel {
            width: 350px;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 20px;
            overflow-y: auto;
        }

        .query-panel {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-top: 2px solid #ffd700;
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .query-panel input {
            flex: 1;
        }

        .tooltip {
            position: absolute;
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ffd700;
            z-index: 1000;
            max-width: 300px;
            pointer-events: none;
        }

        .tooltip.hidden { display: none; }

        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 2000;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .modal.hidden { display: none; }

        .modal-content {
            background: #1a1a2e;
            padding: 30px;
            border-radius: 10px;
            border: 2px solid #ffd700;
            max-width: 90%;
            max-height: 90%;
            overflow: auto;
        }

        .comparison-container {
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }

        .comparison-chart {
            flex: 1;
            min-height: 400px;
        }

        .close {
            float: right;
            font-size: 28px;
            font-weight: bold;
            color: #ffd700;
            cursor: pointer;
        }

        .close:hover {
            color: #ffed4e;
        }

        @keyframes palace-change {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }

        .palace.changing {
            animation: palace-change 0.5s ease-in-out;
        }

        .analysis-section {
            margin: 15px 0;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
            border-left: 3px solid #ffd700;
        }

        .recommendation {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            border-left: 3px solid;
        }

        .recommendation.high { border-left-color: #DC143C; }
        .recommendation.medium { border-left-color: #FF8C00; }
        .recommendation.low { border-left-color: #32CD32; }
        """

    def _get_interactive_javascript(self) -> str:
        """Generate JavaScript for interactive functionality"""
        initial_chart_data = json.dumps(self._serialize_chart(self.current_chart))

        return f"""
        class QiMenInteractive {{
            constructor() {{
                this.currentChart = {initial_chart_data};
                this.selectedPalace = null;
                this.isAnimating = false;
                this.animationSpeed = 1.0;

                this.initializeEventHandlers();
                this.renderChart();
            }}

            initializeEventHandlers() {{
                // Palace interactions
                document.addEventListener('click', (e) => {{
                    if (e.target.classList.contains('palace')) {{
                        this.handlePalaceClick(e.target);
                    }}
                }});

                document.addEventListener('mouseover', (e) => {{
                    if (e.target.classList.contains('palace')) {{
                        this.handlePalaceHover(e.target, e);
                    }}
                }});

                document.addEventListener('mouseout', (e) => {{
                    if (e.target.classList.contains('palace')) {{
                        this.hideTooltip();
                    }}
                }});

                // Time controls
                document.getElementById('time-selector').addEventListener('change', (e) => {{
                    this.handleTimeChange(new Date(e.target.value));
                }});

                document.getElementById('now-button').addEventListener('click', () => {{
                    this.setCurrentTime(new Date());
                }});

                document.getElementById('animate-button').addEventListener('click', () => {{
                    this.toggleAnimation();
                }});

                document.getElementById('speed-slider').addEventListener('input', (e) => {{
                    this.animationSpeed = parseFloat(e.target.value);
                }});

                // Query handling
                document.getElementById('query-submit').addEventListener('click', () => {{
                    const query = document.getElementById('query-input').value;
                    if (query.trim()) {{
                        this.handleQuery(query);
                    }}
                }});

                // Comparison mode
                document.getElementById('comparison-button').addEventListener('click', () => {{
                    this.showComparisonModal();
                }});

                // Modal controls
                document.querySelector('.close').addEventListener('click', () => {{
                    this.hideComparisonModal();
                }});
            }}

            handlePalaceClick(palaceElement) {{
                const palaceNumber = parseInt(palaceElement.dataset.palace);

                // Remove previous selection
                document.querySelectorAll('.palace.selected').forEach(p => {{
                    p.classList.remove('selected');
                }});

                // Select current palace
                palaceElement.classList.add('selected');
                this.selectedPalace = palaceNumber;

                // Show detailed analysis
                this.showPalaceAnalysis(palaceNumber);

                // Send to backend for detailed analysis
                this.requestPalaceAnalysis(palaceNumber);
            }}

            handlePalaceHover(palaceElement, event) {{
                const palaceNumber = parseInt(palaceElement.dataset.palace);
                const config = this.currentChart.configurations[palaceNumber];

                this.showTooltip(event, config);
            }}

            showTooltip(event, config) {{
                const tooltip = document.getElementById('tooltip');
                const auspiciousText = config.is_auspicious ? '吉 Auspicious' : '凶 Inauspicious';

                tooltip.innerHTML = `
                    <div class="tooltip-header">
                        <strong>Palace ${{config.palace_number}}</strong> - ${{auspiciousText}}
                    </div>
                    <div>門 Gate: ${{config.gate || 'Center'}}</div>
                    <div>星 Star: ${{config.star || ''}}</div>
                    <div>神 Spirit: ${{config.spirit || ''}}</div>
                    <div>Element: ${{config.element}}</div>
                `;

                tooltip.style.left = event.pageX + 10 + 'px';
                tooltip.style.top = event.pageY + 10 + 'px';
                tooltip.classList.remove('hidden');
            }}

            hideTooltip() {{
                document.getElementById('tooltip').classList.add('hidden');
            }}

            handleTimeChange(newTime) {{
                // Send request to backend for new chart
                this.requestNewChart(newTime);
            }}

            setCurrentTime(time) {{
                const timeSelector = document.getElementById('time-selector');
                const timeString = time.toISOString().slice(0, 16);
                timeSelector.value = timeString;
                this.handleTimeChange(time);
            }}

            toggleAnimation() {{
                const button = document.getElementById('animate-button');

                if (this.isAnimating) {{
                    this.stopAnimation();
                    button.textContent = '▶ Animate';
                }} else {{
                    this.startAnimation();
                    button.textContent = '⏸ Pause';
                }}

                this.isAnimating = !this.isAnimating;
            }}

            startAnimation() {{
                this.animationInterval = setInterval(() => {{
                    const currentTime = new Date(document.getElementById('time-selector').value);
                    const newTime = new Date(currentTime.getTime() + (3600000 * this.animationSpeed)); // Add 1 hour * speed
                    this.setCurrentTime(newTime);
                }}, 1000 / this.animationSpeed);
            }}

            stopAnimation() {{
                if (this.animationInterval) {{
                    clearInterval(this.animationInterval);
                }}
            }}

            renderChart() {{
                const chartGrid = document.getElementById('chart-grid');
                const gridLayout = [
                    [4, 9, 2],
                    [3, 5, 7],
                    [8, 1, 6]
                ];

                chartGrid.innerHTML = '';

                gridLayout.forEach(row => {{
                    row.forEach(palaceNumber => {{
                        const config = this.currentChart.configurations[palaceNumber];
                        const palaceDiv = this.createPalaceElement(palaceNumber, config);
                        chartGrid.appendChild(palaceDiv);
                    }});
                }});
            }}

            createPalaceElement(palaceNumber, config) {{
                const div = document.createElement('div');
                div.className = 'palace';
                div.dataset.palace = palaceNumber;

                if (palaceNumber === 5) {{
                    div.classList.add('center');
                    div.innerHTML = `
                        <div class="palace-number">Palace ${{palaceNumber}} 中宮</div>
                        <div class="star">⚬ CENTER ⚬</div>
                        <div class="star">${{config.star || ''}}</div>
                    `;
                }} else {{
                    if (config.is_auspicious) {{
                        div.classList.add('auspicious');
                    }} else {{
                        div.classList.add('inauspicious');
                    }}

                    const auspiciousText = config.is_auspicious ? '吉' : '凶';
                    div.innerHTML = `
                        <div class="palace-number">Palace ${{palaceNumber}} ${{auspiciousText}}</div>
                        <div class="gate">門: ${{config.gate ? config.gate.substring(0, 2) : '──'}}</div>
                        <div class="star">星: ${{config.star ? config.star.substring(0, 2) : '──'}}</div>
                        <div class="spirit">神: ${{config.spirit ? config.spirit.substring(0, 2) : '──'}}</div>
                    `;
                }}

                return div;
            }}

            showPalaceAnalysis(palaceNumber) {{
                const config = this.currentChart.configurations[palaceNumber];
                const sidePanel = document.getElementById('chart-info');

                sidePanel.innerHTML = `
                    <div class="analysis-section">
                        <h4>Palace ${{palaceNumber}} Analysis</h4>
                        <p><strong>Status:</strong> ${{config.is_auspicious ? 'Auspicious 吉' : 'Inauspicious 凶'}}</p>
                        <p><strong>Gate:</strong> ${{config.gate || 'Center'}}</p>
                        <p><strong>Star:</strong> ${{config.star || 'N/A'}}</p>
                        <p><strong>Spirit:</strong> ${{config.spirit || 'N/A'}}</p>
                        <p><strong>Element:</strong> ${{config.element}}</p>
                        <p><strong>Energy:</strong> ${{config.energy_quality}}</p>
                        <p><strong>Application:</strong> ${{config.strategic_application}}</p>
                    </div>
                `;
            }}

            requestPalaceAnalysis(palaceNumber) {{
                // Simulate API call for detailed analysis
                // In real implementation, this would call your backend
                console.log(`Requesting detailed analysis for palace ${{palaceNumber}}`);
            }}

            requestNewChart(newTime) {{
                // Simulate API call for new chart
                // In real implementation, this would call your backend
                console.log(`Requesting new chart for time: ${{newTime}}`);

                // For demo, just update the display
                this.updateChartDisplay();
            }}

            updateChartDisplay() {{
                // Add changing animation to all palaces
                document.querySelectorAll('.palace').forEach(palace => {{
                    palace.classList.add('changing');
                    setTimeout(() => {{
                        palace.classList.remove('changing');
                    }}, 500);
                }});

                // Re-render chart with new data
                setTimeout(() => {{
                    this.renderChart();
                }}, 250);
            }}

            handleQuery(query) {{
                console.log(`Processing query: ${{query}}`);

                // Show query results in side panel
                const sidePanel = document.getElementById('chart-info');
                sidePanel.innerHTML = `
                    <div class="analysis-section">
                        <h4>Query Analysis</h4>
                        <p><strong>Question:</strong> ${{query}}</p>
                        <p>Analyzing current chart configuration...</p>
                        <div class="recommendation high">
                            <strong>Primary Recommendation:</strong> Based on current palace positions, timing appears favorable for your inquiry.
                        </div>
                        <div class="recommendation medium">
                            <strong>Timing Advice:</strong> Consider acting within the next 2-4 hours for optimal results.
                        </div>
                    </div>
                `;
            }}

            showComparisonModal() {{
                document.getElementById('comparison-modal').classList.remove('hidden');
            }}

            hideComparisonModal() {{
                document.getElementById('comparison-modal').classList.add('hidden');
            }}
        }}

        // Initialize the interactive chart when page loads
        document.addEventListener('DOMContentLoaded', () => {{
            window.qimenChart = new QiMenInteractive();
        }});
        """

    def _generate_interactive_grid_html(self) -> str:
        """Generate HTML for the interactive grid"""
        grid_layout = [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]

        html_parts = []

        for row in grid_layout:
            for palace_number in row:
                config = self.current_chart.configurations[palace_number]

                if palace_number == 5:
                    # Center palace
                    html_parts.append(f'''
                    <div class="palace center" data-palace="{palace_number}">
                        <div class="palace-number">Palace {palace_number} 中宮</div>
                        <div class="star">⚬ CENTER ⚬</div>
                        <div class="star">{config.star.value if config.star else ""}</div>
                    </div>
                    ''')
                else:
                    # Regular palace
                    auspicious_class = "auspicious" if config.is_auspicious else "inauspicious"
                    auspicious_text = "吉" if config.is_auspicious else "凶"

                    html_parts.append(f'''
                    <div class="palace {auspicious_class}" data-palace="{palace_number}">
                        <div class="palace-number">Palace {palace_number} {auspicious_text}</div>
                        <div class="gate">門: {config.gate.value[:2] if config.gate else "──"}</div>
                        <div class="star">星: {config.star.value[:2] if config.star else "──"}</div>
                        <div class="spirit">神: {config.spirit.value[:2] if config.spirit else "──"}</div>
                    </div>
                    ''')

        return ''.join(html_parts)

    # Helper methods for analysis
    def _calculate_star_influence(self, star) -> float:
        """Calculate star influence strength"""
        # Implementation depends on star type and current timing
        return 0.7  # Placeholder

    def _get_spirit_meaning(self, spirit) -> str:
        """Get meaning of spirit"""
        spirit_meanings = {
            "值符": "Command and authority",
            "騰蛇": "Transformation and change",
            "太陰": "Hidden influences",
            "六合": "Harmony and cooperation",
            "白虎": "Conflict and aggression",
            "玄武": "Stealth and protection",
            "九地": "Defensive positioning",
            "九天": "Elevated perspective"
        }
        return spirit_meanings.get(spirit.value if spirit else "", "Unknown influence")

    def _analyze_elemental_relationships(self, config: QiMenConfiguration) -> Dict:
        """Analyze elemental relationships in configuration"""
        # Implementation for elemental analysis
        return {
            "primary_element": config.element.value,
            "harmony_level": 0.7,
            "conflicts": [],
            "enhancements": []
        }

    def _analyze_temporal_influences(self, palace_number: int) -> Dict:
        """Analyze temporal influences on palace"""
        # Implementation for temporal analysis
        return {
            "current_strength": 0.8,
            "peak_times": ["11:00-13:00", "17:00-19:00"],
            "weak_times": ["23:00-01:00"]
        }

    def _get_element_advice(self, element: Element) -> str:
        """Get advice based on element"""
        advice = {
            Element.WOOD: "Focus on growth, creativity, and new beginnings. Avoid conflict.",
            Element.FIRE: "Perfect for public activities, presentations, and social engagement.",
            Element.EARTH: "Excellent for stability, foundation-building, and team cooperation.",
            Element.METAL: "Good for precision work, quality improvement, and elimination of excess.",
            Element.WATER: "Ideal for deep thinking, research, and adaptive strategies."
        }
        return advice.get(element, "Balance all elements in your approach.")

    def _are_complementary_gates(self, gate1, gate2) -> bool:
        """Check if two gates are complementary"""
        # Implementation for gate relationships
        return False  # Placeholder

    def _have_star_relationship(self, star1, star2) -> bool:
        """Check if two stars have special relationship"""
        # Implementation for star relationships
        return False  # Placeholder

    def _describe_relationship(self, relationship_types: List[str]) -> str:
        """Describe relationship between palaces"""
        descriptions = {
            'same_element': "Shares elemental harmony",
            'complementary_gates': "Gates work in harmony",
            'star_harmony': "Stars support each other"
        }
        return "; ".join([descriptions.get(rt, rt) for rt in relationship_types])

    def _get_time_period_name(self, hour: int) -> str:
        """Get traditional time period name for hour"""
        periods = {
            23: "子時 (Zi Shi)", 1: "丑時 (Chou Shi)", 3: "寅時 (Yin Shi)",
            5: "卯時 (Mao Shi)", 7: "辰時 (Chen Shi)", 9: "巳時 (Si Shi)",
            11: "午時 (Wu Shi)", 13: "未時 (Wei Shi)", 15: "申時 (Shen Shi)",
            17: "酉時 (You Shi)", 19: "戌時 (Xu Shi)", 21: "亥時 (Hai Shi)"
        }
        return periods.get(hour, f"Hour {hour}")

    def _predict_next_change(self, palace_number: int) -> Dict:
        """Predict when palace configuration will next change"""
        return {
            "next_change_time": "2 hours",
            "change_type": "auspiciousness_flip",
            "confidence": 0.8
        }


class InteractiveTaiyiChart:
    """Interactive Taiyi chart with star movement visualization"""

    def __init__(self, initial_time: datetime = None):
        self.calculator = TaiyiCalculator()
        self.visualizer = ChartVisualizer()

        self.initial_time = initial_time or datetime.now()
        self.current_divination = self.calculator.perform_divination(self.initial_time)
        self.state = ChartState(
            current_time=self.initial_time,
            selected_palace=None,
            hover_palace=None,
            time_range_start=self.initial_time - timedelta(days=30),
            time_range_end=self.initial_time + timedelta(days=30),
            animation_speed=1.0,
            show_predictions=False,
            comparison_time=None,
            user_query="",
            interaction_history=[]
        )

    def generate_interactive_html(self) -> str:
        """Generate interactive Taiyi HTML interface"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Interactive Taiyi Divine Number</title>
    <style>
        {self._get_taiyi_css()}
    </style>
</head>
<body>
    <div id="taiyi-app">
        <header class="taiyi-header">
            <h1>太乙神數 Interactive Taiyi Divine Number</h1>
            <div class="taiyi-controls">
                <input type="datetime-local" id="taiyi-time" 
                       value="{self.initial_time.strftime('%Y-%m-%dT%H:%M')}">
                <button id="taiyi-calculate">Calculate</button>
                <button id="star-animation">Animate Stars</button>
            </div>
        </header>

        <main class="taiyi-container">
            <div class="circular-chart" id="taiyi-circle">
                {self._generate_taiyi_svg()}
            </div>

            <div class="taiyi-panel">
                <div class="star-info">
                    <h3>⭐ Master Star</h3>
                    <div id="master-star-info">
                        <p>{self.current_divination.master_star_position.star.value}</p>
                        <p>Palace {self.current_divination.master_star_position.palace.number}</p>
                        <p>Influence: {self.current_divination.master_star_position.influence_strength:.2f}</p>
                    </div>
                </div>

                <div class="star-info">
                    <h3>🌟 Guest Star</h3>
                    <div id="guest-star-info">
                        <p>{self.current_divination.guest_star_position.star.value}</p>
                        <p>Palace {self.current_divination.guest_star_position.palace.number}</p>
                        <p>Influence: {self.current_divination.guest_star_position.influence_strength:.2f}</p>
                    </div>
                </div>

                <div class="element-chart">
                    <h3>Elemental Influences</h3>
                    <div id="element-bars">
                        {self._generate_element_bars()}
                    </div>
                </div>
            </div>
        </main>

        <div class="guidance-panel">
            <h3>Strategic Guidance</h3>
            <div id="guidance-content">
                <p>{self.current_divination.strategic_guidance}</p>
            </div>
        </div>
    </div>

    <script>
        {self._get_taiyi_javascript()}
    </script>
</body>
</html>
        """

    def _generate_taiyi_svg(self) -> str:
        """Generate SVG for Taiyi circular chart"""
        return """
        <svg width="500" height="500" viewBox="0 0 500 500">
            <!-- Palace circles will be generated by JavaScript -->
        </svg>
        """

    def _generate_element_bars(self) -> str:
        """Generate HTML for elemental influence bars"""
        html_parts = []
        element_colors = {
            "木": "#228B22", "火": "#DC143C", "土": "#DAA520",
            "金": "#C0C0C0", "水": "#4169E1"
        }

        for element, influence in self.current_divination.elemental_influences.items():
            color = element_colors.get(element.value, "#666")
            percentage = influence * 100

            html_parts.append(f"""
            <div class="element-bar">
                <span class="element-name">{element.value}</span>
                <div class="bar-container">
                    <div class="bar-fill" style="width: {percentage}%; background-color: {color};"></div>
                </div>
                <span class="element-value">{influence:.2f}</span>
            </div>
            """)

        return ''.join(html_parts)

    def _get_taiyi_css(self) -> str:
        """Generate CSS for Taiyi interface"""
        return """
        /* Taiyi-specific CSS styles */
        body {
            background: radial-gradient(circle at center, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            font-family: 'Microsoft YaHei', serif;
            color: #ffd700;
            margin: 0;
            padding: 0;
        }

        .taiyi-header {
            text-align: center;
            padding: 20px;
            border-bottom: 2px solid #ffd700;
        }

        .taiyi-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 40px;
            padding: 40px;
            min-height: 70vh;
        }

        .circular-chart {
            position: relative;
        }

        .taiyi-panel {
            width: 300px;
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #ffd700;
        }

        .star-info {
            margin-bottom: 20px;
            padding: 15px;
            background: rgba(255,215,0,0.1);
            border-radius: 10px;
        }

        .element-bar {
            display: flex;
            align-items: center;
            margin: 8px 0;
            gap: 10px;
        }

        .element-name {
            width: 30px;
            font-weight: bold;
        }

        .bar-container {
            flex: 1;
            height: 20px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            transition: width 0.5s ease;
            border-radius: 10px;
        }

        .element-value {
            width: 50px;
            text-align: right;
            font-size: 12px;
        }

        .guidance-panel {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
            border: 1px solid #ffd700;
        }
        """

    def _get_taiyi_javascript(self) -> str:
        """Generate JavaScript for Taiyi interactions"""
        return """
        class TaiyiInteractive {
            constructor() {
                this.initializeSVG();
                this.bindEvents();
            }

            initializeSVG() {
                const svg = document.querySelector('svg');

                // Palace positions
                const palaces = [
                    {num: 1, x: 250, y: 80, name: "坎宮"},
                    {num: 2, x: 150, y: 350, name: "坤宮"},
                    {num: 3, x: 420, y: 250, name: "震宮"},
                    {num: 4, x: 350, y: 350, name: "巽宮"},
                    {num: 5, x: 250, y: 250, name: "中宮"},
                    {num: 6, x: 150, y: 150, name: "乾宮"},
                    {num: 7, x: 80, y: 250, name: "兌宮"},
                    {num: 8, x: 350, y: 150, name: "艮宮"},
                    {num: 9, x: 250, y: 420, name: "離宮"}
                ];

                // Draw connections
                const center = palaces.find(p => p.num === 5);
                palaces.filter(p => p.num !== 5).forEach(palace => {
                    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                    line.setAttribute("x1", center.x);
                    line.setAttribute("y1", center.y);
                    line.setAttribute("x2", palace.x);
                    line.setAttribute("y2", palace.y);
                    line.setAttribute("stroke", "#ffd700");
                    line.setAttribute("stroke-width", "1");
                    line.setAttribute("opacity", "0.3");
                    svg.appendChild(line);
                });

                // Draw palaces
                palaces.forEach(palace => {
                    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
                    circle.setAttribute("cx", palace.x);
                    circle.setAttribute("cy", palace.y);
                    circle.setAttribute("r", palace.num === 5 ? 40 : 30);
                    circle.setAttribute("fill", palace.num === 5 ? "#ffd700" : "rgba(255,215,0,0.2)");
                    circle.setAttribute("stroke", "#ffd700");
                    circle.setAttribute("stroke-width", "2");
                    circle.setAttribute("data-palace", palace.num);
                    circle.style.cursor = "pointer";

                    circle.addEventListener("click", () => this.selectPalace(palace.num));
                    svg.appendChild(circle);

                    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                    text.setAttribute("x", palace.x);
                    text.setAttribute("y", palace.y + 5);
                    text.setAttribute("text-anchor", "middle");
                    text.setAttribute("fill", palace.num === 5 ? "#000" : "#ffd700");
                    text.setAttribute("font-size", "12");
                    text.textContent = palace.num;
                    svg.appendChild(text);
                });
            }

            selectPalace(palaceNum) {
                console.log(`Selected palace: ${palaceNum}`);
                // Highlight selected palace
                document.querySelectorAll('circle').forEach(c => {
                    c.setAttribute("stroke-width", "2");
                });

                const selectedCircle = document.querySelector(`circle[data-palace="${palaceNum}"]`);
                selectedCircle.setAttribute("stroke-width", "4");
            }

            bindEvents() {
                document.getElementById('taiyi-calculate').addEventListener('click', () => {
                    const newTime = document.getElementById('taiyi-time').value;
                    console.log(`Calculating for time: ${newTime}`);
                    // Would call backend to recalculate
                });

                document.getElementById('star-animation').addEventListener('click', () => {
                    this.animateStars();
                });
            }

            animateStars() {
                console.log('Starting star animation...');
                // Implementation for star movement animation
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            window.taiyiChart = new TaiyiInteractive();
        });
        """


# Usage example
def create_interactive_demo():
    """Create a complete interactive demo"""

    # Create Qi Men interactive chart
    qimen = InteractiveQiMenChart()
    qimen_html = qimen.generate_interactive_html()

    # Create Taiyi interactive chart
    taiyi = InteractiveTaiyiChart()
    taiyi_html = taiyi.generate_interactive_html()

    # Save to files
    with open('interactive_qimen.html', 'w', encoding='utf-8') as f:
        f.write(qimen_html)

    with open('interactive_taiyi.html', 'w', encoding='utf-8') as f:
        f.write(taiyi_html)

    return qimen, taiyi