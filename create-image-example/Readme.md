
# API Standard

- Microservice based design
- Each API must be completely self isolated and self sufficient (From data, compute, development and deployment perspective)
- REST Based
- Authorization: Bearer Token (JWT)
- Driven by transaction id in the form of UUID.
	- A request can either add a header X-transaction-id. In that case response will include the same value in meta tag
	- Or in case it is not available response will include a newly created transaction id


# Base URL - Microservice

Each microservice is defined as separate base url, but all mapped to a same subdomain.
Example

    /api/subdomain/v1/thirdparty
    ----------------- -----------
    Base             Microservice URL
    API subdomain

In AWS, this is achieved via multiple API bound to same custom domain with respective subdomains

# CRUD and HTTPS Methods

## Create
All Create requests are expressed as POST. Body contains resource descriptor. Response is (typically) resource id which got created, response body and response code.

Example:

    POST /thirdparty/

## Read

### List
Get requests on a collection returns the content of the collection in a list format.
Example:

    GET /thirdparty/


### Read Single Element
Get a single item from a collection.
Example:

    GET /thirdparty/{org_id}

## Update
Update a single item from a collection. It has to be full update, patch is discouraged
Example:

    PUT /thirdparty/{org_id}

## Delete
Delete a single item from a collection.  
Example:

    DELETE /thirdparty/{org_id}



## HTTP Codes

 1. GET : 200 OK
 2. POST : 201 Created
 3. PUT : 202 Accepted
 4. DELETE : 204 No Content
 5. 302 Found (Redirected)
 6. 400 Bad Request
 7. 401 Unauthorized
 8. 403 Forbidden
 9. 404 Not Found
 10. 405 Method Not Allowed
 11. 409 Conflict
 12. 429 Too Many Requests
 13. 500 Internal Server Error
 14. 502 Bad Gateway

# Parameters, Fields, Paging and Filters

## Parameters
Parameters are appended to the path after a ‘?’ and separated by a ‘&’
Example:

    GET /DEVICE_USAGE/MASKED/{USER_ID}/{PATIENT_ID}?LAST_N_RECORD=10&Between=2010-01-01,2010-12-31

## Fields or partial returns

If you don’t want to get back the full body of the reply, use the fields parameter to get a partial result:
Example:

    GET /THIRDPARTY?fields=name

## Expansion (Optional)
In case of hierarchy, it is optional to expand the full hierarchy details or just get the ids
Example:

    GET /THIRDPARTY/{ORG_ID}/PATIENTS/{PATIENT_ID}/ALERTS?expand=true



# Response Format

## General Response Structure

```
{
"meta" : {
        "request_transaction_id" : {UUID} ,
        "success": true|false,
        "request_url": "/domain/subdomain/{microservice}/{resource}/{id}",
        "request_headers": [],        
        "next" : (optional) ,
        "offset" : 0((optional) ,
        "previous" : (optional)
        }
"data" : [
           {
			"id": 1,
			"details": (some)
			},
			{
			"id": 2,
			"details": (some)
			},
		],
"error" : {error_response}
}
```

## Successful Response Structure
```
{
"meta" : {
        "request_transaction_id" : {UUID} ,
        "success": true,
        "request_url": "/domain/subdomain/{microservice}/{resource}/{id}",
        "request_headers": [],        
        "next" : (optional) ,
        "offset" : 0((optional) ,
        "previous" : (optional)
        }
"data" : [
           {
			"id": 1,
			"details": (some)
			},
			{
			"id": 2,
			"details": (some)
			},
		],
"error" : {}
}
```
## Error Response Structure

```
{
"meta" : {
        "request_transaction_id" : {UUID} ,
        "success": false,
        "request_url": "/domain/subdomain/{microservice}/{resource}/{id}",
        "request_headers": [],        
        "next" : (optional) ,
        "offset" : 0((optional) ,
        "previous" : (optional)
        }
"data" : [],
"error" :  {
           "error_reason" : "method not allowed"|UnAuthorized|Forbidden|Server Error ,
			"error_code": (Appropriate HTTPS Error Code),
			"error_msg": (Msg returned by Server)
					}
}
```

# Sample Project

### Pre-flight check

-  Istructions are tested on Ubuntu
- Git
- Python 3.7+
- Python Packages
  * virtualenv
  * pip
- Python Devel is installed
```
sudo apt-get install python-dev
```


### Get the code

```
git clone  https://github.com/ayanguha/modelapi.git
```


### Create Virtual Environment
```shell
cd modelapi
virtualenv modelapi
```
Activate the virtual environment
```
source modelapi/bin/activate
```

### Usage
To run the server, please execute the following from the root directory:

```
pip install -r requirements.txt
python3 app.py
```
