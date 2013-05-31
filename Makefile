all creator-client: creator-client.o CorbaTestSK.o CorbaTest_idl.py
	g++ -g -o creator-client creator-client.o CorbaTestSK.o -lomniORB4 -lomnithread -lomniDynamic4

creator-client.o: creator-client.cc
	g++ -g -c creator-client.cc

CorbaTestSK.o: CorbaTestSK.cc
	g++ -g -c CorbaTestSK.cc

CorbaTestSK.cc: CorbaTest.idl
	omniidl -bcxx CorbaTest.idl

CorbaTest_idl.py: CorbaTest.idl
	omniidl -bpython CorbaTest.idl
