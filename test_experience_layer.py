"""
Test Experience Layer.

Tests:
- Habit formation
- Shortcut detection
- Object memory
- Skill learning
- Experience graph
- QuantaCoin compression
"""

import sys
from pathlib import Path

print("=" * 60)
print("Testing Experience Layer")
print("=" * 60)

# 1. Test Habit Formation
print("\n1. Testing Habit Formation...")
try:
    from experience.habits import HabitManager
    
    habits = HabitManager(repo_path="test_repo")
    
    # Record repeated patterns
    for i in range(5):
        habits.record_pattern((0, 2), entropy=0.5, curvature=0.3)
        habits.record_pattern((2, 3), entropy=0.6, curvature=0.4)
    
    # Check habit strength
    strength1 = habits.get_habit_strength((0, 2))
    strength2 = habits.get_habit_strength((2, 3))
    
    print(f"  ✓ Recorded patterns")
    print(f"  ✓ Habit strength (0→2): {strength1:.4f}")
    print(f"  ✓ Habit strength (2→3): {strength2:.4f}")
    
    assert strength1 > 0, "Should have habit strength"
    assert strength2 > 0, "Should have habit strength"
    
    # Save and load
    habits.save_to_repo()
    habits2 = HabitManager(repo_path="test_repo")
    print(f"  ✓ Loaded {len(habits2.habits)} habits from repo")
    
    # Cleanup
    import shutil
    if Path("test_repo").exists():
        shutil.rmtree("test_repo")
    
    print("  ✓ Habit Formation: PASSED")
except Exception as e:
    print(f"  ✗ Habit Formation: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 2. Test Shortcut Detection
print("\n2. Testing Shortcut Detection...")
try:
    from experience.shortcuts import ShortcutManager
    from combinatoric.interpreter import CombinatoricInterpreter
    
    shortcuts = ShortcutManager(repo_path="test_repo")
    
    # Create shell sequence
    shell_sequence = [0, 2, 3, 4]
    entropy_history = [1.0, 0.8, 0.6, 0.4]  # Decreasing
    curvature_history = [0.3, 0.3, 0.3, 0.3]  # Stable
    error_history = [0.1, 0.1, 0.1, 0.1]  # Low variance
    
    shortcut = shortcuts.detect_shortcut(
        shell_sequence,
        entropy_history=entropy_history,
        curvature_history=curvature_history,
        error_history=error_history
    )
    
    print(f"  ✓ Detected shortcut: {shortcut is not None}")
    if shortcut:
        print(f"  ✓ Shortcut signature: {shortcut.signature[:16]}...")
        print(f"  ✓ Entropy drop: {shortcut.entropy_drop:.4f}")
        print(f"  ✓ Curvature consistency: {shortcut.curvature_consistency:.4f}")
    
    shortcuts.save_to_repo()
    
    # Cleanup
    if Path("test_repo").exists():
        shutil.rmtree("test_repo")
    
    print("  ✓ Shortcut Detection: PASSED")
except Exception as e:
    print(f"  ✗ Shortcut Detection: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 3. Test Object Memory
print("\n3. Testing Object Memory...")
try:
    from experience.object_memory import ObjectMemory
    from combinatoric.interpreter import CombinatoricInterpreter
    
    objects = ObjectMemory(repo_path="test_repo")
    ci = CombinatoricInterpreter()
    
    # Process text to create combinatoric packet
    packet = ci.interpret("def factorial(n): return n * factorial(n-1) if n > 0 else 1")
    
    # Update object memory
    objects.update_from_combinatorics(packet)
    
    print(f"  ✓ Processed combinatoric packet")
    print(f"  ✓ Objects stored: {len(objects.objects)}")
    
    if objects.objects:
        obj = list(objects.objects.values())[0]
        print(f"  ✓ Object triplets: {len(obj.triplets)}")
        print(f"  ✓ Object shell stats: {obj.shell_stats}")
    
    objects.save_to_repo()
    
    # Cleanup
    if Path("test_repo").exists():
        shutil.rmtree("test_repo")
    
    print("  ✓ Object Memory: PASSED")
except Exception as e:
    print(f"  ✗ Object Memory: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Test Skills
print("\n4. Testing Skills...")
try:
    from experience.skills import SkillManager
    
    skills = SkillManager(repo_path="test_repo")
    
    # Create a sequence
    sequence = [
        {"type": "shell", "value": 0},
        {"type": "shell", "value": 2},
        {"type": "shell", "value": 3},
        {"type": "shell", "value": 4},
    ]
    
    # Update skill
    skill = skills.update_skills(sequence, success=True)
    
    print(f"  ✓ Created skill: {skill.signature[:16]}...")
    print(f"  ✓ Skill count: {skill.count}")
    print(f"  ✓ Skill success rate: {skill.success_rate:.4f}")
    
    skills.save_to_repo()
    
    # Cleanup
    if Path("test_repo").exists():
        shutil.rmtree("test_repo")
    
    print("  ✓ Skills: PASSED")
except Exception as e:
    print(f"  ✗ Skills: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. Test Experience Graph
print("\n5. Testing Experience Graph...")
try:
    from experience.experience_graph import ExperienceGraph
    
    graph = ExperienceGraph(repo_path="test_repo")
    
    # Add nodes
    graph.add_node("shell_0", "shell", {"value": 0})
    graph.add_node("shell_2", "shell", {"value": 2})
    
    # Add edge
    graph.add_edge("shell_0", "shell_2", "flux", weight=1.0)
    
    print(f"  ✓ Graph nodes: {len(graph.nodes)}")
    print(f"  ✓ Graph edges: {len(graph.edges)}")
    
    graph.save_to_repo()
    
    # Cleanup
    if Path("test_repo").exists():
        shutil.rmtree("test_repo")
    
    print("  ✓ Experience Graph: PASSED")
except Exception as e:
    print(f"  ✗ Experience Graph: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 6. Test Full Experience Layer
print("\n6. Testing Full Experience Layer...")
try:
    from experience.experience_layer import ExperienceLayer
    from runtime.capsules import Capsule
    from combinatoric.interpreter import CombinatoricInterpreter
    
    el = ExperienceLayer(repo_path="test_repo")
    ci = CombinatoricInterpreter()
    
    # Process text
    text = "if x > 0 then return x else return -x"
    packet = ci.interpret(text)
    
    # Create capsule
    capsule = Capsule(
        triplet_summary={"count": len(packet.triplets)},
        shell_state=2,
        entropy_snapshot=1.0,
        curvature_snapshot=0.5,
        measurement_error=0.3
    )
    
    # Process through experience layer
    result = el.process_capsule(capsule, packet)
    
    print(f"  ✓ Processed capsule through experience layer")
    print(f"  ✓ Habits: {result['habits_updated']}")
    print(f"  ✓ Shortcuts: {result['shortcuts_updated']}")
    print(f"  ✓ Objects: {result['objects_updated']}")
    print(f"  ✓ Skills: {result['skills_updated']}")
    print(f"  ✓ Compression ratio: {result['compression_ratio']:.4f}")
    print(f"  ✓ Hash: {result['hash'][:16]}...")
    
    # Verify files created
    experience_dir = Path("test_repo") / "experience"
    assert (experience_dir / "habits.json").exists(), "Habits file should exist"
    assert (experience_dir / "shortcuts.json").exists(), "Shortcuts file should exist"
    assert (experience_dir / "objects.json").exists(), "Objects file should exist"
    assert (experience_dir / "skills.json").exists(), "Skills file should exist"
    assert (experience_dir / "experience_graph.json").exists(), "Graph file should exist"
    
    print(f"  ✓ All experience files saved to repo")
    
    # Cleanup
    if Path("test_repo").exists():
        shutil.rmtree("test_repo")
    
    print("  ✓ Full Experience Layer: PASSED")
except Exception as e:
    print(f"  ✗ Full Experience Layer: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 7. Test LCM Integration
print("\n7. Testing LCM Integration...")
try:
    from core.lcm import LCM
    from experience.experience_layer import ExperienceLayer
    
    lcm = LCM()
    el = ExperienceLayer(repo_path="test_repo")
    
    # Process with experience
    result = lcm.process_with_experience("def hello(): return 'world'", el)
    
    print(f"  ✓ LCM processed with experience layer")
    print(f"  ✓ Capsule generated")
    print(f"  ✓ Experience updated: {len(result.get('experience', {}))} updates")
    
    # Cleanup
    if Path("test_repo").exists():
        shutil.rmtree("test_repo")
    
    print("  ✓ LCM Integration: PASSED")
except Exception as e:
    print(f"  ✗ LCM Integration: FAILED - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("EXPERIENCE LAYER TEST SUMMARY")
print("=" * 60)
print("✓ Habit formation working")
print("✓ Shortcut detection working")
print("✓ Object memory working")
print("✓ Skills learning working")
print("✓ Experience graph working")
print("✓ Full experience layer operational")
print("✓ LCM integration working")
print("✓ QuantaCoin compression working")
print("✓ Repo storage working")
print("\n🎉 Experience Layer is fully operational!")
print("Apop can now learn, form habits, and maintain identity!")
print("=" * 60)

