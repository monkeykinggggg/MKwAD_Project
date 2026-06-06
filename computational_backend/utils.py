import tenseal as ts

def compute_he_mean(enc_vector: ts.CKKSVector, count: int) -> ts.CKKSVector:
    return enc_vector.sum() * (1 / count)

def compute_he_variance(enc_vector: ts.CKKSVector, count: int) -> ts.CKKSVector:
    calculated_mean = compute_he_mean(enc_vector, count)
    
    # E[X^2]
    enc_squared = enc_vector.square()
    mean_of_squares = enc_squared.sum() * (1 / count)
    
    # (E[X])^2
    square_of_mean = calculated_mean.square()
    
    # Variance
    variance_enc = mean_of_squares - square_of_mean
    return variance_enc