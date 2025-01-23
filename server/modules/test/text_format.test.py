import unittest
import config
from clock_str import make_plural

class TextFormatting(unittest.TestCase):
    def test_text_formatting(self):
        clock_out_data_m = config.clock_out_data_message.format(
            date='2023-08-09',
            user_name='John Doe', 
            hours='1',
            hours_s=make_plural(1),
            minutes='2',
            minutes_s=make_plural(2),
            meeting_hours='3',
            meeting_hours_s=make_plural(3),
            meeting_minutes='4',
            meeting_minutes_s=make_plural(4),
            break_hours='5',
            break_hours_s=make_plural(5),
            break_minutes='6',
            break_minutes_s=make_plural(6)
        ).replace('\\n', '\n')
        expected = '2023-08-09 - John Doe has clocked out.\n**Business Hours**\n1 hour and 2 minutes\n**Meeting Time**\n3 hours and 4 minutes\n**Break Time**\n5 hours and 6 minutes'
        self.assertEqual(clock_out_data_m, expected)

if __name__ == '__main__':
    unittest.main()