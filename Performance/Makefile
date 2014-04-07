CXXFLAGS =	-O2 -g -Wall -fmessage-length=0

OBJS = src/Performance.o

LIBS = -lboost_system-mt
LD_FLAGS = -L"/usr/lib/"
INCLUDE = -I"/usr/include/"
TARGET = Performance

$(TARGET):	$(OBJS)
	$(CXX) $(INCLUDE) -o $(TARGET) $(OBJS) $(LIBS)

all:	$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)
