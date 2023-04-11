{ listen, pythonpath }:
''
  import multiprocessing

  workers = multiprocessing.cpu_count() * 2 + 1
  bind = "${listen}"

  proc_name = "ekklesia-portal"
  pythonpath = "${pythonpath}"
''
