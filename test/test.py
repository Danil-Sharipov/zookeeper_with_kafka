import docker

containers = docker.from_env().containers.list()
for i in containers:
	if i != 'kafka':
		continue
	exit_code,output = i.exec_run("/opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper localhost:2181 --list",user='0')
	if exit_code != 0:
		print(output)
		raise Exception("kafka-topics not work")
	exit_code,output = i.exec_run("/opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper localhost:2181 --describe --topic MyTopic",user='0')
	if exit_code != 0:
		print(output)
		raise Exception("kafka-topics not work")