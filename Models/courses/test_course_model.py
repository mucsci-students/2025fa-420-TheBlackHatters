# Run with pytest -q from inside courses directory.

import pytest
from Course_model import (
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


def test_to_dict_omit_empty():
    c = Course("CS101", 3)
    d = c.to_dict(omit_empty=True)
    assert d["course_id"] == "CS101"
    assert d["credits"] == 3
    assert "room" not in d
    assert "lab" not in d


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
        {"course_id": "CMSC 141", "credits": 4, "room": ["Roddy 140"], "lab": ["Windows"]},
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

    with pytest.raises(ValueError):
        modify_course_in_config(cfg, "CMSC 150", updates={"course_id": "CMSC 140"})


def test_delete_course_from_config():
    cfg = sample_inner_config()
    add_course_to_config(cfg, {"course_id": "CMSC 150", "credits": 4})
    removed = delete_course_from_config(cfg, "CMSC 150")
    assert removed["course_id"] == "CMSC 150"
    with pytest.raises(ValueError):
        delete_course_from_config(cfg, "CMSC 150")