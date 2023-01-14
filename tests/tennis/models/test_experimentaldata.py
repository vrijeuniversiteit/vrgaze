from unittest import TestCase
from unittest.mock import MagicMock

from vrgaze.tennis.models.datamodel import ConditionData
from vrgaze.tennis import ExperimentalData


class TestExperimentalData(TestCase):
    def test_constructor_with_list(self):
        mock_data = MagicMock(spec=ConditionData)
        data = [mock_data, mock_data, mock_data]
        ed = ExperimentalData(data)
        self.assertEqual(ed.conditions, data)

    def test_constructor_with_one_condition(self):
        mock_data = MagicMock(spec=ConditionData)
        ed = ExperimentalData(mock_data)
        self.assertEqual(ed.conditions, [mock_data])
