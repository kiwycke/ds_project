import unittest as ut
from unittest import mock
from statistics_bikeshare import StatisticsBikeshare
from statistics_bikeshare import InvalidInput

class TestStatisticsBikeshare(ut.TestCase):
	@mock.patch('statistics_bikeshare.input', create=True)
	def test_bulk_check(self, mocked_input):
		print('='*24+' Testing bulk_check() ' + '='*24)

		mocked_input.side_effect = ['asd', 'y', 'yes', 'n', 'no']
		bike_stat = StatisticsBikeshare()

		bike_stat.bulk_check()
		self.assertRaises(InvalidInput)

		self.assertEqual(bike_stat.bulk, True)

		bike_stat.bulk_check()
		self.assertEqual(bike_stat.bulk, True)

		bike_stat.bulk_check()
		self.assertEqual(bike_stat.bulk, False)

		bike_stat.bulk_check()
		self.assertEqual(bike_stat.bulk, False)

		print('='*24+' END Testing bulk_check() ' + '='*24 + '\n')
			
	@mock.patch('statistics_bikeshare.input', create=True)
	def test_want_filter(self, mocked_input):
		print('='*24+' Testing want_filter() ' + '='*24)

		mocked_input.side_effect = ['asd', 'y', 'yes', 'n', 'no']
		bike_stat = StatisticsBikeshare()

		res = bike_stat.want_filter()
		self.assertRaises(InvalidInput)

		self.assertEqual(res, True)

		self.assertEqual(bike_stat.want_filter(), True)

		self.assertEqual(bike_stat.want_filter(), False)

		self.assertEqual(bike_stat.want_filter(), False)

		print('='*24+' END Testing want_filter() ' + '='*24 + '\n')


	def test_map_input_to_days(self):
		print('='*24+' Testing map_input_to_days() ' + '='*24)

		bike_stat = StatisticsBikeshare()

		input_days_0 = {'a'}
		expected_days_0 = {'m', 't', 'w', 'th', 'f', 's', 'su'}
		self.assertEqual(bike_stat.map_input_to_days(input_days_0), expected_days_0)

		input_days_1 = {'a', 'wdays', 't', 't'}
		expected_days_1 = {'m', 't', 'w', 'th', 'f', 's', 'su'}
		self.assertEqual(bike_stat.map_input_to_days(input_days_1), expected_days_1)

		input_days_2 = {'wdays'}
		expected_days_2 = {'m', 't', 'w', 'th', 'f'}
		self.assertEqual(bike_stat.map_input_to_days(input_days_2), expected_days_2)

		input_days_3 = {'wdays', 's', 's'}
		expected_days_3 = {'m', 't', 'w', 'th', 'f', 's'}
		self.assertEqual(bike_stat.map_input_to_days(input_days_3), expected_days_3)

		input_days_4 = {'wends'}
		expected_days_4 = {'s', 'su'}
		self.assertEqual(bike_stat.map_input_to_days(input_days_4), expected_days_4)

		input_days_5 = {'wends', 't', 'm'}
		expected_days_5 = {'m', 't', 's', 'su'}
		self.assertEqual(bike_stat.map_input_to_days(input_days_5), expected_days_5)

		input_days_6 = {'wends', 'wdays'}
		expected_days_6 = {'m', 't', 'w', 'th', 'f', 's', 'su'}
		self.assertEqual(bike_stat.map_input_to_days(input_days_6), expected_days_6)

		input_days_7 = {'wends', 'wdays', 'a'}
		expected_days_7 = {'m', 't', 'w', 'th', 'f', 's', 'su'}
		self.assertEqual(bike_stat.map_input_to_days(input_days_7), expected_days_7)

		input_days_8 = {'wends', 'wdays', 'wends', 'wdays', 'a', 'a'}
		expected_days_8 = {'m', 't', 'w', 'th', 'f', 's', 'su'}
		self.assertEqual(bike_stat.map_input_to_days(input_days_8), expected_days_8)

		print('='*24+' END Testing map_input_to_days() ' + '='*24 + '\n')

	def test_col_check(self):
		print('='*24+' Testing col_check() ' + '='*24)

		bike_stat = StatisticsBikeshare()
		bike_stat.df = bike_stat.df.reindex(columns = ['Start Time', 'End Time', 'Start Station', 'End Station'])

		self.assertEqual(bike_stat.col_check('Start Time'), True)

		self.assertEqual(bike_stat.col_check('End Time'), True)

		self.assertEqual(bike_stat.col_check('Start Station'), True)

		self.assertEqual(bike_stat.col_check('End Station'), True)

		self.assertEqual(bike_stat.col_check('Trip Duration'), False)

		self.assertEqual(bike_stat.col_check('Gender'), False)

		print('='*24+' END Testing col_check() ' + '='*24 + '\n')

	@mock.patch('statistics_bikeshare.input', create=True)
	def test_get_filters(self, mocked_input):
		print('='*24+' Testing get_filters() ' + '='*24)

		bike_stat = StatisticsBikeshare()

		expected_cities_0 = ['chicago', 'new york city', 'washington']
		expected_months_0 = ['1', '2', '3', '4', '5', '6']
		expected_days_0 = ['Friday', 'Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday']

		mocked_input.side_effect = ['y', 'n']
		input_cities_0, input_months_0, input_days_0 = bike_stat.get_filters()
		self.assertEqual(sorted(input_cities_0), expected_cities_0)
		self.assertEqual(sorted(input_months_0), expected_months_0)
		self.assertEqual(sorted(input_days_0), expected_days_0)

		mocked_input.side_effect = ['y', 'y', 'a', 'a', 'a']
		input_cities_1, input_months_1, input_days_1 = bike_stat.get_filters()
		self.assertEqual(sorted(input_cities_1), expected_cities_0)
		self.assertEqual(sorted(input_months_1), expected_months_0)
		self.assertEqual(sorted(input_days_1), expected_days_0)


		expected_cities_1 = ['chicago']
		expected_months_1 = ['2', '3']
		expected_days_1 = ['Saturday', 'Sunday']

		mocked_input.side_effect = ['y', 'y', 'c', '2 3', 'wends']
		input_cities_2, input_months_2, input_days_2 = bike_stat.get_filters()
		self.assertEqual(sorted(input_cities_2), expected_cities_1)
		self.assertEqual(sorted(input_months_2), expected_months_1)
		self.assertEqual(sorted(input_days_2), expected_days_1)

		mocked_input.side_effect = ['n', 'n', '\n']
		input_cities_3, input_months_3, input_days_3 = bike_stat.get_filters()
		self.assertEqual(sorted(input_cities_3), expected_cities_0)
		self.assertEqual(sorted(input_months_3), expected_months_0)
		self.assertEqual(sorted(input_days_3), expected_days_0)

		print('='*24+' END Testing get_filters() ' + '='*24 + '\n')

	def test_secure_input(self):
		print('='*24+' Testing secure_input() ' + '='*24)

		bike_stat = StatisticsBikeshare()

		input_cities_0 = {'W', 'N'}
		expected_cities_0 = {'w', 'n'}
		self.assertEqual(bike_stat.secure_input(input_cities_0), expected_cities_0)

		input_months_0 = {'A', '1', '5'}
		expected_months_0 = {'a', '1', '5'}
		self.assertEqual(bike_stat.secure_input(input_months_0), expected_months_0)

		input_days_0 = {'M', 'tH'}
		expected_days_0 = {'m', 'th'}
		self.assertEqual(bike_stat.secure_input(input_days_0), expected_days_0)

		print('='*24+' END Testing secure_input() ' + '='*24)


if __name__ == '__main__':
    ut.main()