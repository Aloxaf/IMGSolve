
CFLAGS=$(shell python-config --cflags)
LDFLAGS=$(shell python-config --ldflags)


Cdenoise.so: Cdenoise.o
	${CC} -shared Cdenoise.o ${LDFLAGS} -o Cdenoise.so -s

Cdenoise.o: Cdenoise.c
	${CC} -c -fPIC ${CFLAGS} Cdenoise.c -O3

Cdenoise.c: Cdenoise.pyx
	cython Cdenoise.pyx

.PHONY:clean
clean:
	-rm *.so, *.o, *.c
