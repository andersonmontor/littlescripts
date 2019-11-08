import unittest as ut 
import stopwatch as sw

# TODO: ver se tem forma mais "enxuta" de codificar os testes sem repetir muito codigo (pytest maybe)
class TestTimer(ut.TestCase):

	def test_pb(self):
		params = [80, 1000, 500, "teste: "]
		expected_output = "teste: [XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX----------------------------------] 50%"
		self.assertEqual(sw.progress_bar(*params), expected_output)



if __name__ == '__main__':
	ut.main()