from calculate.algorithm.algorithm import Algorithm


class StandardAlgorithm(Algorithm):

    def inner_product(self, vector_v, vector_w):
        
        return (vector_v.transpose()@vector_w).toarray()