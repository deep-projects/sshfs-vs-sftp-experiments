batches:
- inputs:
    infile:
      class: File
      connector:
        access:
          auth:
            password: '{{htw_password}}'
            username: '{{htw_username}}'
          filePath: /home/users/bschilling/test_data/infile5G.bin
          host: avocado01.f4.htw-berlin.de
        command: red-connector-ssh
  outputs: {}
cli:
  baseCommand: null_cat.sh
  class: CommandLineTool
  cwlVersion: v1.0
  doc: Prints the content of a file to /dev/null
  inputs:
    infile:
      inputBinding:
        position: 1
      type: File
  outputs: {}
container:
  engine: docker
  settings:
    image:
      url: bruno1996/null_cat_image:latest
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
