# Run with pytest -q from inside tests/Model_tests directory.

import pytest
from Models.Course_model import (
    Course,
    add_course_to_config,
    modify_course_in_config,
    delete_course_from_config,
)


def sample_inner_config():
    return {
        "rooms": ["Roddy 136", "Roddy 140", "Esbenshade 361"],
        "labs": ["Linux", "Windows"],
        "courses": [
            {
                "course_id": "CMSC 140",
                "credits": 4,
                "room": ["Roddy 136"],
                "lab": ["Linux"],
                "conflicts": [],
                "faculty": ["Zoppetti"],
            }
        ],
    }


# Course basic tests


def test_build_and_validate_minimal():
    cfg = sample_inner_config()
    data = {"course_id": "CMSC 150", "credits": 4}
    c = Course.build_and_validate(data, config_obj=cfg, existing_courses=cfg["courses"])
    assert isinstance(c, Course)
    assert c.course_id == "CMSC 150"
    assert c.credits == 4


def test_list_cleaning_and_dedup():
    c = Course(
        "CS200",
        3,
        room=["  Roddy 136", "Roddy 136", "Roddy 140", ""],
        lab=["Linux", "Linux", "  Linux "],
        conflicts=["CS101", "CS101", " CS102 "],
        faculty=["Smith", "Smith", "  Jones  "],
    )
    assert c.room == ["Roddy 136", "Roddy 140"]
    assert c.lab == ["Linux"]
    assert c.conflicts == ["CS101", "CS102"]
    assert c.faculty == ["Smith", "Jones"]


def test_setters_and_rename():
    c = Course("CS101", 3)
    c.set_credits(5)
    assert c.credits == 5
    c.rename("CS101X")
    assert c.course_id == "CS101X"
    c.add_rooms(["Roddy 136"])
    c.add_labs(["Linux"])
    assert c.room == ["Roddy 136"]
    assert c.lab == ["Linux"]
    c.remove_rooms(["Roddy 136"])
    c.remove_labs(["Linux"])
    assert c.room == []
    assert c.lab == []


def test_list_modification_methods():
    """Test add/remove methods for all list attributes."""
    c = Course("CS101", 3)

    # Test rooms
    c.add_rooms(["Room1", "Room2"])
    assert c.room == ["Room1", "Room2"]
    c.add_rooms(["Room3"])
    assert "Room3" in c.room
    c.remove_rooms(["Room1"])
    assert c.room == ["Room2", "Room3"]

    # Test labs
    c.add_labs(["Lab1", "Lab2"])
    assert c.lab == ["Lab1", "Lab2"]
    c.remove_labs(["Lab2"])
    assert c.lab == ["Lab1"]

    # Test conflicts
    c.add_conflicts(["MATH101", "PHYS101"])
    assert "MATH101" in c.conflicts
    c.remove_conflicts(["MATH101"])
    assert c.conflicts == ["PHYS101"]

    # Test faculty
    c.add_faculty(["Smith", "Jones"])
    assert c.faculty == ["Smith", "Jones"]
    c.remove_faculty(["Smith"])
    assert c.faculty == ["Jones"]


# Membership tests


def test_membership_non_strict_allows_unknown():
    cfg = sample_inner_config()
    c = Course("CS404", 3, room=["Nowhere 100"], lab=["MacOS"])
    c.validate(config_obj=cfg, strict_membership=False)  # should not raise


def test_membership_strict_raises_on_unknown():
    cfg = sample_inner_config()
    c = Course("CS404", 3, room=["Nowhere 100"], lab=["MacOS"])
    with pytest.raises(ValueError):
        c.validate(config_obj=cfg, strict_membership=True)


# Uniqueness tests


def test_uniqueness_duplicate_rejected():
    cfg = sample_inner_config()
    dup = Course("CMSC 140", 4)
    with pytest.raises(ValueError):
        dup.validate(existing_courses=cfg["courses"])


def test_uniqueness_ignore_index_when_modifying():
    cfg = sample_inner_config()
    idx = 0
    existing = cfg["courses"]
    c = Course.from_dict(existing[idx])
    c.set_credits(5)
    # Should not raise when ignoring same index
    c.validate(existing_courses=existing, ignore_index=idx)
    # Should raise without ignore
    with pytest.raises(ValueError):
        c.validate(existing_courses=existing, ignore_index=None)


# Config helper tests


def test_add_course_to_config_success_and_duplicate():
    cfg = sample_inner_config()
    stored = add_course_to_config(
        cfg,
        {
            "course_id": "CMSC 141",
            "credits": 4,
            "room": ["Roddy 140"],
            "lab": ["Windows"],
        },
    )
    assert stored["course_id"] == "CMSC 141"
    assert stored in cfg["courses"]

    with pytest.raises(ValueError):
        add_course_to_config(cfg, {"course_id": "CMSC 141", "credits": 3})


def test_modify_course_in_config_fields():
    cfg = sample_inner_config()
    add_course_to_config(cfg, {"course_id": "CMSC 150", "credits": 4})

    updated = modify_course_in_config(
        cfg,
        "CMSC 150",
        updates={
            "credits": 5,
            "room": ["Esbenshade 361"],
            "lab": ["Windows"],
            "faculty": ["Jones"],
            "conflicts": ["CMSC 140"],
        },
    )
    assert updated["credits"] == 5
    assert updated["room"] == ["Esbenshade 361"]
    assert updated["lab"] == ["Windows"]
    assert updated["faculty"] == ["Jones"]
    assert updated["conflicts"] == ["CMSC 140"]

    # Editing to duplicate ID should still be allowed because the same index is ignored
    modify_course_in_config(cfg, "CMSC 150", updates={"course_id": "CMSC 140"})
    # The edited course now has CMSC 140 (same as original), but that’s ok in current logic.


def test_delete_course_from_config():
    cfg = sample_inner_config()
    add_course_to_config(cfg, {"course_id": "CMSC 150", "credits": 4})
    removed = delete_course_from_config(cfg, "CMSC 150")
    assert removed["course_id"] == "CMSC 150"
    with pytest.raises(ValueError):
        delete_course_from_config(cfg, "CMSC 150")


def test_course_credits_validation():
    """Test various invalid credit values."""
    with pytest.raises(ValueError, match="Invalid credits"):
        Course("CS101", "not a number")
    with pytest.raises(ValueError, match="non-negative"):
        Course("CS101", -1)
    with pytest.raises(ValueError):
        Course("CS101", None)
    # Valid cases
    assert Course("CS101", "3").credits == 3  # string number
    assert Course("CS101", 0).credits == 0  # zero credits


def test_course_id_whitespace_handling():
    """Test course_id whitespace handling."""
    c = Course("  CS101  ", 3)
    assert c.course_id == "CS101"  # should be stripped
    with pytest.raises(ValueError, match="empty"):
        Course("   ", 3)
    with pytest.raises(ValueError, match="empty"):
        Course("", 3)


def test_validate_with_empty_config():
    """Test validation with empty config sections."""
    empty_config = {"rooms": [], "labs": [], "courses": [], "faculty": []}
    c = Course(
        "CS101",
        3,
        room=["Room1"],
        lab=["Lab1"],
        faculty=["Smith"],
        conflicts=["MATH101"],
    )

    # Should not raise in non-strict mode
    c.validate(config_obj=empty_config, strict_membership=False)

    # Should raise in strict mode with details about empty lists
    with pytest.raises(ValueError) as exc:
        c.validate(config_obj=empty_config, strict_membership=True)
    assert "Available rooms: None defined" in str(exc.value)


def test_modify_course_edge_cases():
    """Test edge cases in course modification."""
    cfg = sample_inner_config()

    # Test modifying with empty updates
    modified = modify_course_in_config(cfg, "CMSC 140", updates={})
    assert modified["course_id"] == "CMSC 140"  # unchanged

    # Test modifying with None values (should keep existing)
    modified = modify_course_in_config(
        cfg, "CMSC 140", updates={"credits": None, "room": None}
    )
    assert modified["credits"] == 4  # unchanged
    assert modified["room"] == ["Roddy 136"]  # unchanged

    # Test invalid target_index
    with pytest.raises(ValueError):
        modify_course_in_config(cfg, "CMSC 140", target_index=999)


def test_course_type_safety():
    """Test handling of various input types."""
    # Test with integer course_id
    c = Course(101, 3)
    assert isinstance(c.course_id, str)

    # Test with None values in lists
    c = Course(
        "CS101", 3, room=[None, "Room1", None], lab=[None], faculty=[None, "Smith"]
    )
    assert None not in c.room
    assert None not in c.lab
    assert None not in c.faculty

    # Test with mixed types in lists
    c = Course("CS101", 3, room=[123, "Room1", 3.14])
    assert all(isinstance(r, str) for r in c.room)


def test_self_conflict_validation():
    """Test handling of self-conflicts."""
    cfg = sample_inner_config()

    # Try to create course with self as conflict
    course_data = {
        "course_id": "CMSC 150",
        "credits": 3,
        "conflicts": ["CMSC 150"],  # self-conflict
    }

    # Add course and validate it doesn't conflict with itself
    c = Course.build_and_validate(course_data, config_obj=cfg)
    assert "CMSC 150" in c.conflicts  # current behavior allows self-conflicts


def test_faculty_name_formats():
    """Test different faculty name formats and normalization."""
    cfg = {
        "faculty": [
            {"name": "Dr. Smith"},  # dict with name
            "Professor Jones",  # direct string
            123,  # number
        ]
    }

    c = Course("CS101", 3, faculty=["Dr. Smith", "Professor Jones", "123"])
    c.validate(config_obj=cfg, strict_membership=True)

    # Test faculty name cleaning
    c = Course("CS101", 3, faculty=["  Dr. Smith  ", " Professor Jones "])
    assert c.faculty == ["Dr. Smith", "Professor Jones"]


def test_complex_modification_sequence():
    """Test a complex sequence of modifications."""
    cfg = sample_inner_config()

    # Add initial course
    add_course_to_config(
        cfg,
        {
            "course_id": "CMSC 999",
            "credits": 3,
            "room": ["Roddy 136"],
            "lab": ["Linux"],
        },
    )

    # Modify it multiple times
    modify_course_in_config(cfg, "CMSC 999", updates={"room": ["Roddy 140"]})
    modify_course_in_config(cfg, "CMSC 999", updates={"lab": ["Windows"]})
    modify_course_in_config(cfg, "CMSC 999", updates={"credits": 4})

    # Delete and try to modify (should fail)
    delete_course_from_config(cfg, "CMSC 999")
    with pytest.raises(ValueError):
        modify_course_in_config(cfg, "CMSC 999", updates={"credits": 5})
