ifeq ($(OS), Windows_NT)
	ifeq ($(PROCESSOR_ARCHITEW6432), AMD64)
		ARCH="64bit"
	else
		ifeq ($(PROCESSOR_ARCHITECTURE), AMD64)
			ARCH="64bit"
		else
			ifeq ($(PROCESSOR_ARCHITECTURE), x86)
				ARCH="32bit"
			endif
		endif
	endif
	include Makefile.Windows
else
	UNAME_S := $(shell uname -s)
	UNAME_A := $(shell uname -a)
	ifeq ($(UNAME_S), Linux)
		ifeq ($(findstring x86_64, $(UNAME_A)), x86_64)
			ARCH="64bit"
		else
			ARCH="32bit"
		endif
		include Makefile.Linux
	endif
	ifeq ($(UNAME_S), Darwin)
		include Makefile.MacOSX
	endif
endif
