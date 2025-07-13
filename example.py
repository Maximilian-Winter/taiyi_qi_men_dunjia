import datetime
import os

from divination.taiyi import TaiyiCalculator
from divination.qi_men_dunjia import QiMenCalculator, TimeFrame
from divination.visualizations import ChartVisualizer, create_matplotlib_qimen, create_matplotlib_taiyi


def demonstrate_taiyi_divination():
    """Demonstrate Taiyi Divine Number system with multiple visualization options"""
    print("=" * 80)
    print("🌟 TAIYI DIVINE NUMBER DEMONSTRATION")
    print("=" * 80)
    
    # Initialize calculator
    taiyi = TaiyiCalculator()
    
    # Test with current time
    current_time = datetime.datetime.now()
    print(f"Calculating for: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Perform divination
    divination = taiyi.perform_divination(current_time)
    
    # Initialize visualizer
    visualizer = ChartVisualizer()
    
    print("\n📊 STANDARD DISPLAY:")
    print(taiyi.display_divination_result(divination))
    
    print("\n🎯 CIRCULAR ASCII CHART:")
    print(visualizer.render_taiyi_circular(divination))
    
    print("\n📝 DETAILED CIRCULAR CHART:")
    print(visualizer.render_taiyi_detailed_circular(divination))
    
    # Save HTML version
    html_content = visualizer.render_html_taiyi(divination)
    os.makedirs("output", exist_ok=True)
    with open("output/taiyi_chart.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("💾 HTML chart saved to: output/taiyi_chart.html")
    
    # Try matplotlib version (optional)
    try:
        fig = create_matplotlib_taiyi(divination, "output/taiyi_chart.png")
        if fig:
            print("🖼️  Matplotlib chart saved to: output/taiyi_chart.png")
    except Exception as e:
        print(f"📝 Matplotlib visualization not available: {e}")
    
    return divination


def demonstrate_qimen_charts():
    """Demonstrate Qi Men Dun Jia system with multiple visualization options"""
    print("\n" + "=" * 80)
    print("🎯 QI MEN DUN JIA DEMONSTRATION")
    print("=" * 80)
    
    # Initialize calculator
    calculator = QiMenCalculator()
    visualizer = ChartVisualizer()
    
    # Test with different time frames
    current_time = datetime.datetime.now()
    print(f"Calculating for: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Hour-based chart (most common)
    print("\n⏰ HOURLY CHART:")
    hour_chart = calculator.calculate_qi_men_chart(current_time, TimeFrame.HOUR)
    
    print("\n📊 STANDARD DISPLAY:")
    print(calculator.display_qi_men_chart(hour_chart))
    
    print("\n🎨 ASCII ART CHART:")
    print(visualizer.render_qimen_ascii(hour_chart))
    
    print("\n📋 DETAILED ASCII CHART:")
    print(visualizer.render_qimen_detailed(hour_chart))
    
    # Save HTML version
    html_content = visualizer.render_html_qimen(hour_chart)
    with open("output/qimen_hour_chart.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("💾 HTML hour chart saved to: output/qimen_hour_chart.html")
    
    # Day-based chart
    print("\n📅 DAILY CHART:")
    day_chart = calculator.calculate_qi_men_chart(current_time, TimeFrame.DAY)
    print(visualizer.render_qimen_ascii(day_chart))
    
    # Month-based chart
    print("\n🗓️  MONTHLY CHART:")
    month_chart = calculator.calculate_qi_men_chart(current_time, TimeFrame.MONTH)
    print(visualizer.render_qimen_ascii(month_chart))
    
    # Try matplotlib version (optional)
    try:
        fig = create_matplotlib_qimen(hour_chart, "output/qimen_chart.png")
        if fig:
            print("🖼️  Matplotlib chart saved to: output/qimen_chart.png")
    except Exception as e:
        print(f"📝 Matplotlib visualization not available: {e}")
    
    return hour_chart


def demonstrate_calendar_system():
    """Demonstrate the Chinese lunar calendar system"""
    print("\n" + "=" * 80)
    print("🗓️  CHINESE LUNAR CALENDAR DEMONSTRATION")
    print("=" * 80)
    
    from divination.calendar import ChineseLunarCalendar
    
    calendar = ChineseLunarCalendar()
    
    # Test dates
    test_dates = [
        datetime.datetime(2024, 1, 1, 12, 0),      # New Year
        datetime.datetime(2024, 2, 10, 6, 0),      # Chinese New Year 2024
        datetime.datetime.now(),                    # Current time
        datetime.datetime(2024, 12, 21, 18, 0),    # Winter Solstice
    ]
    
    for date in test_dates:
        print(f"\n📅 Gregorian: {date.strftime('%Y-%m-%d %H:%M')}")
        
        # Convert to lunar
        lunar_date = calendar.gregorian_to_lunar(date)
        print(f"🌙 Lunar: Year {lunar_date.year}, Month {lunar_date.month}, Day {lunar_date.day}")
        if lunar_date.is_leap_month:
            print("   (Leap Month)")
        
        # Four Pillars
        print(f"🏛️  Four Pillars:")
        print(f"   Year:  {lunar_date.year_stem.chinese}{lunar_date.year_branch.chinese} ({lunar_date.year_branch.zodiac_english})")
        print(f"   Month: {lunar_date.month_stem.chinese}{lunar_date.month_branch.chinese}")
        print(f"   Day:   {lunar_date.day_stem.chinese}{lunar_date.day_branch.chinese}")
        print(f"   Hour:  {lunar_date.hour_stem.chinese}{lunar_date.hour_branch.chinese} ({lunar_date.hour_branch.time_period})")
        
        # Element analysis
        analysis = calendar.analyze_lunar_date(lunar_date)
        print(f"🌟 Elements: {dict(analysis['elemental_composition']['element_distribution'])}")
        print(f"⚖️  Balance: {analysis['elemental_composition']['balance_assessment']}")
        
        print("-" * 60)


def demonstrate_palace_system():
    """Demonstrate the Nine Palaces and Eight Trigrams system"""
    print("\n" + "=" * 80)
    print("🏛️  NINE PALACES & EIGHT TRIGRAMS DEMONSTRATION")
    print("=" * 80)
    
    from divination.trigrams import NinePalaces, EightTrigrams
    
    nine_palaces = NinePalaces()
    eight_trigrams = EightTrigrams()
    
    # Display palace grid
    print("🌐 Nine Palaces Layout:")
    print(nine_palaces.display_palace_grid())
    
    # Show trigram details
    print("🔯 Eight Trigrams Details:")
    for trigram in eight_trigrams.trigrams:
        print(f"\n{trigram.get_visual_symbol()} {trigram.chinese} ({trigram.pinyin}) - {trigram.english}")
        print(f"   Element: {trigram.element.value} | Direction: {trigram.direction.value}")
        print(f"   Quality: {trigram.quality}")
        print(f"   Strategy: {trigram.strategic_application}")
        print(f"   Family: {trigram.family_position}")


def interactive_divination():
    """Interactive divination session"""
    print("\n" + "=" * 80)
    print("🔮 INTERACTIVE DIVINATION SESSION")
    print("=" * 80)
    
    taiyi = TaiyiCalculator()
    qimen = QiMenCalculator()
    visualizer = ChartVisualizer()
    
    while True:
        print("\nChoose divination type:")
        print("1. Taiyi Divine Number")
        print("2. Qi Men Dun Jia")
        print("3. Both systems")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "4":
            break
        
        # Get query time
        use_current = input("Use current time? (y/n): ").strip().lower() == 'y'
        
        if use_current:
            query_time = datetime.datetime.now()
        else:
            try:
                date_str = input("Enter date/time (YYYY-MM-DD HH:MM): ")
                query_time = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid format, using current time.")
                query_time = datetime.datetime.now()
        
        print(f"\n🕒 Query time: {query_time.strftime('%Y-%m-%d %H:%M')}")
        
        if choice in ["1", "3"]:
            print("\n" + "🌟" * 30)
            print("TAIYI DIVINE NUMBER RESULT")
            print("🌟" * 30)
            
            divination = taiyi.perform_divination(query_time)
            print(visualizer.render_taiyi_circular(divination))
        
        if choice in ["2", "3"]:
            print("\n" + "🎯" * 30)
            print("QI MEN DUN JIA RESULT")
            print("🎯" * 30)
            
            chart = qimen.calculate_qi_men_chart(query_time)
            print(visualizer.render_qimen_ascii(chart))


def main():
    """Main demonstration function"""
    print("🏮" * 40)
    print("CHINESE DIVINATION FRAMEWORK DEMONSTRATION")
    print("🏮" * 40)
    print("This demonstration showcases the complete divination system")
    print("with traditional Chinese Taiyi and Qi Men Dun Jia methods.")
    print()
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    try:
        # Core demonstrations
        demonstrate_calendar_system()
        demonstrate_palace_system()
        demonstrate_taiyi_divination()
        demonstrate_qimen_charts()
        
        # Interactive session
        interactive_choice = input("\n🎮 Would you like to try interactive divination? (y/n): ").strip().lower()
        if interactive_choice == 'y':
            interactive_divination()
        
        print("\n" + "🎊" * 30)
        print("DEMONSTRATION COMPLETE!")
        print("🎊" * 30)
        print("Check the 'output' folder for saved HTML and image files.")
        print("Thank you for exploring Chinese divination traditions!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demonstration interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")


if __name__ == "__main__":
    main()