# Knowledge Extraction on Korean Tabular Data

## About

This module is for extracting RDF triples from Korean tabular data, especially Web tables written in HTML syntax.

## Prerequisite

* `Ubuntu 16.04 LTS`
* `Python 3`

## How to execute

1. Clone this repository on your server.

2. Install dependencies by executing `sh install-dependency.sh`.

3. Download a KB from `http://qamel.kaist.ac.kr/resource/KB.zip`, and locate all the files contained in `KB.zip` under the folder `data/KB`.

4. Set IP address and port number of your server by editting `service-address.json`.

5. Finally, start REST API of T2K by executing `sh start-service.sh`.

## How to use

You can use REST API of T2K by a cURL command. The sample command is as follows:

- sample cURL command: `curl -d '{"html_table": "<table> <tbody> <tr> <th>소속 리그</th> <th>소속</th> <th>감독</th> </tr> <tr> <td>센트럴 리그</td> <td>요미우리 자이언츠</td> <td>하라 다쓰노리</td> </tr> <tr> <td>퍼시픽 리그</td> <td>세이부 라이온스</td> <td>이하라 하루키</td> </tr> </tbody> </table>"}'  http://(IP-address):(port-number)/service`

- sample output: 
```
[
    [
        "http://ko.dbpedia.org/resource/센트럴_리그",
        "http://dbpedia.org/ontology/team",
        "http://ko.dbpedia.org/resource/요미우리_자이언츠",
        "0.9311381578445435"
    ],
    [
        "http://ko.dbpedia.org/resource/요미우리_자이언츠",
        "http://dbpedia.org/ontology/team",
        "http://ko.dbpedia.org/resource/센트럴_리그",
        "0.9128541350364685"
    ],
    [
        "http://ko.dbpedia.org/resource/퍼시픽_리그",
        "http://dbpedia.org/ontology/team",
        "http://ko.dbpedia.org/resource/사이타마_세이부_라이온스",
        "0.9311381578445435"
    ],
    [
        "http://ko.dbpedia.org/resource/사이타마_세이부_라이온스",
        "http://dbpedia.org/ontology/team",
        "http://ko.dbpedia.org/resource/퍼시픽_리그",
        "0.9128541350364685"
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