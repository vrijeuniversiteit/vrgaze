from unittest import TestCase

from vrgaze.tennis.services.io.read import Reader, Validator


class TestReader(TestCase):
    def setUp(self):
        self.reader = Reader()


class TestDiscoverFiles(TestReader):
    def test_should_discover_example_file(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/single_example_file")
        self.assertEqual(self.reader.number_files, 1)


class TestReadFiles(TestReader):
    def test_should_find_two_trials(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/single_example_file")
        self.reader.read_files()
        self.assertEqual(len(self.reader.participants[0].trials), 2)

    def test_should_have_232_frames_for_first_trial(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/single_example_file")
        self.reader.read_files()
        self.assertEqual(len(self.reader.participants[0].trials[0].frames), 232)

    def test_should_read_ball_position_x_for_both_trials(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/experimental_condition")
        self.reader.read_files()

        first_trial_first_position = 0.00626
        first_trial_last_position = -1.627846
        second_trial_first_position = 0.0054250
        second_trial_last_position = -0.193335

        self.assertAlmostEqual(
            self.reader.participants[0].trials[0].frames[0].ball_position_x,
            first_trial_first_position,
            delta=0.000001
        )
        self.assertAlmostEqual(
            self.reader.participants[0].trials[0].frames[-1].ball_position_x,
            first_trial_last_position,
            delta=0.000001
        )
        self.assertAlmostEqual(
            self.reader.participants[0].trials[1].frames[0].ball_position_x,
            second_trial_first_position,
            delta=0.000001
        )
        self.assertAlmostEqual(
            self.reader.participants[0].trials[1].frames[-1].ball_position_x,
            second_trial_last_position,
            delta=0.000001
        )

    def test_should_read_column_tobii_gazeray_is_valid(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/experimental_condition")
        self.reader.read_files()
        first_trial_first_frame = self.reader.participants[0].trials[0].frames[0].gaze_is_valid
        first_occurrence_false = self.reader.participants[0].trials[0].frames[171].gaze_is_valid

        self.assertTrue(first_trial_first_frame)
        self.assertFalse(first_occurrence_false)

    def test_should_read_tobii_gazeray_origin_x_for_both_trials(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/single_example_file")
        self.reader.read_files()

        first_trial_first_position = 0.1023313
        first_trial_last_position = 0.1708458
        second_trial_first_position = 0.127413
        second_trial_last_position = 0

        self.assertAlmostEqual(
            self.reader.participants[0].trials[0].frames[0].gaze_origin_x,
            first_trial_first_position,
            delta=0.000001
        )
        self.assertAlmostEqual(
            self.reader.participants[0].trials[0].frames[-1].gaze_origin_x,
            first_trial_last_position, delta=0.000001
        )
        self.assertAlmostEqual(
            self.reader.participants[0].trials[1].frames[0].gaze_origin_x,
            second_trial_first_position, delta=0.000001
        )
        self.assertAlmostEqual(
            self.reader.participants[0].trials[1].frames[-1].gaze_origin_x,
            second_trial_last_position, delta=0.000001
        )

    def test_should_find_two_participants(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/experimental_condition")
        self.reader.read_files()
        self.assertEqual(len(self.reader.participants), 2)

    def test_should_increment_participant_id(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/experimental_condition")
        self.reader.read_files()
        self.assertEqual(self.reader.participants[0].participant_id, 1)
        self.assertEqual(self.reader.participants[1].participant_id, 2)

    def test_should_read_tobii_gazeorigin_and_direction(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/experimental_condition")
        self.reader.read_files()
        first_frame = self.reader.participants[0].trials[0].frames[0]
        self.assertEqual(first_frame.gaze_origin_x, 0.1023313)
        self.assertEqual(first_frame.gaze_origin_y, 1.76664)
        self.assertEqual(first_frame.gaze_origin_z, -11.76237)
        self.assertEqual(first_frame.gaze_direction_x, -0.01645234)
        self.assertEqual(first_frame.gaze_direction_y, 0.05927261)
        self.assertEqual(first_frame.gaze_direction_z, 0.9981007)

    def test_should_read_results_location(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/single_example_file")
        self.reader.read_files()
        result_x = self.reader.participants[0].trials[0].result_location_x
        result_y = self.reader.participants[0].trials[0].result_location_y
        result_z = self.reader.participants[0].trials[0].result_location_z
        self.assertEqual(result_x, -2.881121)
        self.assertEqual(result_y, 0.03343761)
        self.assertEqual(result_z, 12.05697)

    def test_should_read_result_distance_to_closest_target(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/single_example_file")
        self.reader.read_files()
        result = self.reader.participants[0].trials[0].distance_to_closest_target
        self.assertEqual(result, 3.108663)

    def test_should_convert_timestamps_to_seconds_starting_at_0(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/single_example_file")
        self.reader.read_files()
        first_frame = self.reader.participants[0].trials[0].frames[0]
        self.assertEqual(first_frame.timestamp, 0.0)

    def test_timestamps_for_each_trial_should_commence_at_0(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/single_example_file")
        self.reader.read_files()
        self.assertEqual(self.reader.participants[0].trials[0].frames[0].timestamp, 0.0)
        self.assertEqual(self.reader.participants[0].trials[1].frames[0].timestamp, 0.0)

    def test_timestamps_should_show_delta_seconds_between_frames(self):
        self.reader.discover_files("vrgaze/example_data/tennis_data/single_example_file")
        self.reader.read_files()
        self.assertAlmostEqual(self.reader.participants[0].trials[0].frames[1].timestamp, 0.011, delta=0.001)


class TestValidator(TestCase):
    def test_should_throw_error_if_header_is_different(self):
        expected_header = 'participant_id,test_id,block_number,ball_number,timestamp,ball_position_x,ball_position_y,' \
                          'ball_position_z,shortest_path_normalized_x,shortest_path_normalized_y,shortest_path_normalized_z,look_direction_normalized_x,look_direction_normalized_y,look_direction_normalized_z,result_location_x,result_location_y,result_location_z,target_type,distance_to_closest_target,smi_camera_raycast_x,smi_camera_raycast_y,smi_camera_raycast_z,smi_binocular_por_x,smi_binocular_por_y,smi_binocular_por_is_valid,smi_ipd,smi_ipd_is_valid,smi_left_por_x,smi_left_por_y,smi_left_por_is_valid,smi_right_por_x,smi_right_por_y,smi_right_por_is_valid,smi_left_basepoint_x,smi_left_basepoint_y,smi_left_basepoint_z,smi_left_basepoint_is_valid,smi_right_basepoint_x,smi_right_basepoint_y,smi_right_basepoint_z,smi_right_basepoint_is_valid,smi_left_gazedirection_x,smi_left_gazedirection_y,smi_left_gazedirection_z,smi_left_gazedirection_is_valid,smi_right_gazedirection_x,smi_right_gazedirection_y,smi_right_gazedirection_z,smi_right_gazedirection_is_valid,tobii_gazeray_isvalid,tobii_gazeray_origin_x,tobii_gazeray_origin_y,tobii_gazeray_origin_z,tobii_gazeray_direction_x,tobii_gazeray_direction_y,tobii_gazeray_direction_z,tobii_left_pupil_isvalid,tobii_left_pupildiameter,tobii_left_ray_isvalid,tobii_left_ray_origin_x,tobii_left_ray_origin_y,tobii_left_ray_origin_z,tobii_left_ray_direction_x,tobii_left_ray_direction_y,tobii_left_ray_direction_z,tobii_right_pupil_isvalid,tobii_right_pupildiameter,tobii_right_ray_isvalid,tobii_right_ray_origin_x,tobii_right_ray_origin_y,tobii_right_ray_origin_z,tobii_right_ray_direction_x,tobii_right_ray_direction_y,tobii_right_ray_direction_z,participant_head_position_x,participant_head_position_y,participant_head_position_z,participant_head_rotation_x,participant_head_rotation_y,participant_head_rotation_z,racket_knob_position_x,racket_knob_position_y,racket_knob_position_z,racket_knob_rotation_x,racket_knob_rotation_y,racket_knob_rotation_z\n'
        actual_header = "wrong_header"

        self.assertRaises(ValueError, Validator.validate_header, expected_header, actual_header)
