import unittest
from stocktrace.util import slf4p

logger = slf4p.getLogger(__name__)

class TestSequenceFunctions(unittest.TestCase):

    def test_diff_text_file(self):
        list1 = []
        with open("old_xm.txt") as f:
            list1 = f.readlines()
        logger.debug(len(list1))
        list2 = []
        with open("new_xm2.txt") as f:
            list2 = f.readlines()
        logger.debug(len(list2))
        diff_list = list(set(list1) - set(list2))
        logger.debug(len(diff_list))
        for xm in diff_list:
            logger.debug(xm)


