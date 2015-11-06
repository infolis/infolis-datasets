INFOLINK_VERSION = 1.0
GIT = git
GRADLE = ./gradlew

.PHONY: all pull war

all: infoLink/build

pull:
	$(GIT) submodule foreach git pull origin master
	$(GIT) add infoLink

war:
	cd infoLink; $(GRADLE) war

infoLink:
	$(GIT) submodule init
	$(GIT) submodule update

infoLink/build : infoLink
	cd infoLink && $(GRADLE) jar

realclean:
	rm -r infoLink
