//============================================================================
// Name        : Performance.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <boost/any.hpp>
#include <vector>
#include <string>

using namespace std;
int main(void) {
	vector<boost::any> args;
	int a = 5;
	string b = "test";
	args.push_back(a);
	args.push_back(b);

	cout << boost::any_cast<int> (args[0]);
	cout << boost::any_cast<string>(args[1]);
	return EXIT_SUCCESS;
}
