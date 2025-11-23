import unittest
from Models.Timeslots_model import validate_time, TimeSlotModel

class TestValidateTime(unittest.TestCase):
    def test_valid_times(self):
        """Adding a valid time format should not raise an error."""
        self.assertTrue(validate_time("00:00"))
        self.assertTrue(validate_time("23:59"))
        self.assertTrue(validate_time("09:30"))

    def test_invalid_format(self):
        """Adding an invalid time format should raise an error."""
        self.assertFalse(validate_time("9:00"))
        self.assertFalse(validate_time("123:00"))
        self.assertFalse(validate_time("aa:bb"))
        self.assertFalse(validate_time("12-00"))

    def test_invalid_values(self):
        """Adding invalid values should also raise errors."""
        self.assertFalse(validate_time("24:00"))
        self.assertFalse(validate_time("12:60"))
        self.assertFalse(validate_time("99:99"))

class TestTimeSlotModel(unittest.TestCase):
    def setUp(self):
        # Sets up an example timeslot for tests.
        self.model = TimeSlotModel({"times": {"MON": [{"start": "08:00", "spacing": 60, "end": "12:00"}]}})

    def test_list_slots(self):
        """Slots for that day should be printed."""
        self.assertEqual(len(self.model.list_slots("MON")), 1)
        self.assertEqual(self.model.list_slots("TUE"), [])

    def test_add_slot_valid(self):
        """Adding a valid slot should result in the established test timeslot having an additional slot with those qualtities."""
        self.model.add_slot("TUE", "09:00", 30, "10:00")
        slots = self.model.list_slots("TUE")
        self.assertEqual(len(slots), 1)
        self.assertEqual(slots[0]["start"], "09:00")
        self.assertEqual(slots[0]["spacing"], 30)
        self.assertEqual(slots[0]["end"], "10:00")

    def test_add_slot_invalid(self):
        """Adding an invalid slot should result in an error and no slot addition."""
        with self.assertRaises(ValueError):
            self.model.add_slot("WED", "99:00", 30, "10:00")
        with self.assertRaises(ValueError):
            self.model.add_slot("WED", "09:00", 30, "25:00")

    def test_edit_slot_valid(self):
        """Properly editing a slot should result in that slot being changed to the new information."""
        self.model.edit_slot("MON", 0, start="09:00", end="11:00", spacing=45)
        slot = self.model.list_slots("MON")[0]
        self.assertEqual(slot["start"], "09:00")
        self.assertEqual(slot["end"], "11:00")
        self.assertEqual(slot["spacing"], 45)

    def test_edit_slot_invalid_index(self):
        """Using an invalid index when editing a slot should throw an error."""
        with self.assertRaises(IndexError):
            self.model.edit_slot("MON", 5, start="10:00")
        with self.assertRaises(IndexError):
            self.model.edit_slot("FRI", 0, start="10:00")

    def test_edit_slot_invalid_time(self):
        """Using an invalid time when editing a slot should throw an error."""
        with self.assertRaises(ValueError):
            self.model.edit_slot("MON", 0, start="99:00")
        with self.assertRaises(ValueError):
            self.model.edit_slot("MON", 0, end="99:00")

    def test_delete_slot_valid(self):
        """Providing valid index when deleting a slot should result in the slot's removal."""
        deleted = self.model.delete_slot("MON", 0)
        self.assertEqual(deleted["start"], "08:00")
        self.assertEqual(self.model.list_slots("MON"), [])

    def test_delete_slot_invalid(self):
        """Providing an invalid index while deleting a slot should throw an error."""
        with self.assertRaises(IndexError):
            self.model.delete_slot("MON", 5)
        with self.assertRaises(IndexError):
            self.model.delete_slot("FRI", 0)