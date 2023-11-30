# zookeeper-with-kafka
1)
```bash
kill -9 $(ps aux | grep server-1.properties| awk '{print $2}')
for i in $(ps aux | grep server-1.properties| awk '{print $2}');do kill -9 $i||true;done

ps aux | grep server-1.properties
docker compose exec -u 0 kafka /opt/kafka_2.11-0.10.1.0/bin/kafka-server-start.sh -daemon /opt/kafka_2.11-0.10.1.0/config/server-2.properties
./bin/zookeeper-shell.sh localhost:2181 ls /brokers/ids
./bin/kafka-topics.sh --zookeeper localhost:2181 --describe --topic replicated-topic

```
