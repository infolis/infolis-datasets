INFOLINK_VERSION = 1.0
GIT = git
GRADLE = ./gradlew
TOMCAT_WEBAPPS = $(HOME)/build/apache-tomcat-7.0.64/webapps/

.PHONY: all pull war deploy

all: infoLink/build

pull:
	$(GIT) submodule foreach git pull origin master
	$(GIT) add infoLink
	$(GIT) add corpus-creation/

war: infoLink/build/libs/infoLink-$(INFOLINK_VERSION).war

infoLink/build/libs/infoLink-$(INFOLINK_VERSION).war: gradleclean
	cd infoLink; $(GRADLE) war

deploy: war
	cp infoLink/build/libs/infoLink-$(INFOLINK_VERSION).war $(TOMCAT_WEBAPPS)

infoLink:
	$(GIT) submodule init
	$(GIT) submodule update

infoLink/build : infoLink
	cd infoLink && $(GRADLE) jar

gradleclean:
	cd infoLink && $(GRADLE) clean

start:
	$(CATALINA_HOME)/bin/startup.sh

stop:
	$(CATALINA_HOME)/bin/shutdown.sh

restart: 
	$(MAKE) stop
	$(MAKE) start

realclean:
	rm -r infoLink

test:
	cd infoLink && $(GRADLE) cleanTest test -i
