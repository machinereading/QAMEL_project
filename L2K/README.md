# Knowledge Extraction on Korean Textual Data

## About
This module is for extracting RDF triples from Korean textual data, especially Onlympics news texts.

## Prerequisite
* `Ubuntu 16.04 LTS`
* `Python 3`

## How to install & execute
1. Clone this repository on your server.

2. Install dependencies by executing `sh install-dependency.sh`.

3. Download a knowledge base (KB) from `http://qamel.kaist.ac.kr/resource/KB.zip`, and locate all the files contained in `KB.zip` under the folder `data/KB`.

4. Set IP address and port number of your server by editting `service-address.json`.

5. Finally, start REST API of L2K by executing `sh start-service.sh`.

## How to use
You can use REST API of L2K by a cURL command. The sample command is as follows:

- sample cURL command: `curl -d '{"date": "2018-02-10", "content": "임효준은 어제 오후 강릉 아이스아레나에서 열린 2018 평창올림픽 남자 쇼트트랙 500m 결승에서 3위를 기록하며 동메달을 차지했다." }'  http://(IP-address):(port-number)/service`

- sample output: 
```
[
    [
        "임효준",
        "http://www.bbc.co.uk/ontologies/sport/competesIn",
        "2018_평창_동계올림픽_쇼트트랙_여자_500m_결승_A",
        "0.9723265171051025"
    ],
    [
        "임효준",
        "http://dbpedia.org/ontology/rank",
        "3",
        "0.9665167927742004"
    ],
    [
        "임효준",
        "http://dbpedia.org/property/record",
        "2018",
        "0.921284019947052"
    ],
    [
        "2018_평창_동계올림픽_쇼트트랙_여자_500m_결승_A",
        "http://dbpedia.org/ontology/date",
        "2018-02-09",
        "0.9824678301811218"
    ],
    [
        "임효준",
        "http://dbpedia.org/property/record",
        "http://ko.dbpedia.org/resource/동메달",
        "0.9703184962272644"
    ],
    [
        "2018_평창_동계올림픽_쇼트트랙_여자_500m_결승_A",
        "http://www.bbc.co.uk/ontologies/sport/hasCompetitor",
        "임효준",
        "0.9998432397842407"
    ]
]
```

## External dependencies
This module internally uses an external REST API of a CNN model for relation extraction. Please refer to `https://github.com/machinereading/re-cnn` if you want to install the CNN model on your local server.

## Licenses
* `CC BY-NC-SA` [Attribution-NonCommercial-ShareAlike](https://creativecommons.org/licenses/by-nc-sa/2.0/)
* If you want to commercialize this resource, [please contact to us](http://mrlab.kaist.ac.kr/contact)

## Maintainer
Jiseong Kim `jiseong@kaist.ac.kr`

## Publisher
[Machine Reading Lab](http://mrlab.kaist.ac.kr/) @ KAIST

## Acknowledgement
This research was financially supported by the Ministry of Trade, Industry and Energy(MOTIE) and Korea Institute for Advancement of Technology(KIAT) through the International Cooperative R&D program.