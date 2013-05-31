#include <iostream>

using namespace std;

#include "CorbaTest.hh"

int main(int argc, char **argv) {
    if (argc != 2) {
       cout << "Expected exactly one argument: The IOR string." << endl;
       return 1;
    }

    CORBA::ORB_var orb = CORBA::ORB_init(argc, argv);

    CORBA::Object_var obj = orb->string_to_object(argv[1]);
    CorbaTest::CarFactory_var factory = CorbaTest::CarFactory::_narrow(obj);

    CorbaTest::Car_var car = factory->add_car();
    CORBA::String_var uuid = car->get_uuid();
    std::cout << "Created car with UUID " << (char *) uuid << "." << endl;

    orb->destroy();
    return 0;
}
