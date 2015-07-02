Installation
------------

Installation is simple using pip. ::

  pip install arnold

Initialization
^^^^^^^^^^^^^^

To generate the arnold config folder, run the following command: ::
  
  arnold init

This will create a directory and fill it with the default content. The directory will look like this: ::

  .
  +-- arnold_config
  |   +-- __init__.py
  |   +-- migrations
  |       +-- __init__.py

You can provide an option for a custom folder name by using the `--folder` option. Note that if you provide a custom folder, you will have to pass the `--folder` option to all future arnold commands.
