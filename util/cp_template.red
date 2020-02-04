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
            host: "avocado01.f4.htw-berlin.de"
            filePath: "/home/users/bschilling/test_data/infile5G.bin"
            auth:
              username: '{{htw_username}}'
              password: '{{htw_password}}'
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
      url: "https://agency.f4.htw-berlin.de/cctest"
      auth:
        username: "{{cc_test_agency_username}}"
        password: "{{cc_test_agency_password}}"
