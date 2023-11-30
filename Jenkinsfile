pipeline {
    agent any

    stages {
        stage('1p1c') {
            steps {
                git 'https://github.com/Danil-Sharipov/zookeeper_with_kafka.git'
                sh'''
                    docker compose up -d
                    docker compose exec -u 0 kafka /opt/kafka_2.11-0.10.1.0/bin/zookeeper-server-start.sh -daemon zookeeper.properties
                    docker compose exec -u 0 kafka /opt/kafka_2.11-0.10.1.0/bin/kafka-server-start.sh -daemon /opt/kafka_2.11-0.10.1.0/config/server.properties
                    sleep 10
                    docker compose exec -u 0 kafka /opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic MyTopic --partitions 1 --replication-factor 1

                '''
            }
        }
        stage('1p1c test'){
            steps{
                sh'''
                    python3 test/test.py
                '''

            }
        }
        stage('1p1c consumer+produser for only'){
            steps{
                sh'''
                    docker compose exec -u 0 producer /bin/bash -c "echo 'I am so exhausted' | /opt/kafka_2.11-0.10.1.0/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic MyTopic"
                    docker compose exec -u 0 consumer /opt/kafka_2.11-0.10.1.0/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic MyTopic --from-beginning --max-messages 1

                '''

            }
        }
        stage('3 broker'){
            steps{
                sh'''
                    docker compose exec kafka sh -c "/opt/kafka_2.11-0.10.1.0/bin/kafka-server-start.sh -daemon /opt/kafka_2.11-0.10.1.0/config/server-1.properties|sleep 2"
                    sleep 10
                    docker compose exec kafka sh -c "/opt/kafka_2.11-0.10.1.0/bin/kafka-server-start.sh -daemon /opt/kafka_2.11-0.10.1.0/config/server-2.properties|sleep 2"
                    sleep 10
                    docker compose exec -u 0 kafka /opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic replicated-topic --partitions 1 --replication-factor 3

                '''
            }
        }
        stage('3 broker test'){
            steps{
                sh'''
                    python3 test/test2.py
                '''

            }
        }
        stage('fault tolerance'){
            steps{
                sh'''
                    docker compose exec -u 0 producer /bin/bash -c "echo 'hello 1' | /opt/kafka_2.11-0.10.1.0/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic replicated-topic"
                    docker compose exec -u 0 producer /bin/bash -c "echo 'hello 2' | /opt/kafka_2.11-0.10.1.0/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic replicated-topic"
                    docker compose exec -u 0 consumer /opt/kafka_2.11-0.10.1.0/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic replicated-topic --from-beginning --max-messages 2
                    docker compose exec -u 0 kafka /opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper localhost:2181 --describe --topic replicated-topic
                    chmod +x scripts/test.sh
                    docker compose exec -u 0 -d kafka /scripts/test.sh
                    sleep 10 
                    docker compose exec -u 0 kafka /opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper localhost:2181 --describe --topic replicated-topic

                '''
            }
        }
        stage('end of suffer?'){
            steps{
                sh'''
                    docker compose exec -u 0 kafka /opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic topic-danil --partitions 1 --replication-factor 2
                    docker compose exec -u 0 producer /bin/bash -c "echo 'key 1, message 1' | /opt/kafka_2.11-0.10.1.0/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic topic-danil --property parse.key=true --property key.separator=,"
                    docker compose exec -u 0 producer /bin/bash -c "echo 'key 2, message 2' | /opt/kafka_2.11-0.10.1.0/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic topic-danil --property parse.key=true --property key.separator=,"
                    docker compose exec -u 0 producer /bin/bash -c "echo 'null, message 2' | /opt/kafka_2.11-0.10.1.0/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic topic-danil --property parse.key=true --property key.separator=,"
                    docker compose exec -u 0 consumer /opt/kafka_2.11-0.10.1.0/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic topic-danil --from-beginning --max-messages 3


                '''
            }
        }
        stage('read file.log'){
            steps{
                sh'''
                    docker compose exec -u 0 kafka /opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic topic-end --partitions 1 --replication-factor 2
                    chmod +r /file.log
                    docker compose exec -u 0 producer /bin/bash -c "/opt/kafka_2.11-0.10.1.0/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic topic-end < /file.log"
                    docker compose exec -u 0 consumer /opt/kafka_2.11-0.10.1.0/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic topic-end --from-beginning --max-messages 15

                '''
            }
        }
        
    }
    post {
     success {
        withCredentials([string(credentialsId: 'botSecret', variable: 'TOKEN'), string(credentialsId: 'chatId', variable: 'CHAT_ID')]) {
        sh  ("""
            curl -s -X POST https://api.telegram.org/bot${TOKEN}/sendMessage -d chat_id=${CHAT_ID} -d parse_mode=markdown -d text='*${env.JOB_NAME}* : POC *Branch*: ${env.GIT_BRANCH} *Build* : OK *Published* = YES'
        """)
        }
     }

     aborted {
        withCredentials([string(credentialsId: 'botSecret', variable: 'TOKEN'), string(credentialsId: 'chatId', variable: 'CHAT_ID')]) {
        sh  ("""
            curl -s -X POST https://api.telegram.org/bot${TOKEN}/sendMessage -d chat_id=${CHAT_ID} -d parse_mode=markdown -d text='*${env.JOB_NAME}* : POC *Branch*: ${env.GIT_BRANCH} *Build* : `Aborted` *Published* = `Aborted`'
        """)
        }

     }
     failure {
        withCredentials([string(credentialsId: 'botSecret', variable: 'TOKEN'), string(credentialsId: 'chatId', variable: 'CHAT_ID')]) {
        sh  ("""
            curl -s -X POST https://api.telegram.org/bot${TOKEN}/sendMessage -d chat_id=${CHAT_ID} -d parse_mode=markdown -d text='*${env.JOB_NAME}* : POC  *Branch*: ${env.GIT_BRANCH} *Build* : `not OK` *Published* = `no`'
        """)
        }
     }

 }

}
