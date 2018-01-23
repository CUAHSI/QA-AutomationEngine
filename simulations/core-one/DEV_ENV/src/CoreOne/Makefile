JFLAGS = -g -classpath .:.. -Xlint:unchecked
JC = javac
.SUFFIXES: .java .class
.java.class:
	$(JC) $(JFLAGS) $*.java

CLASSES = \
	AutomatedTestingEngine.java \
	Github.java \
	GithubThread.java \
	JenkinsEmailPlugin.java \
	JenkinsJob.java \
	JenkinsJobCoord.java \
	JenkinsSystem.java \
	JenkinsView.java \
	SeleniumGridHub.java \
	SeleniumGridNode.java

default: classes

classes: $(CLASSES:.java=.class)
	chmod 755 *.java *.class
	rm ../../../DEVS_Suite_3.0.0_executable_linux_64/bin/CoreOne/*
	rm ../../../DEVS_Suite_3.0.0_executable_linux_64/src/CoreOne/*
	cp *.java ../../../DEVS_Suite_3.0.0_executable_linux_64/bin/CoreOne/
	cp *.java ../../../DEVS_Suite_3.0.0_executable_linux_64/src/CoreOne/
	cp *.class ../../../DEVS_Suite_3.0.0_executable_linux_64/src/CoreOne/

clean:
	$(RM) *.class
