import tenseal as ts
from utils import compute_he_mean, compute_he_variance, compute_he_covariance
import numpy as np
import unittest

class TestHEComputations(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.he_context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60]
        )
        self.he_context.global_scale = 2**40
        self.he_context.generate_galois_keys()

    def test_compute_he_mean(self):
        message = [2,3,4,5,2,9]
        count = len(message)
        expected_mean = sum(message) / count
        
        c = ts.ckks_vector(self.he_context, message)
        encrypted_mean = compute_he_mean(c, count)
        decrypted_result = encrypted_mean.decrypt()[0]
        self.assertAlmostEqual(decrypted_result, expected_mean, places=3)

    def test_compute_he_variance(self):
        message = [120, 70, 90, 40]
        count = len(message)
        expected_variance = np.var(message)
        c = ts.ckks_vector(self.he_context, message)
        
        enc_result = compute_he_variance(c, count)
        decrypted_result = enc_result.decrypt()[0]
        self.assertAlmostEqual(decrypted_result, expected_variance, places=3)
        
    def test_compute_he_covariance(self):
        x = [1, 2, 3, 4]
        y = [2, 3, 4, 5]
        count = len(x)
        cov_matrix = np.cov(x, y, ddof=0) 
        expected_covariance = cov_matrix[0][1]
        
        enc_x = ts.ckks_vector(self.he_context, x)
        enc_y = ts.ckks_vector(self.he_context, y)
        enc_covariance = compute_he_covariance(enc_x, enc_y, count)
        decrypted_covariance = enc_covariance.decrypt()[0]
        self.assertAlmostEqual(decrypted_covariance, expected_covariance, places=3)

if __name__ == '__main__':
    unittest.main()