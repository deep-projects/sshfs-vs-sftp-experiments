batches:
- inputs:
    text: hello
  outputs: {}
- inputs:
    text: hello
  outputs: {}
- inputs:
    text: hello
  outputs: {}
- inputs:
    text: hello
  outputs: {}
- inputs:
    text: hello
  outputs: {}
- inputs:
    text: hello
  outputs: {}
- inputs:
    text: hello
  outputs: {}
- inputs:
    text: hello
  outputs: {}
- inputs:
    text: hello
  outputs: {}
- inputs:
    text: hello
  outputs: {}
cli:
  baseCommand: echo
  class: CommandLineTool
  cwlVersion: v1.0
  doc: Simple Test Script
  inputs:
    text:
      inputBinding:
        position: 1
      type: string
  outputs: {}
container:
  engine: docker
  settings:
    image:
      url: python:3.8
    ram: 256
execution:
  engine: ccagency
  settings:
    access:
      auth:
        password: '{{cc_test_agency_password}}'
        username: '{{cc_test_agency_username}}'
      url: https://agency.f4.htw-berlin.de/cctest
    batchConcurrencyLimit: 10000000
redVersion: '9'
