redVersion: '9'
cli:
  cwlVersion: 'v1.0'
  class: 'CommandLineTool'
  baseCommand: 'null_cat.sh'
  doc: 'Prints the content of a file to /dev/null'

  inputs:
    infile:
      type: 'string'
      inputBinding:
        position: 1
    indir:
      type: 'Directory'
      inputBinding:
        position: 2
  outputs: {}

batches:
  - inputs:
      infile: 'infile5G.bin'
      indir:
        class: 'Directory'
        connector:
          command: "red-connector-ssh"
          mount: True
          access:
            host: "avocado01.f4.htw-berlin.de"
            dirPath: "/home/users/bschilling/test_data"
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
