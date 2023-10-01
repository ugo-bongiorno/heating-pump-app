CC=gcc
CFLAGS=-fPIC -L${LIBMODBUS_INSTALL_PATH} -I${LIBMODBUS_INSTALL_PATH} -lmodbus

all: hp_tools.so manual_test/test_script

hp_tools.o: hp_tools.c hp_tools.h
	$(CC) -c hp_tools.c $(CFLAGS)

hp_tools.so: hp_tools.o
	$(CC) hp_tools.o -shared -o hp_tools.so $(CFLAGS)

manual_test/test_script.o: manual_test/test_script.c
	$(CC) -c manual_test/test_script.c -o manual_test/test_script.o $(CFLAGS)

manual_test/test_script: hp_tools.o hp_tools.h manual_test/test_script.o
	$(CC) hp_tools.o manual_test/test_script.o -o manual_test/test_script $(CFLAGS)

clean:
	rm -f hp_tools.o hp_tools.so manual_test/test_script.o manual_test/test_script
