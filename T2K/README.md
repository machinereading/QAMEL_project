# Knowledge Extraction on Korean Tabular Data

## About

This module is for extracting RDF triples from Korean tabular data, especially Web tables written in HTML syntax.

## Prerequisite

* `Ubuntu 16.04 LTS`
* `Java 1.8`
* `Python 3`

## How to execute

1. Clone this repository on your server.

2. Go to the folder `T2K-API` and install dependencies by executing `sh install-dependency.sh`.

3. Download a word embedding model from `http://qamel.kaist.ac.kr/resource/ko_vec_100dim_1min_pos_stem`, and locate it under the folder `CNN-API/data/embedding`.

4. Download a KB from `http://qamel.kaist.ac.kr/resource/KB.zip`, and locate all the files contained in `KB.zip` under the folder `T2K-API/data/KB`.

5. Go to the folder `CNN-API` and start L2K by executing `sh start-service.sh`.

6. Go to the folder `T2K-API`, set IP address and port number of your server by editting `service-address.json`, and start REST API of T2K by executing `sh start-service.sh`.

## How to use

You can use REST API of T2K by a cURL command. The sample command is as follows:

`sample cURL command: curl -d '{"html_table": "<table> <tbody> <tr> <th>소속 리그</th> <th>소속</th> <th>감독</th> </tr> <tr> <td>센트럴 리그</td> <td>요미우리 자이언츠</td> <td>하라 다쓰노리</td> </tr> <tr> <td>퍼시픽 리그</td> <td>세이부 라이온스</td> <td>이하라 하루키</td> </tr> </tbody> </table>"}'  http://(IP-address):(port-number)/service`

## Licenses
* `CC BY-NC-SA` [Attribution-NonCommercial-ShareAlike](https://creativecommons.org/licenses/by-nc-sa/2.0/)
* If you want to commercialize this resource, [please contact to us](http://mrlab.kaist.ac.kr/contact)

## Maintainer
Jiseong Kim `jiseong@kaist.ac.kr`

## Publisher
[Machine Reading Lab](http://mrlab.kaist.ac.kr/) @ KAIST