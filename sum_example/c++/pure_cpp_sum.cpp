#include <iostream> // For printing
#include "pure_cpp_sum.h" // Not really necessary for such a simple example...
#include <cstdlib> // for converting to float

long long int sum_N(int N){
	long long int sum = 0;

	for (int i=0; i<N; i++){
		sum += i;
	}

	return sum;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: program <number>\n";
        return 1;
    }
	int N = static_cast<int>(std::atof(argv[1])); 
	std::cout << "C++: N= " << N/1. << ", sum = " << sum_N(N)/1. << std::endl;

	return 0;
}

