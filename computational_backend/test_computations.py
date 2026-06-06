import pytest
import tenseal as ts
from utils import compute_he_mean, compute_he_variance
import numpy as np

@pytest.fixture(scope="module")
def he_context():
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = 2**40
    context.generate_galois_keys()
    return context

def test_compute_he_mean(he_context):
    raw_data = [20.0, 30.0, 40.0, 50.0]
    count = len(raw_data)
    expected_mean = np.mean(raw_data)
    
    enc_vector = ts.ckks_vector(he_context, raw_data)
    
    enc_result = compute_he_mean(enc_vector, count)
    decrypted_result = enc_result.decrypt()[0]
    
    assert pytest.approx(decrypted_result, rel=1e-3) == expected_mean

def test_compute_he_variance(he_context):
    raw_data = [120.0, 130.0, 140.0, 150.0]
    count = len(raw_data)
    expected_variance = np.var(raw_data) # Population variance
    
    enc_vector = ts.ckks_vector(he_context, raw_data)
    
    enc_result = compute_he_variance(enc_vector, count)
    decrypted_result = enc_result.decrypt()[0]
    
    assert pytest.approx(decrypted_result, rel=1e-3) == expected_variance