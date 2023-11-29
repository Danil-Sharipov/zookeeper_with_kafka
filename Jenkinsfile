pipeline {
    agent any

    stages {
        stage('1p1c') {
            steps {
                git 'https://github.com/Danil-Sharipov/zookeeper_with_kafka.git'
                sh '''
                    docker compose up -d
                '''
            }
            steps{
                sh '''
                    docker compose exec -u 0 consumer /opt/kafka_2.11-0.10.1.0/bin/zookeeper-server-start.sh -daemon zookeeper.properties
                    docker compose exec -u 0 producer /opt/kafka_2.11-0.10.1.0/bin/zookeeper-server-start.sh -daemon zookeeper.properties
                    docker compose exec -u 0 consumer /opt/kafka_2.11-0.10.1.0/bin/kafka-server-start.sh -daemon  server.properties
                    docker compose exec -u 0 producer /opt/kafka_2.11-0.10.1.0/bin/kafka-server-start.sh -daemon  server.properties
                    docker compose exec -u 0 consumer /opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper consumer:2181 --create --topic MyTopic --partitions 1 --replication-factor 1
                    docker compose exec -u 0 producer /opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper producer:2181 --create --topic MyTopic --partitions 1 --replication-factor 1


                '''
                

            }
        }
        stage('1z1k test'){
            steps{
                sh'''
                    python3 test/test.py
                '''

            }
        }
        stage('1z1k consumer+produser for only'){
            steps{
                sh'''
                    
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
