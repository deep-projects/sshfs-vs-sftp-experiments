redVersion: '9'
cli:
  cwlVersion: 'v1.0'
  class: 'CommandLineTool'
  baseCommand: 'null_cat.sh'
  doc: 'Prints the content of a file to /dev/null'

  inputs:
    infile:
      type: 'File'
      inputBinding:
        position: 1
  outputs: {}

batches:
  - inputs:
      infile:
        class: 'File'
        connector:
          command: "red-connector-ssh"
          access:
            host: ""
            filePath: "test_data/infile.bin"
            auth:
              username: ''
              password: ''
            bannerTimeout: 240
            timeout: 240
            authTimeout: 240
    outputs: {}

container:
  engine: 'docker'
  settings:
    image:
      url: 'bruno1996/null_cat_image:latest'
    ram: 256

execution:
  engine: "ccagency"
  settings:
    batchConcurrencyLimit: 10000000
    access:
      url: ""
      auth:
        username: ""
        password: ""
