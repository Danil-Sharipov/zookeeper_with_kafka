pipeline {
    agent any

    stages {
        stage('1z1k make topics') {
            steps {
                sh '''
                    docker run -d --name kafka-zookeeper -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=\`docker-machine ip \\`docker-machine active\\`` --env ADVERTISED_PORT=9092 spotify/kafka
                '''
            }
            steps{
                sh '''
                    docker exec kafka-zookeeper /opt/kafka_2.11-0.10.1.0/bin/zookeeper-server-start.sh -daemon zookeeper.properties
                    docker exec kafka-zookeeper /opt/kafka_2.11-0.10.1.0/bin/kafka-server-start.sh -daemon  server.properties
                    docker exec kafka-zookeeper /opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic MyTopic --partitions 1 --replication-factor 1


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
