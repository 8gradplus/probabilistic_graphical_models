from unittest import TestCase
import numpy as np
from helper.add_numpy_axis import add_axis


class TestAddAxis(TestCase):

    def test_add_one_axis_add_the_end_of_2d_array(self):
        a = np.ones(shape=(2, 2))
        indices = [10, 12]
        indices_ext = [10, 12, 14]
        self.assertEqual(add_axis(a, indices, indices_ext).shape, (2, 2, 1))

    def test_add_one_axis_in_the_middle_of_2d_array(self):
        a = np.ones(shape=(2, 2))
        indices = [10, 12]
        indices_ext = [10, 11, 12]
        self.assertEqual(add_axis(a, indices, indices_ext).shape, (2, 1, 2))

    def test_add_one_axis_at_beginning_of_2d_array(self):
        a = np.ones(shape=(2, 2))
        indices = [10, 12]
        indices_ext = [7, 10, 12]
        self.assertEqual(add_axis(a, indices, indices_ext).shape, (1, 2, 2))

    def test_add_two_axis_at_beginning_of_2d_array(self):
        a = np.ones(shape=(2, 2))
        indices = [10, 12]
        indices_ext = [5, 7, 10, 12]
        self.assertEqual(add_axis(a, indices, indices_ext).shape, (1, 1, 2, 2))

    def test_add_two_axis_at_end_of_2d_array(self):
        a = np.ones(shape=(2, 2))
        indices = [10, 12]
        indices_ext = [10, 12, 13, 14]
        self.assertEqual(add_axis(a, indices, indices_ext).shape, (2, 2, 1, 1))

    def test_some_crazy_axis_insertions(self):
        a = np.ones(shape=(2, 2))
        indices = [10, 12]
        indices_ext = [7, 10, 11, 12, 13, 14]
        self.assertEqual(add_axis(a, indices, indices_ext).shape, (1, 2, 1, 2, 1, 1))

    def test_axis_insertion_should_raise_error_if_pixels_is_not_a_subset_of_extended_pixels(self):
        a = np.ones(shape=(2, 2))
        indices = [5, 10, 12]
        indices_ext = [7, 10, 11, 12, 13, 14]
        self.assertRaises(AssertionError, lambda: add_axis(a, indices, indices_ext))