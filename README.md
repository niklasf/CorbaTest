CORBA test
==========

Homework for learning CORBA as desribed in `exercise.pdf`.

![Screenshot of the program](/screenshot.png)

Build
-----
```
sudo apt-get install omniorb libomniorb4-dev omniidl omniidl-python
make
```

Running
-------
- Starting the server: `python server.py` prints the IOR string.
- Starting a client: `python client.py`
- Adding a new car: `./creator-client IOR:...`

Blueprint source
----------------
http://bibikalki.narod.ru/italjanskij/subaru/Subaru-Forester-2003/
