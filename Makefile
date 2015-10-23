INFOLINK_VERSION = 1.0
INFOLINK_JAR = infoLink-$(INFOLINK_VERSION).jar
GIT = git
GRADLE = ./gradlew

all: infoLink-jar

.PHONY pull:
	$(GIT) submodule foreach git pull origin master
	$(GIT) add infoLink

infoLink:
	$(GIT) submodule init
	$(GIT) submodule update

infoLink-jar: infoLink/build/libs/$(INFOLINK_JAR)

infoLink/build/libs/$(INFOLINK_JAR): infoLink
	cd infoLink && $(GRADLE) jar
	
