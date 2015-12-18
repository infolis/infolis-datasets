INFOLINK_VERSION = 1.0
GIT = git
GRADLE = ./gradlew

TOMCAT_MAJOR = 7
TOMCAT_MINOR_PATCH = 0.67
TOMCAT_VERSION = $(TOMCAT_MAJOR).$(TOMCAT_MINOR_PATCH)
TOMCAT_DIR = apache-tomcat-$(TOMCAT_VERSION)
TOMCAT_TARGZ = $(TOMCAT_DIR).tar.gz
TOMCAT_WEBAPPS = $(TOMCAT_DIR)/webapps/
TOMCAT_PORT = 8090
TOMCAT_URL = "http://mirror.23media.de/apache/tomcat/tomcat-$(TOMCAT_MAJOR)/v$(TOMCAT_VERSION)/bin/$(TOMCAT_TARGZ)"
TOMCAT_PID = $(shell ps aux |grep -E "java.+$(CATALINA_HOME).+org.apache.catalina.startup.Bootstrap" |grep -v grep|tr -s ' '|cut -d' ' -f2)

CATALINA_HOME = $(PWD)/$(TOMCAT_DIR)

.PHONY: all pull war deploy jar tomcat tomcat-start tomcat-stop tomcat-restart

all: infoLink/build

#
# Initialization

pull:
	$(GIT) submodule foreach git pull origin master
	$(GIT) add infoLink
	$(GIT) add corpus-creation
	$(GIT) add ocror

war: infoLink/build/libs/infoLink-$(INFOLINK_VERSION).war

realclean:
	rm -r infoLink

#
# infoLink related
#

infoLink:
	$(GIT) submodule init
	$(GIT) submodule update

infoLink/build : infoLink
	cd infoLink && $(GRADLE) jar

gradleclean:
	cd infoLink && $(GRADLE) clean

test:
	cd infoLink && $(GRADLE) cleanTest test -i

infoLink/build/libs/infoLink-$(INFOLINK_VERSION).war: gradleclean
	cd infoLink; $(GRADLE) war

jar: infoLink/build/libs/infoLink-$(INFOLINK_VERSION).jar

infoLink/build/libs/infoLink-$(INFOLINK_VERSION).jar: gradleclean
	cd infoLink; $(GRADLE) jar

deploy: war
	date > LAST_DEPLOY
	cp infoLink/build/libs/infoLink-$(INFOLINK_VERSION).war $(TOMCAT_WEBAPPS)


#
# Tomcat-related
#

tomcat: $(TOMCAT_DIR)

$(TOMCAT_DIR): $(TOMCAT_TARGZ)
	tar xmf $(TOMCAT_TARGZ)
	cat conf/server.xml | sed 's/8090/$(TOMCAT_PORT)/' > $(TOMCAT_DIR)/conf/server.xml

$(TOMCAT_TARGZ):
	wget $(TOMCAT_URL)

tomcat-start:
	$(CATALINA_HOME)/bin/startup.sh

tomcat-stop:
	kill -9 $(TOMCAT_PID)

tomcat-status:
	@if [ "x$(TOMCAT_PID)" = "x" ];then \
		echo "STOPPED"; \
	else \
		echo "RUNNING [$(TOMCAT_PID)]"; \
	fi


tomcat-restart:
	$(MAKE) tomcat-stop
	$(MAKE) tomcat-start
