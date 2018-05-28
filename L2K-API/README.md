# Knowledge Extraction on Korean Textual Data

## About
This module is for extracting RDF triples from Korean textual data, especially Onlympics news texts.

## Prerequisite
* `Ubuntu 16.04 LTS`
* `Java 1.8`
* `Python 3`

## How to install & execute
1. Clone this repository on your server.

2. Install dependencies by executing `sh install-dependency.sh`.

3. Download a KB from `http://qamel.kaist.ac.kr/resource/KB.zip`, and locate all the files contained in `KB.zip` under the folder `data/KB`.

4. Set IP address and port number of your server by editting `service-address.json`.

5. Finally, start REST API of L2K by executing `sh start-service.sh`.

## How to use
You can use REST API of L2K by a cURL command. The sample command is as follows:

`sample cURL command: curl -d '{"date": "2018-02-10", "content": "오늘 진행된 2018평창동계올림픽 남자 1500m 결승에서 임효준이 2분10초485를 기록하며 금메달로 결승선을 통과했다." }'  http://(IP-address):(port-number)/service`

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