#!/usr/bin/env python

# For connecting to the DynamoDB
import boto.dynamodb
# So we can get everything from environment variables, thus making the code credential agnostic, and withotu requiring files with critical secuirty data thoat could mistakenly get checked in
import os
# For parsing the result out of the JSON format
import json
# The actuall web server component
import web

# List of allowed URLs- anything else will get at best a 404
urls =(
  '/secret', 'get_secret'
  '/health', 'get_health
)

# Rhe specifications of the web application - only loopback and port 5000 are bound. 
class MyApplication(web.application):
 def run(self, port=5000, *middleware):
   func = self.wsgifunc(*middleware)
   return web.httpserver.runsimple(func, ('127.0.0.1', port))
   
# This code gets executed whenever a browser visits 127.0.0.1:5000/secret   
class get_secret:
  # We only define GET operations
  def GET(self):
  
    # Established a connection using credntials pulled from environment variables
    connection = boto.dynamodb.connect_to_region(
      os.environ['aws_region_name'],
      aws_access_key=os.environ['aws_access_key'],
      aws_secret_access_key=os.environ['aws_secret_access_key']
  
    # Specify which table to work with - agian using environment variables 
    table = connection.get_table(os.environ['table_name'])
  
    # This is the query definition and the request all in  one
    queryResponse = table.get_item(
      hash_key=os.environ['search_key']
    )
    
    # Pull out just the information we want
    item = json.dumps(queryResponse['secret_code'])
    
    # Build and return (to the requesting HTTP endpoint) the output string.
    output = '{secret_code : ' + item + ' }'
    return output
  
# This code gets executed whenever a browser visits 127.0.0.1:5000/health
class get_health:
  # We only define GET operations
  def GET(self):
    # Build and return (to the requesting HTTP endpoint) the output string.
    output = '{status: healthy, container: ,Link_to_Hub., project: github.com/nguttman/devops_challenge }'
    return output

#This code is the actual application. No exit parameter were specified, so the app will run until forceable terminated.   
if __name__ == "__main__":
  app = MyApplication(urls, globals())
  app.run()
  
  