"""
Test script for Music Recommendation Engine
"""

from music_recommendation_engine import get_music_recommendation


def test_scenarios():
    test_inputs = [
        "I'm feeling really sad and lonely after my breakup",
        "I'm so stressed about my exams and work pressure",
        "I'm super excited about my new job and can't wait to start!",
        "I'm feeling romantic and missing my partner",
        "I'm happy and feeling grateful for everything"
    ]
    
    print("🧪 Testing Music Recommendation Engine\n")
    print("=" * 60)
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n📝 Test Case {i}: {test_input}")
        print("-" * 60)
        result = get_music_recommendation(test_input)
        print(result)
        print()


if __name__ == "__main__":
    test_scenarios()
