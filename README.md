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
>
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

Will be updated soon...
