# http-fun
A simple http service to try out things. 

# http-fun

## A simple http service that demonstrates DevOps

### Supported Endpoints
- /helloworld
- /versionz

### Examples

> /helloworld
>> Greets the user with a simple Hello. 
>>
>> If the endpoint is called without any parameters, service greets with "Hello Stranger"
>>
>> If the endpoint is called with a name parameter, service greets the person with name split on capitalization, like so. "Hello Person Name"
>> 
>> localhost:8080/helloworld?name=AingaranElango&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;==>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Hello Aingaran Elango"

> /versionz
>> Provides information on Application.
>>
>> Currently, configured to present latest SHA hash from its repository and the name of the project.
>>
>> ```
>> {
>>  "name": "http-fun",
>>  "git hash": "8f55f4ab9293a3ae1e1d199e9df33d8191c22c9e"
>> }
>> ```

### Setup

#### Requirements
- Python 3+
- Docker
- git

#### Setup dependencies
```
pip3 install -r requirements.txt
python3 app/make.py
```

#### Run Tests
```
python3 -m unittest test/app-test.py
```

#### Build image
```
git clone https://github.com/eaingaran/http-fun.git
cd http-fun
docker build . --tag=<image-name>:<image-tag>
```

#### Run image
```
docker run -p 5000:5000 <image-name>:<image-tag>
curl localhost:5000/helloworld
curl localhost:5000/helloworld?name=AlfredENeumann
curl localhost:5000/versionz
```
