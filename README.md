# zookeeper-with-kafka
1)
```bash
/opt/kafka_2.11-0.10.1.0/bin/zookeeper-server-start.sh -daemon zookeeper.properties
/opt/kafka_2.11-0.10.1.0/bin/kafka-server-start.sh -daemon  server.properties
# Создание топика
/opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic MyTopic --partitions 1 --replication-factor 1 
# Проверка
/opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper localhost:2181 --list
/opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper localhost:2181 --describe --topic MyTopic
# Запуск консьюмера и потребителя
/opt/kafka_2.11-0.10.1.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic MyTopic
/opt/kafka_2.11-0.10.1.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic MyTopic
## some message
# stop
/opt/kafka_2.11-0.10.1.0/bin/kafka-server-stop.sh 
/opt/kafka_2.11-0.10.1.0/bin/zookeeper-server-stop.sh 
# дублируем конфиги для продьюсера
cp /opt/kafka_2.11-0.10.1.0/config/server.properties /opt/kafka_2.11-0.10.1.0/config/server-1.properties
cp /opt/kafka_2.11-0.10.1.0/config/server.properties /opt/kafka_2.11-0.10.1.0/config/server-2.properties
```
