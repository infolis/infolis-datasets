INFOLINK_VERSION = 1.0
GIT = git
GRADLE = ./gradlew

.PHONY all: infoLink/build

.PHONY pull:
	$(GIT) submodule foreach git pull origin master
	$(GIT) add infoLink

infoLink/src:
	$(GIT) submodule init
	$(GIT) submodule update

infoLink/build : infoLink/src
	cd infoLink && $(GRADLE) jar

realclean:
	rm -r infoLink
