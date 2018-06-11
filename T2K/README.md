# Knowledge Extraction on Korean Tabular Data

## About

This module is for extracting RDF triples from Korean tabular data, especially Web tables written in HTML syntax.

## Prerequisite

* `Ubuntu 16.04 LTS`
* `Python 3`

## How to run

1. Clone this repository on your server.

2. Install dependencies by executing `sh install-dependency.sh`.

3. Download a knowledge base (KB) from `http://qamel.kaist.ac.kr/resource/KB.zip`, and locate all the files contained in `KB.zip` under the folder `data/KB`.

4. Set IP address and port number of your server by editting `service-address.json`.

5. Finally, start REST API of T2K by executing `sh start-service.sh`.

## How to use

You can use REST API of T2K by a cURL command. The sample command is as follows:

- sample cURL command: `curl -d '{"html_table": "<table> <tbody> <tr> <th>클럽</th> <th>연고지</th> <th>경기장</th> </tr> <tr> <td>올랭피크 마르세유</td> <td>마르세유</td> <td>스타드 벨로드롬</td> </tr> <tr> <td>AS 모나코</td> <td>모나코</td> <td>루이 2세 경기장</td> </tr> </table>"}'  http://(IP-address):(port-number)/service`

- sample output: 
```
[
    [
        "http://ko.dbpedia.org/resource/스타드_벨로드롬",
        "http://dbpedia.org/ontology/tenant",
        "http://ko.dbpedia.org/resource/올랭피크_드_마르세유",
        "0.796083927154541"
    ],
    [
        "http://ko.dbpedia.org/resource/스타드_루이_II",
        "http://dbpedia.org/ontology/tenant",
        "http://ko.dbpedia.org/resource/AS_모나코_FC",
        "0.7711466550827026"
    ],
    [
        "http://ko.dbpedia.org/resource/올랭피크_드_마르세유",
        "http://dbpedia.org/ontology/ground",
        "http://ko.dbpedia.org/resource/스타드_벨로드롬",
        "0.8142433166503906"
    ],
    [
        "http://ko.dbpedia.org/resource/AS_모나코_FC",
        "http://dbpedia.org/ontology/ground",
        "http://ko.dbpedia.org/resource/스타드_루이_II",
        "0.8178586959838867"
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