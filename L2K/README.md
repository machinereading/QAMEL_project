# Knowledge Extraction on Korean Textual Data

## About

This module is for extracting RDF triples from Korean textual data, especially Onlympics news texts.

## Prerequisite

* `Ubuntu 16.04 LTS`
* `Java 1.8`
* `Python 3`

## How to execute

1. Clone this repository on your server.

2. Go to each `CNN-API` and `L2K-API` and install dependencies by executing 'sh install-dependency.sh'.

3. Download a word embedding model from `http://qamel.kaist.ac.kr/resource/ko_vec_100dim_1min_pos_stem`, and locate it under `CNN-API/data/embedding`.

4. Download a KB from `http://qamel.kaist.ac.kr/resource/KB.zip`, and locate all the files contained in `KB.zip` under `L2K-API/data/KB`.

5. Go to `CNN-API` and start L2K by executing `sh start-service.sh`.

6. Go to `L2K-API`, set IP address and port number of your server by editting `service-address.json`, and start REST API of L2K by executing `sh start-service.sh`.

## How to use

You can use REST API of L2K by a cURL command. The sample command is as follows:

`sample cURL command: curl -d '{"date": "2018-02-10", "content": "오늘 진행된 2018평창동계올림픽 남자 1500m 결승에서 임효준이 2분10초485를 기록하며 금메달로 결승선을 통과했다." }'  http://(IP-address):(port-number)/service`

## Licenses
* `CC BY-NC-SA` [Attribution-NonCommercial-ShareAlike](https://creativecommons.org/licenses/by-nc-sa/2.0/)
* If you want to commercialize this resource, [please contact to us](http://mrlab.kaist.ac.kr/contact)

## Maintainer
Jiseong Kim `jiseong@kaist.ac.kr`

## Publisher
[Machine Reading Lab](http://mrlab.kaist.ac.kr/) @ KAIST