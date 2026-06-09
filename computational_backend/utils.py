import tenseal as ts

def compute_he_mean(enc_vector: ts.CKKSVector, count: int) -> ts.CKKSVector:
    _mean = enc_vector.sum() * (1 / count)
    return _mean

def compute_he_variance(enc_vector: ts.CKKSVector, count: int) -> ts.CKKSVector:
    """Variance = E[X^2] - (E[X])^2"""
    _mean = compute_he_mean(enc_vector, count)
    vec_squared = enc_vector.square()
    mean_of_squares = vec_squared.sum() * (1 / count)

    square_of_mean = _mean.square()
    encrypted_variance = mean_of_squares - square_of_mean
    return encrypted_variance

def compute_he_covariance(enc_x: ts.CKKSVector, enc_y: ts.CKKSVector, count: int) -> ts.CKKSVector:
    """Cov(X,Y) = E[X*Y] - E[X]*E[Y]"""
    _mean_xy = compute_he_mean(enc_x * enc_y, count)
    _mean_x = compute_he_mean(enc_x, count)
    _mean_y = compute_he_mean(enc_y, count)
    return _mean_xy - (_mean_x * _mean_y)